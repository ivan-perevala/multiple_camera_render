"""
Утиліти для роботи з відображенням у 2D/3D переглядачах.
"""

from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
if __debug__:
    from importlib import reload
# Зовнішній пакунок
if __debug__:
    if '_' in locals():
        reload(_viewport_metrics)
        reload(_depthmap)
        reload(_aa_base)
        reload(_framebuffer_framework)
        reload(_batch_preset)
        reload(_draw_framework)
        reload(_fxaa)
        reload(_smaa)
    else:
        _ = None
        from . import _viewport_metrics
        from . import _depthmap
        from . import _aa_base
        from . import _framebuffer_framework
        from . import _batch_preset
        from . import _draw_framework
        from . import _fxaa
        from . import _smaa

from . _viewport_metrics import *
from . _depthmap import *
from . _aa_base import *
from . _framebuffer_framework import *
from . _batch_preset import *
from . _draw_framework import *
from . _fxaa import *
from . _smaa import *
# Цей пакунок

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
        pass

__all__ = (
    # _viewport_metrics
    "get_viewport_metrics",

    # _depthmap
    "get_depth_map",

    # _aa_base
    "AAPreset",
    "AABase",

    # _framebuffer_framework
    "Mode",
    "FrameBufferFramework",

    # _batch_preset
    "BatchPreset",

    # _draw_framework
    "DrawFramework",

    # _fxaa
    "FXAA",

    # _smaa
    "SMAA",
)
