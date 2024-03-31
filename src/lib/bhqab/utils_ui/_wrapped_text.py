from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
# Зовнішній пакунок
# Цей пакунок
# Внутрішній пакунок
# Бібліотеки Blender
from mathutils import Vector
import blf
from bpy.app.translations import pgettext

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
        from bpy.types import UILayout, Context

__all__ = (
    "eval_text_pixel_dimensions",
    "draw_wrapped_text",
)


def eval_text_pixel_dimensions(*, fontid: int = 0, text: str = "") -> Vector:
    """
    Обчислює розмір тексту в пікселях з поточними налаштуваннями модуля ``blf``.

    :param fontid: Ідентифікатор шрифту, за замовчуванням ``0``.
    :type fontid: int, опційно
    :param text: Текст для обробки, за замовчуванням - пустий рядок.
    :type text: str, опційно
    :return: Висота і ширина тексту.
    :rtype: `mathutils.Vector`_
    """
    ret = Vector((0.0, 0.0))
    if not text:
        return ret

    is_single_char = bool(len(text) == 1)
    SINGLE_CHARACTER_SAMPLES = 100
    if is_single_char:
        text *= SINGLE_CHARACTER_SAMPLES

    ret.x, ret.y = blf.dimensions(fontid, text)

    if is_single_char:
        ret.x /= SINGLE_CHARACTER_SAMPLES

    return ret


def draw_wrapped_text(
        context: Context,
        layout: UILayout,
        *,
        text: str,
        text_ctxt: None | str = None,
) -> None:
    """
    Відображує текстовий блок, з автоматичний перенесенням рядків відповідно до ширини поточного регіону.

    :param context: Поточний контекст.
    :type context: `Context`_
    :param layout: Поточний користувацький інтерфейс.
    :type layout: `UILayout`_
    :param text: Текст для відображення.
    :type text: str
    """
    col = layout.column(align=True)

    if context.region.type == 'WINDOW':
        win_padding = 30
    elif context.region.type == 'UI':
        win_padding = 52
    else:
        win_padding = 52

    wrap_width = context.region.width - win_padding
    space_width = eval_text_pixel_dimensions(text=' ').x

    text = pgettext(text, text_ctxt)

    for line in text.split('\n'):
        num_characters = len(line)

        if not num_characters:
            col.separator()
            continue

        line_words = list((_, eval_text_pixel_dimensions(text=_).x) for _ in line.split(' '))
        num_line_words = len(line_words)
        line_words_last = num_line_words - 1

        sublines = [""]
        subline_width = 0.0

        for i in range(num_line_words):
            word, word_width = line_words[i]

            sublines[-1] += word
            subline_width += word_width

            next_word_width = 0.0
            if i < line_words_last:
                next_word_width = line_words[i + 1][1]

                sublines[-1] += ' '
                subline_width += space_width

            if subline_width + next_word_width > wrap_width:
                subline_width = 0.0
                if i < line_words_last:
                    sublines.append("")  # Add new subline.

        for subline in sublines:
            col.label(text=subline)
