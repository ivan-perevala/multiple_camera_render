# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from bpy.types import Object, Context

import bhqmain4 as bhqmain

log = logging.getLogger(__name__)
_err = log.error

if TYPE_CHECKING:
    from . chunk_main import Main


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

    def invoke(self, context):
        super().invoke(context)

        scene = context.scene

        self.frame_current = scene.frame_current
        self.render_filepath = scene.render.filepath
        self.camera_ob = scene.camera
        self.use_lock_interface = scene.render.use_lock_interface

        return bhqmain.InvokeState.SUCCESSFUL

    def cancel(self, context):
        super().cancel(context)

        scene = context.scene

        scene.frame_current = self.frame_current
        scene.render.filepath = self.render_filepath
        scene.render.use_lock_interface = self.use_lock_interface

        try:
            getattr(self.camera_ob, "name")
        except ReferenceError:
            _err("Initial camera was removed by user, it would not be restored")
        else:
            scene.camera = self.camera_ob

        return bhqmain.InvokeState.SUCCESSFUL
