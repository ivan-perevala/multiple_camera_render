# BlenderHQ addon base module.
# Copyright (C) 2022 Ivan Perevala (ivpe)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
if __debug__:
    from importlib import reload
# Зовнішній пакунок
# Цей пакунок
if __debug__:
    if '_' in locals():
        reload(utils_gpu)
        reload(utils_ui)
        reload(utils_wm)
        reload(reports)
    else:
        _ = None
        from . import utils_gpu
        from . import utils_ui
        from . import utils_wm
        from . import reports

from . utils_gpu import *
from . utils_ui import *
from . utils_wm import *
from . reports import *
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
    # utils_gpu._viewport_metrics
    "get_viewport_metrics",
    # utils_gpu._depthmap
    "get_depth_map",
    # utils_gpu._aa_base
    "AAPreset",
    "AABase",
    # utils_gpu._framebuffer_framework
    "Mode",
    "FrameBufferFramework",
    # utils_gpu._batch_preset
    "BatchPreset",
    # utils_gpu._draw_framework
    "DrawFramework",
    # utils_gpu._fxaa
    "FXAA",
    # utils_gpu._smaa
    "SMAA",

    # utils_ui._unique_name
    "eval_unique_name",
    # utils_ui._wrapped_text
    "eval_text_pixel_dimensions",
    "draw_wrapped_text",
    # utils_ui._developer_extras
    "developer_extras_poll",
    "template_developer_extras_warning",
    # utils_ui._progress
    "progress",
    # utils_ui._icons_cache
    "IconsCache",
    # utils_ui._preset
    "copy_default_presets_from",
    "template_preset",
    # utils_ui._localization
    "update_localization",
    "request_localization_from_file",

    # utils_wm
    "iter_areas",
    "iter_regions",
    "iter_windows_areas_regions",
    "iter_area_regions",
    "iter_area_spaces",
    "tag_redraw_all_regions",

    # reports
    "CONSOLE_ESC_SEQ",
    "AddonLogger",
)
