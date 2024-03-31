# Multiple Camera Render addon.
# Copyright (C) 2020 Vladlen Kuzmin (ssh4), Ivan Perevala (ivpe)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

bl_info = {
    "name": "Multiple Camera Render",
    "author": "Vladlen Kuzmin (ssh4), Ivan Perevala (ivpe)",
    "version": (3, 6, 3),
    "blender": (3, 6, 3),
    "description": "Sequential rendering from multiple cameras",
    "location": "Tool settings > Camera Render",
    "support": 'COMMUNITY',
    "category": "Render",
    "doc_url": "https://github.com/BlenderHQ/multiple_camera_render",
}

import os
import time

dt = time.time()

ADDON_PKG = __package__.split('.')[0]
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

from . lib import bhqab


class Reports(bhqab.reports.AddonLogger):
    pass


Reports.initialize(
    logger_name=bl_info["name"],
    directory=os.path.join(os.path.dirname(__file__), "logs"),
    max_num_logs=30,
)

log = Reports.log


def get_addon_preferences(context: Context) -> props.pref.Preferences:
    return context.preferences.addons[ADDON_PKG].preferences


if "bpy" in locals():
    from importlib import reload

    reload(icons)
    reload(props)
    reload(main)
    reload(langs)
else:
    from . import icons
    from . import props
    from . import main
    from . import langs

import bpy
from bpy.types import (
    Context,
    Menu,
)
import bpy.app.handlers
import bpy.app.translations
from bpy.app.handlers import persistent

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . props import Scene
    from . props.scene import SceneProps

log.debug("Sub-module import time: {:.6f} second(s)".format(time.time() - dt))


@persistent
def handler_load_post(_=None):
    log.debug("Loaded with settings:").push_indent()

    context = bpy.context

    log.debug("Preferences:").push_indent()

    addon_pref = get_addon_preferences(context)
    Reports.log_settings(item=addon_pref)

    log.pop_indent()

    log.debug("Scene:").push_indent()

    scene: Scene = context.scene
    scene_props: SceneProps = scene.mcr

    Reports.log_settings(item=scene_props)

    log.pop_indent().pop_indent()


_application_handlers = (
    (bpy.app.handlers.render_init, main.Main.handler_render_init),
    (bpy.app.handlers.render_complete, main.Main.handler_render_complete),
    (bpy.app.handlers.render_cancel, main.Main.handler_render_cancel),
    (bpy.app.handlers.render_write, main.Main.handler_render_write),
    (bpy.app.handlers.frame_change_pre, main.Main.handler_frame_change_pre),
    (bpy.app.handlers.load_post, handler_load_post),
)


def ui_draw(self: Menu, context: Context):
    layout = self.layout
    scene: Scene = context.scene
    scene_props: SceneProps = scene.mcr

    layout.separator()

    col = layout.column(align=True)
    col.prop(scene_props, "use_multiple_camera_render")
    scol = col.column(align=True)
    scol.enabled = scene_props.use_multiple_camera_render
    scol.prop(scene_props, "use_viewport")


def register():
    props.register()

    for handler, callback in _application_handlers:
        handler.append(callback)

    bpy.types.TOPBAR_MT_render.append(ui_draw)

    bpy.app.translations.register(ADDON_PKG, langs.LANGS)


def unregister():
    bpy.app.translations.unregister(ADDON_PKG)

    bpy.types.TOPBAR_MT_render.remove(ui_draw)

    for handler, callback in _application_handlers:
        handler.remove(callback)

    props.unregister()
