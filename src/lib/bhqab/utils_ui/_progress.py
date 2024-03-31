from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
# Зовнішній пакунок
# Цей пакунок
from . _unique_name import eval_unique_name
from . _wrapped_text import draw_wrapped_text
# Внутрішній пакунок
# Бібліотеки Blender
import bpy
from bl_ui import space_statusbar
from bpy.types import PropertyGroup, WindowManager, STATUSBAR_HT_header
from bpy.props import StringProperty, FloatProperty, BoolProperty, IntProperty, CollectionProperty

##############################
# Імпорт для перевірки типів #
##############################
if __debug__:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        # Стандартні бібліотеки
        from typing import Generator
        # Зовнішній пакунок
        # Цей пакунок
        # Внутрішній пакунок
        # Бібліотеки Blender
        from bpy.types import Context, UILayout

__all__ = ("progress",)


def _update_statusbar():
    bpy.context.workspace.status_text_set(text=None)


class _progress_meta(type):
    @property
    def PROGRESS_BAR_UI_UNITS(cls):
        return cls._PROGRESS_BAR_UI_UNITS

    @PROGRESS_BAR_UI_UNITS.setter
    def PROGRESS_BAR_UI_UNITS(cls, value):
        cls._PROGRESS_BAR_UI_UNITS = max(cls._PROGRESS_BAR_UI_UNITS_MIN, min(value, cls._PROGRESS_BAR_UI_UNITS_MAX))


class progress(metaclass=_progress_meta):
    """
    Клас для відображення індикаторів прогресу в рядку статусу.

    :cvar int PROGRESS_BAR_UI_UNITS: Кількість одиниць користувацького інтерфейсу [4...12] для одного індикатора
        прогресу (ширина заголовку і значка не враховується). За замовчуванням - 6 (тільки для читання).

    .. versionadded:: 3.3
    """

    _PROGRESS_BAR_UI_UNITS = 6
    _PROGRESS_BAR_UI_UNITS_MIN = 4
    _PROGRESS_BAR_UI_UNITS_MAX = 12

    _is_drawn = False
    _attrname = ""

    class ProgressPropertyItem(PropertyGroup):
        """
        Індикатор прогресу.
        """

        identifier: StringProperty(
            maxlen=64,
            options={'HIDDEN'},
        )
        """
        Ідентифікатор індикатора прогресу (назва).

        .. versionadded:: 3.6
        """

        def _common_value_update(self, _context):
            _update_statusbar()

        valid: BoolProperty(
            default=True,
            update=_common_value_update,
        )

        num_steps: IntProperty(
            min=1,
            default=1,
            subtype='UNSIGNED',
            options={'HIDDEN'},
            update=_common_value_update,
        )
        """
        Кількість кроків виконання операції.

        .. versionadded:: 3.3
        """

        step: IntProperty(
            min=0,
            default=0,
            subtype='UNSIGNED',
            options={'HIDDEN'},
            update=_common_value_update,
        )
        """
        Поточний крок виконання операції.

        .. versionadded:: 3.3
        """

        def _get_progress(self):
            return (self.step / self.num_steps) * 100

        def _set_progress(self, _value):
            pass

        value: FloatProperty(
            min=0.0,
            max=100.0,
            precision=1,
            get=_get_progress,
            # set=_set_progress,
            subtype='PERCENTAGE',
            options={'HIDDEN'},
        )
        """
        Оцінений прогрес виконання, лише для зчитування.

        .. versionadded:: 3.3
        """

        icon: StringProperty(
            default='NONE',
            maxlen=64,
            options={'HIDDEN'},
            update=_common_value_update,
        )
        """
        Значок для відображення.

        .. versionadded:: 3.3
        """

        icon_value: IntProperty(
            min=0,
            default=0,
            subtype='UNSIGNED',
            options={'HIDDEN'},
            update=_common_value_update,
        )
        """
        Індекс значка попереднього перегляду для відображення.

        .. versionadded:: 3.3
        """

        label: StringProperty(
            default="Progress",
            options={'HIDDEN'},
            update=_common_value_update,
        )
        """
        Заголовок.

        .. versionadded:: 3.3
        """

        cancellable: BoolProperty(
            default=False,
            options={'HIDDEN'},
            update=_common_value_update,
        )
        """
        Чи відображувати кнопку скасування операції.

        .. versionadded:: 3.3
        """

    def _func_draw_progress(self, context: Context):
        layout: UILayout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.template_input_status()
        layout.separator_spacer()
        layout.template_reports_banner()

        if hasattr(WindowManager, progress._attrname):
            layout.separator_spacer()
            for item in progress.valid_progress_items():
                row = layout.row(align=True)
                row.label(text=item.label, icon=item.icon, icon_value=item.icon_value)

                srow = row.row(align=True)
                srow.ui_units_x = progress.PROGRESS_BAR_UI_UNITS
                srow.prop(item, "value", text="")

                if item.cancellable:
                    row.prop(item, "valid", text="", icon='X', toggle=True, invert_checkbox=True)

        layout.separator_spacer()

        row = layout.row()
        row.alignment = 'RIGHT'

        row.label(text=context.screen.statusbar_info())

    @classmethod
    def progress_items(cls) -> tuple[ProgressPropertyItem]:
        return tuple(getattr(bpy.context.window_manager, cls._attrname, tuple()))

    @classmethod
    def valid_progress_items(cls) -> Generator[ProgressPropertyItem]:
        """
        Генератор що містить лише незавершені індикатори прогресу.

        :yield: Незавершений прогрес.
        :rtype: Generator[:class:`ProgressPropertyItem`]
        """
        return (_ for _ in cls.progress_items() if _.valid)

    @classmethod
    def _get(cls, *, identifier: str) -> None | ProgressPropertyItem:
        for item in cls.progress_items():
            if item.identifier == identifier:
                return item

    @classmethod
    def get(cls, *, identifier: str = "") -> ProgressPropertyItem:
        ret = cls._get(identifier=identifier)
        if ret:
            ret.valid = True
            return ret

        if not cls._is_drawn:
            bpy.utils.register_class(progress.ProgressPropertyItem)
            cls._attrname = eval_unique_name(arr=WindowManager, prefix="bhq_", suffix="_progress")

            setattr(
                WindowManager,
                cls._attrname,
                CollectionProperty(type=progress.ProgressPropertyItem, options={'HIDDEN'})
            )
            STATUSBAR_HT_header.draw = cls._func_draw_progress
            _update_statusbar()

        cls._is_drawn = True
        ret: progress.ProgressPropertyItem = getattr(bpy.context.window_manager, cls._attrname).add()
        ret.identifier = identifier
        return ret

    @classmethod
    def complete(cls, *, identifier: str):
        item = cls._get(identifier=identifier)
        if item:
            item.valid = False

            for _ in cls.valid_progress_items():
                return
            cls.release_all()

    @classmethod
    def release_all(cls):
        """
        Видаляє всі індикатори прогресу і відновлює стандартне відображення рядку статусу.
        """
        import importlib
        if not cls._is_drawn:
            return

        assert (cls._attrname)
        delattr(WindowManager, cls._attrname)
        bpy.utils.unregister_class(progress.ProgressPropertyItem)

        importlib.reload(space_statusbar)
        STATUSBAR_HT_header.draw = space_statusbar.STATUSBAR_HT_header.draw
        _update_statusbar()

        cls._is_drawn = False
