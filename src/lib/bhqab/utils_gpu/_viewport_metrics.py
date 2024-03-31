from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
# Зовнішній пакунок
# Цей пакунок
# Внутрішній пакунок
# Бібліотеки Blender
import gpu
from mathutils import Vector

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

__all__ = ("get_viewport_metrics",)


def get_viewport_metrics() -> Vector:
    """
    Одиниці виміру поточного переглядача у вигляді вектора.

    :return: x = ``1.0 / ширину``, y = ``1.0 / висоту``, z = ``ширина``, w = ``висота``
    :rtype: `Vector`_
    """
    viewport = gpu.state.viewport_get()
    w, h = viewport[2], viewport[3]
    return Vector((1.0 / w, 1.0 / h, w, h))
