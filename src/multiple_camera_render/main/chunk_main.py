# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging

import bpy
from bpy.types import Context, Event

import bhqmain

from . chunk_restore import Restore
from . chunk_timers import Timers
from . chunk_render import Render, RenderStatus

log = logging.getLogger(__name__)


class Main(bhqmain.MainChunk['Main', 'Context']):
    chunks = {
        "restore": Restore,
        "timers": Timers,
        "render": Render,
    }

    restore: Restore
    timers: Timers
    render: Render

    preview: bool
    animation: bool

    def __init__(self, main):
        super().__init__(main)

        self.preview = False
        self.animation = False

    def modal(self, context: Context, event: Event):
        if event.type.startswith('TIMER'):
            if self.preview or (not bpy.app.is_job_running('RENDER')):
                if self.render.status == RenderStatus.NEED_LAUNCH:
                    self.render.launch_render(context)
            if self.render.status == RenderStatus.COMPLETE:
                if self.cancel(context) == bhqmain.InvokeState.SUCCESSFUL:
                    return {'FINISHED'}
                else:
                    return {'CANCELLED'}
        if self.preview:
            return {'PASS_THROUGH'}
        else:
            return {'RUNNING_MODAL'}
