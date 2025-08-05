# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

import bpy   # pyright: ignore [reportMissingModuleSource]
from bpy.types import Context, Event   # pyright: ignore [reportMissingModuleSource]

import bhqmain4 as bhqmain

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
    quit: bool

    def __init__(self, main):
        super().__init__(main)

        self.preview = False
        self.animation = False
        self.quit = False

    def modal(self, context: Context, event: None | Event):
        if event is None or event.type.startswith('TIMER'):
            match self.render.status:

                case RenderStatus.NEED_LAUNCH:
                    if not self.render.launch_render(context):
                        log.warning("Unable to launch render")
                        return {'CANCELLED'}

                case RenderStatus.COMPLETE:
                    if self.cancel(context) == bhqmain.InvokeState.SUCCESSFUL:
                        if self.quit:
                            bpy.ops.wm.quit_blender()
                        return {'FINISHED'}
                    else:
                        return {'CANCELLED'}

                case RenderStatus.CANCELLED:
                    if self.cancel(context) == bhqmain.InvokeState.SUCCESSFUL:
                        return {'FINISHED'}
                    else:
                        return {'CANCELLED'}

        if self.preview:
            if event.type == 'ESC' and event.value == 'PRESS':
                if self.cancel(context) != bhqmain.InvokeState.SUCCESSFUL:
                    log.warning("Unable to properly cancel chunks at user cancelled preview")
                return {'CANCELLED'}
            return {'PASS_THROUGH'}
        else:
            return {'RUNNING_MODAL'}
