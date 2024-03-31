from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
# Зовнішній пакунок
# Цей пакунок
# Внутрішній пакунок
# Бібліотеки Blender
import bpy

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

__all__ = (
    "update_localization",
    "request_localization_from_file",
)

def update_localization(*, module: str, langs: dict):
    """
    Метод оновлення реєстрації локалізації в реальному часі.

    :param module: Назва модулю додатку.
    :type module: str
    :param langs: Словник.
    :type langs: dict
    """
    try:
        bpy.app.translations.unregister(module)
    except RuntimeError:
        pass
    else:
        bpy.app.translations.register(module, langs)


def request_localization_from_file(*, module: str, langs: dict, msgctxt: str, src: str, dst: dict[str, str]):
    """
    Метод оновлення локалізації додатку з файлів. Може бути корисним наприклад для README.txt файлів.

    :param module: Назва модулю додатку.
    :type module: str
    :param langs: Словник.
    :type langs: dict
    :param msgctxt: Контекст перекладу.
    :type msgctxt: str
    :param src: Шлях до файлу що містить оригінальні дані.
    :type src: str
    :param dst: Словник у форматі: Назва локалізації - шлях до файлу перекладу.
    :type dst: dict[str, str]
    :return: Текст оригіналу.
    :rtype: str
    """
    for lang, translations in langs.items():
        if lang in dst:
            for item in translations.keys():
                if item[0] == msgctxt:
                    return item[1]

    src_data = ""
    with open(src, 'r', encoding='utf-8') as src_file:
        src_data = src_file.read()
        for dst_locale, dst_filename in dst.items():
            with open(dst_filename, 'r', encoding='utf-8') as dst_file:
                if dst_locale not in langs:
                    langs[dst_locale] = dict()
                langs[dst_locale][(msgctxt, src_data)] = dst_file.read()

    update_localization(module=module, langs=langs)
    return src_data

