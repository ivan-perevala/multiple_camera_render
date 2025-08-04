# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


def __reload_submodules(lc):
    from importlib import reload

    if "options_panel" in lc:
        reload(options_panel)
    if "per_camera_panel" in lc:
        reload(per_camera_panel)
    if "time_menu_header_draw" in lc:
        reload(time_menu_header_draw)
    if "topbar_menu_render_draw" in lc:
        reload(topbar_menu_render_draw)
    if "ui_menu_button_context_draw" in lc:
        reload(ui_menu_button_context_draw)
    if "view_3d_header_draw" in lc:
        reload(view_3d_header_draw)


__reload_submodules(locals())

from . import options_panel
from . import per_camera_panel
from . import time_menu_header_draw
from . import topbar_menu_render_draw
from . import ui_menu_button_context_draw
from . import view_3d_header_draw


from . options_panel import MCR_PT_options
from . per_camera_panel import MCR_PT_scene_use_per_camera
from . time_menu_header_draw import additional_TIME_MT_marker_draw
from . topbar_menu_render_draw import additional_TOPBAR_MT_render_draw
from . ui_menu_button_context_draw import additional_UI_MT_button_context_menu
from . view_3d_header_draw import additional_VIEW3D_HT_header_draw


__all__ = (
    # file://./options_panel.py
    "MCR_PT_options",
    # file://./per_camera_panel.py
    "MCR_PT_scene_use_per_camera",
    # file://./time_menu_header_draw.py
    "additional_TIME_MT_marker_draw",
    # file://./topbar_menu_render_draw.py
    "additional_TOPBAR_MT_render_draw",
    # file://./ui_menu_button_context_draw.py
    "additional_UI_MT_button_context_menu",
    # file://./view_3d_header_draw.py
    "additional_VIEW3D_HT_header_draw",
)
