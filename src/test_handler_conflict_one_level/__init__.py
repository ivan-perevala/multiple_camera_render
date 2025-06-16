# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy


# Render handlers:
def render_init(*args, **kwargs):
    pass


def render_stats(*args, **kwargs):
    pass


def render_pre(*args, **kwargs):
    pass


def render_post(*args, **kwargs):
    pass


def render_complete(*args, **kwargs):
    pass


def render_write(*args, **kwargs):
    pass


def render_cancel(*args, **kwargs):
    pass


# Scene frame:
def frame_change_pre(*args, **kwargs):
    pass


def frame_change_post(*args, **kwargs):
    pass


# Animation playback:
def animation_playback_pre(*args, **kwargs):
    pass


def animation_playback_post(*args, **kwargs):
    pass


# Composite:
def composite_pre(*args, **kwargs):
    pass


def composite_post(*args, **kwargs):
    pass


def composite_cancel(*args, **kwargs):
    pass


# Dependency graph:
def depsgraph_update_post(*args, **kwargs):
    pass


def depsgraph_update_pre(*args, **kwargs):
    pass


functions = {
    # Render handlers:
    "render_init": render_init,
    "render_stats": render_stats,
    "render_pre": render_pre,
    "render_post": render_post,
    "render_complete": render_complete,
    "render_write": render_write,
    "render_cancel": render_cancel,

    # Scene frame:
    "frame_change_pre": frame_change_pre,
    "frame_change_post": frame_change_post,


    # Animation playback:
    "animation_playback_pre": animation_playback_pre,
    "animation_playback_post": animation_playback_post,

    # Composite:
    "composite_pre": composite_pre,
    "composite_post": composite_post,
    "composite_cancel": composite_cancel,

    # Dependency graph:
    "depsgraph_update_pre": depsgraph_update_pre,
    "depsgraph_update_post": depsgraph_update_post,
}


def register():
    for handler_name, func in functions.items():
        handler: list = getattr(bpy.app.handlers, handler_name)
        if func not in handler:
            handler.append(func)


def unregister():
    for handler_name, func in functions.items():
        handler: list = getattr(bpy.app.handlers, handler_name)
        if func in handler:
            handler.remove(func)
