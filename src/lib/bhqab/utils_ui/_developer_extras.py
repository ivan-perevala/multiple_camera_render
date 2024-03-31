from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
# Зовнішній пакунок
# Цей пакунок
from . _wrapped_text import draw_wrapped_text
# Внутрішній пакунок
# Бібліотеки Blender

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
        from bpy.types import Context, UILayout

__all__ = (
    "developer_extras_poll",
    "template_developer_extras_warning",
)

def developer_extras_poll(context: Context) -> bool:
    """
    Чи потрібно відобразити секцію користувацького інтерфейсу, яка призначена для розробки або налагодження.

    :param context: Поточний контекст.
    :type context: `Context`_
    :return: Позитивне значення означає що так, потрібно.
    :rtype: bool
    """
    return context.preferences.view.show_developer_ui


def template_developer_extras_warning(context: Context, layout: UILayout) -> None:
    """
    Шаблон для відображення попередження про те що ця секція користувацького інтерфейсу призначена виключно для розробки
    та налагодження.

    :param context: Поточний контекст.
    :type context: `Context`_
    :param layout: Поточний користувацький інтерфейс.
    :type layout: `UILayout`_
    """
    if developer_extras_poll(context):
        col = layout.column(align=True)
        scol = col.column(align=True)
        scol.alert = True
        scol.label(text="Warning", icon='INFO')
        text = "This section is intended for developers. You see it because " \
            "you have an active \"Developers Extras\" option in the Blender " \
            "user preferences."
        draw_wrapped_text(context, scol, text=text, text_ctxt='BHQAB_Preferences')

        col.prop(context.preferences.view, "show_developer_ui")

