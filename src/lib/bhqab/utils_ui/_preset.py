from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
import os
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
        from bpy.types import UILayout, Menu

__all__ = (
    "copy_default_presets_from",
    "template_preset",
)


def copy_default_presets_from(*, src_root: str):
    """
    Створює копії файлів шаблонів з директорії додатку до директорії де Blender зберігає шаблони.

    :param src_root: Директорія що містить файли шаблонів.
    :type src_root: str
    """
    for root, _dir, files in os.walk(src_root):
        for filename in files:
            rel_dir = os.path.relpath(root, src_root)
            src_fp = os.path.join(root, filename)

            tar_dir = bpy.utils.user_resource('SCRIPTS', path=os.path.join("presets", rel_dir), create=True)
            if not tar_dir:
                print("Failed to create presets path")
                return

            tar_fp = os.path.join(tar_dir, filename)

            with open(src_fp, 'r', encoding="utf-8") as src_file, open(tar_fp, 'w', encoding="utf-8") as tar_file:
                tar_file.write(src_file.read())


def template_preset(layout: UILayout, *, menu: Menu, operator: str) -> None:
    """
    Метод відображення шаблонів в користувацькому інтерфейсі.

    :param layout: Поточний користувацький інтерфейс.
    :type layout: `UILayout`_
    :param menu: Клас меню що буде використано для відображення списку шаблонів.
    :type menu: 'Menu'_
    :param operator: ``bl_idname`` оператора для створення і видалення шаблонів.
    :type operator: str
    """
    row = layout.row(align=True)
    row.use_property_split = False

    row.menu(menu=menu.__name__, text=menu.bl_label)
    row.operator(operator=operator, text="", icon='ADD')
    row.operator(operator=operator, text="", icon='REMOVE').remove_active = True
