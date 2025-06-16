# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy

from . import handlers

functions = {
    # Render handlers:
    "render_init": handlers.render.render_init,
    "render_stats": handlers.render.render_stats,
    "render_pre": handlers.render.render_pre,
    "render_post": handlers.render.render_post,
    "render_complete": handlers.render.render_complete,
    "render_write": handlers.render.render_write,
    "render_cancel": handlers.render.render_cancel,

    # Scene frame:
    "frame_change_pre": handlers.scene_frame.frame_change_pre,
    "frame_change_post": handlers.scene_frame.frame_change_post,


    # Animation playback:
    "animation_playback_pre": handlers.playback.animation_playback_pre,
    "animation_playback_post": handlers.playback.animation_playback_post,

    # Composite:
    "composite_pre": handlers.composite.composite_pre,
    "composite_post": handlers.composite.composite_post,
    "composite_cancel": handlers.composite.composite_cancel,

    # Dependency graph:
    "depsgraph_update_pre": handlers.depsgraph.dg.depsgraph_update_pre,
    "depsgraph_update_post": handlers.depsgraph.dg.depsgraph_update_post,
}


def register():
    for handler_name, func in functions.items():
        handler: list = getattr(bpy.app.handlers, handler_name)
        if func not in handler:
            handler.append(func)


def unregister():
    for handler_name, func in functions.items():
        handler: list = getattr(bpy.app.handlers, handler_name)
        if func not in handler:
            handler.remove(func)
