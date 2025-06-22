# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import bpy
from bpy.types import Object, Context

import bhqmain4 as bhqmain

from . validate_id import validate_camera_object

log = logging.getLogger(__name__)
_err = log.error

if TYPE_CHECKING:
    from . chunk_main import Main


CONFLICTING_HANDLERS = (
    # Render handlers:
    "render_init",
    "render_stats",
    "render_pre",
    "render_post",
    "render_complete",
    "render_write",
    "render_cancel",

    # Scene frame:
    "frame_change_pre",
    "frame_change_post",

    # Animation playback:
    "animation_playback_pre",
    "animation_playback_post",

    # Composite:
    "composite_pre",
    "composite_post",
    "composite_cancel",

    # Dependency graph:
    "depsgraph_update_post",
    "depsgraph_update_pre",
)
"Handlers which may lead to addon conflicting with other addons."


class Restore(bhqmain.MainChunk['Main', 'Context']):
    "Contains blend data which was modified during execution, so it can be restored."

    frame_current: int
    render_filepath: str
    camera_ob: None | Object
    use_lock_interface: bool
    handler_callbacks: dict[str, list]

    def __init__(self, main):
        super().__init__(main)

        self.frame_current = 0
        self.render_filepath = ""
        self.camera_ob = None
        self.use_lock_interface = False

    def _capture_handlers(self):
        self.handler_callbacks = {
            handler_name: functions[:] for handler_name in CONFLICTING_HANDLERS
            if (functions := getattr(bpy.app.handlers, handler_name, None))
        }

    def _restore_handlers(self):
        for handler_name, functions in self.handler_callbacks.items():
            getattr(bpy.app.handlers, handler_name)[:] = functions

    def invoke(self, context):
        super().invoke(context)

        scene = context.scene

        self.frame_current = scene.frame_current
        self.render_filepath = scene.render.filepath
        self.camera_ob = scene.camera
        self.use_lock_interface = scene.render.use_lock_interface
        self._capture_handlers()

        return bhqmain.InvokeState.SUCCESSFUL

    def cancel(self, context):
        super().cancel(context)

        scene = context.scene

        scene.frame_current = self.frame_current
        scene.render.filepath = self.render_filepath
        scene.render.use_lock_interface = self.use_lock_interface

        if validate_camera_object(self.camera_ob):
            scene.camera = self.camera_ob
        else:
            _err("Initial camera was removed by user, it would not be restored")

        self._restore_handlers()

        return bhqmain.InvokeState.SUCCESSFUL
