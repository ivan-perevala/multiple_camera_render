from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
import random
import string
from typing import Iterable
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


__all__ = ("eval_unique_name",)


def eval_unique_name(*, arr: Iterable, prefix: str = "", suffix: str = "") -> str:
    """
    Створює випадкову унікальну назву для нового елемента масиву з зазначеним префіксом і суфіксом. Може бути
    використано для ``bpy.data`` і ``bpy.ops`` для реєстрації тимчасових блоків даних.

    :param arr: Масив для якого повинна бути згенерована унікальна назва.
    :type arr: Iterable
    :param prefix: Префікс назви. Якщо масивом є ``bpy.ops`` то префікс буде поміщено в
        ``bpy.ops.[prefix][випадкова назва]`` і результатом виконання функції буде поле ``bl_idname`` оператора у
        форматі ``[prefix][випадкова назва][suffix]``
    :type prefix: str, опційно
    :param suffix: Суфікс назви, за замовчуванням ""
    :type suffix: str, опційно
    :return: Унікальна назва.
    :rtype: str
    """
    if arr is bpy.ops:
        ret = prefix + '.' + str().join(random.sample(string.ascii_lowercase, k=10)) + suffix
        if isinstance(getattr(getattr(arr, ret, None), "bl_idname", None), str):
            return eval_unique_name(arr=arr, prefix=prefix, suffix=suffix)
        return ret
    else:
        ret = prefix + str().join(random.sample(string.ascii_letters, k=5)) + suffix
        if hasattr(arr, ret) or (isinstance(arr, Iterable) and ret in arr):
            return eval_unique_name(arr=arr, prefix=prefix, suffix=suffix)
        return ret
