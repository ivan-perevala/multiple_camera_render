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
from gpu.types import GPUTexture

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
        from gpu.types import GPUFrameBuffer

__all__ = ("get_depth_map",)


def get_depth_map(*, depth_format: str = 'DEPTH_COMPONENT32F') -> GPUTexture:
    """
    Текстура глибини в поточному буфері кадру.

    :return: Текстура типу ``DEPTH_COMPONENT32F`` що має розмір переглядача.
    :rtype: `GPUTexture`_
    """
    fb: GPUFrameBuffer = gpu.state.active_framebuffer_get()
    return GPUTexture(
        gpu.state.viewport_get()[2:],
        data=fb.read_depth(*fb.viewport_get()), format=depth_format
    )
