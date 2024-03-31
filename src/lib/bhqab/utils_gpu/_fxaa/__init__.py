from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
import os
# Зовнішній пакунок
from .. _aa_base import AABase, AAPreset
from .. _batch_preset import BatchPreset
from .. _framebuffer_framework import Mode
from .. _viewport_metrics import get_viewport_metrics
# Цей пакунок
# Внутрішній пакунок
# Бібліотеки Blender
from bpy.props import EnumProperty, FloatProperty
from gpu.types import GPUShader, GPUShaderCreateInfo, GPUStageInterfaceInfo
import gpu

##############################
# Імпорт для перевірки типів #
##############################
if __debug__:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        # Стандартні бібліотеки
        # Зовнішній пакунок
        # Цей пакунок
        # Внутрішній пакунок
        # Бібліотеки Blender
        pass

__all__ = ("FXAA",)


class FXAA(AABase):
    __slots__ = (
        "_value",
        "_value_0",
        "_shader_eval",
    )

    description: str = "Fast approximate anti-aliasing"

    if __debug__:
        _shader_eval: None | GPUShader
        "Шейдер скомпільований з поточними налаштуваннями."
        _value: float
        "Проміжне значення якості між шаблонами."
        _value_0: float
        "Проміжне значення якості між шаблонами (для відстеження змін)."

    _cached_shader_code: tuple[str] = tuple()
    "Кешований текст шейдера."

    # NOTE: Кількість масивів завжди рівна кількості елементів переліку `_AAPreset`.
    __quality_lookup__: tuple[tuple, tuple, tuple, tuple] = (
        (10, 11, 12, 13, 14, 15,),  # _AAPreset.LOW
        (20, 21, 22, 23, 24, 25,),  # _AAPreset.MEDIUM
        (26, 27, 28, 29,),  # _AAPreset.HIGH
        (39,)  # _AAPreset.ULTRA
    )

    @classmethod
    def get_prop_preset(cls) -> EnumProperty:
        """
        Властивість якості обробки для відображення в користувацьких налаштування.
        """
        return EnumProperty(
            items=(
                (AAPreset.NONE.name, "None", "Do not use fast approximate anti-aliasing"),
                (AAPreset.LOW.name, "Low", "Default medium dither"),
                (AAPreset.MEDIUM.name, "Medium", "Less dither, faster"),
                (AAPreset.HIGH.name, "High", "Less dither, more expensive"),
                (AAPreset.ULTRA.name, "Ultra", "No dither, very expensive"),
            ),
            default=AAPreset.HIGH.name,
            options={'HIDDEN', 'SKIP_SAVE'},
            translation_context='BHQAB_Preferences',
            name="Preset",
            description="Fast approximate anti-aliasing quality preset"
        )

    @classmethod
    def get_prop_value(cls) -> FloatProperty:
        """
        Властивість проміжного значення якості для відображення в користувацьких налаштуваннях.
        """
        return FloatProperty(
            min=0, max=1, default=1.0, step=0.001,
            subtype='PERCENTAGE',
            options={'HIDDEN', 'SKIP_SAVE'},
            translation_context='BHQAB_Preferences',
            name="Quality",
            description="FXAA preset quality tuning"
        )

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value) -> None:
        self._value = max(0.0, min(1.0, float(value)))

    def _do_value_eval(self):
        if self._value_0 != self._value:
            self._value_0 = self._value
            return True
        return False

    def _eval_shader(self):
        cls = self.__class__
        if AAPreset.NONE != self._preset:
            _do_update_on_preset_change = self._do_preset_eval()
            _do_update_on_value_change = self._do_value_eval()
            if self._shader_eval is None or _do_update_on_preset_change or _do_update_on_value_change:
                if not cls._cached_shader_code:
                    with (open(os.path.join(os.path.dirname(__file__), "fxaa.vert")) as fxaa_vert_file,
                          open(os.path.join(os.path.dirname(__file__), "fxaa.frag")) as fxaa_frag_file,
                          open(os.path.join(os.path.dirname(__file__), "fxaa_lib.glsl")) as fxaa_lib_file):
                        cls._cached_shader_code = (fxaa_vert_file.read(), fxaa_frag_file.read(), fxaa_lib_file.read())

                lookup = cls.__quality_lookup__[int(self._preset) - 2]
                preset_value = lookup[max(0, min(len(lookup) - 1, int(len(lookup) * self._value)))]

                vertexcode, fragcode, libcode = cls._cached_shader_code

                info = GPUShaderCreateInfo()
                info.define("FXAA_QUALITY__PRESET", str(preset_value))

                info.vertex_in(0, 'VEC2', "P")
                info.vertex_in(1, 'VEC2', "UV")

                info.sampler(0, 'FLOAT_2D', "u_Image")
                info.push_constant('VEC4', "u_ViewportMetrics", 0)

                vs_out = GPUStageInterfaceInfo("vs_out")
                vs_out.smooth('VEC2', "v_pos")
                info.vertex_out(vs_out)

                info.fragment_out(0, 'VEC4', "f_Color")

                info.typedef_source(libcode)
                info.vertex_source(vertexcode)
                info.fragment_source(fragcode)

                self._shader_eval = gpu.shader.create_from_info(info)
        else:
            self._shader_eval = None

    def modal_eval(
            self,
            context,
            *,
            texture_width=0,
            texture_height=0,
            color_format="",
            percentage=100
    ):
        # Задокументовано в 'AABase'
        self._eval_shader()

    def __init__(
        self,
        *,
        mode=Mode.REGION,
        area_type='VIEW_3D',
        region_type='WINDOW'
    ):
        super().__init__(area_type=area_type, region_type=region_type)
        self._value = 0.0
        self._value_0 = 0.0
        self._shader_eval = None

        assert (BatchPreset.get_ndc_rectangle_tris_P_UV() is not None)

    def draw(self, *, texture):
        # Задокументовано в 'AABase'
        shader = self._shader_eval

        super().draw(texture=texture)

        viewport_metrics = get_viewport_metrics()

        with gpu.matrix.push_pop():
            self._setup_gpu_state()

            shader.uniform_sampler("u_Image", texture)
            shader.uniform_float("u_ViewportMetrics", viewport_metrics)
            BatchPreset.get_ndc_rectangle_tris_P_UV().draw(shader)

    @staticmethod
    def ui_preferences(layout, *, pref, **kwargs):
        # Задокументовано в 'AABase'
        attr_fxaa_preset = kwargs.get("attr_fxaa_preset", "fxaa_preset")
        layout.prop(pref, attr_fxaa_preset)
        fxaa_preset = getattr(pref, attr_fxaa_preset)
        row = layout.row()
        row.enabled = fxaa_preset != AAPreset.ULTRA.name
        row.prop(pref, kwargs.get("attr_fxaa_value", "fxaa_value"))

    def update_from_preferences(self, *, pref, **kwargs):
        # Задокументовано в 'AABase'
        self.preset = getattr(pref, kwargs.get("attr_fxaa_preset", "fxaa_preset"))
        self.value = getattr(pref, kwargs.get("attr_fxaa_value", "fxaa_value"))
