from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
from enum import IntEnum, auto
# Зовнішній пакунок
# Цей пакунок
# Внутрішній пакунок
# Бібліотеки Blender
import gpu
from mathutils import Matrix

##############################
# Імпорт для перевірки типів #
##############################
if __debug__:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        # Стандартні бібліотеки
        from typing import Literal
        # Зовнішній пакунок
        # Цей пакунок
        # Внутрішній пакунок
        # Бібліотеки Blender
        from gpu.types import GPUTexture
        from bpy.types import Context, AddonPreferences, UILayout


__all__ = (
    "AAPreset",
    "AABase",
)


class AAPreset(IntEnum):
    """
    Перелік шаблонів згладжування.
    """

    NONE = auto()
    "Без згладжування."
    LOW = auto()
    "Низький."
    MEDIUM = auto()
    "Середній."
    HIGH = auto()
    "Високий."
    ULTRA = auto()
    "Найвищий."


class AABase(object):
    """
    Базовий клас для методів згладжування.

    :cvar str name: Назва методу згладжування, відповідає назві дочірнього класу, лише для зчитування.
    :cvar str description: Опис методу згладжування.

    :ivar str preset: Поточний шаблон налаштувань.
    """
    __slots__ = (
        "_preset",
        "_preset_0",
    )
    _preset: AAPreset
    _preset_0: AAPreset

    description: str = ""

    def __init__(self, *, area_type='VIEW_3D', region_type='WINDOW'):
        self._preset = AAPreset.NONE
        self._preset_0 = AAPreset.NONE

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

    @property
    def preset(self) -> Literal['NONE', 'LOW', 'MEDIUM', 'HIGH', 'ULTRA']:
        return self._preset.name

    @preset.setter
    def preset(self, value: Literal['NONE', 'LOW', 'MEDIUM', 'HIGH', 'ULTRA']):
        val_eval = AAPreset.NONE
        try:
            val_eval = AAPreset[value]
        except KeyError:
            str_possible_values = ', '.join(AAPreset.__members__.keys())
            raise KeyError(f"Key '{value}' not found in {str_possible_values}")
        else:
            self._preset = val_eval

    def _do_preset_eval(self) -> bool:
        if self._preset_0 != self._preset:
            self._preset_0 = self._preset
            return True
        return False

    @staticmethod
    def _setup_gpu_state(alpha_premult: bool = True):
        gpu.matrix.load_matrix(Matrix.Identity(4))
        gpu.matrix.load_projection_matrix(Matrix.Identity(4))
        gpu.state.blend_set('ALPHA_PREMULT' if alpha_premult else 'ALPHA')
        # Не потрібно встановлювати взагалі, https://github.com/BlenderHQ/path_tool/issues/5
        # gpu.state.front_facing_set(False)
        # FRONT | BACK створює ґлітчі під час рендерингу у фоновому режимі.
        # gpu.state.face_culling_set('NONE')
        gpu.state.depth_mask_set(False)
        gpu.state.depth_test_set('ALWAYS')

    def modal_eval(
            self,
            context: Context,
            *,
            texture_width: int = 0,
            texture_height: int = 0,
            color_format: str = "",
            percentage: int = 100
    ):
        """
        Оновлення відповідно до поточного контексту. Необхідно робити виклик в модальному методі оператора.

        :param context: Поточний контекст виконання.
        :type context: `Context`_
        :param texture_width: Ширина текстури, за замовчуванням 0
        :type texture_width: int, опційно
        :param texture_height: Висота текстури, за замовчуванням 0
        :type texture_height: int, опційно
        :param color_format: Формат текстури кольору, за замовчуванням ""
        :type color_format: str, опційно
        :param percentage: Відсоток від розміру переглядача, за замовчуванням 100.
        :type percentage: int, опційно
        """
        pass

    def draw(self, *, texture: GPUTexture) -> None:
        """
        Метод відображення текстури в переглядачі. Перезаписаний метод дочірнього класу повинен починатися з

        .. code-block:: python

            super().draw(texture=texture)

        Відбудеться перевірка того що метод згладжування не викликано для відображення коли обрано опцію
        :attr:`AAPreset.NONE`

        :param texture: Текстура для відображення.
        :type texture: `GPUTexture`_
        """
        assert (AAPreset.NONE != self._preset)

    @staticmethod
    def ui_preferences(layout: UILayout, *, pref: AddonPreferences, **kwargs):
        """
        Відображення користувацьких налаштувань методу згладжування.

        :param layout: Поточний інтерфейс користувача.
        :type layout: `UILayout`_
        :param pref: Екземпляр користувацьких налаштувань.
        :type pref: `AddonPreferences`_
        """
        pass

    def update_from_preferences(self, *, pref: AddonPreferences, **kwargs):
        """
        Оновлення параметрів згладжування з користувацьких налаштувань.

        :param pref: Екземпляр користувацьких налаштувань.
        :type pref: `AddonPreferences`_
        """
        pass
