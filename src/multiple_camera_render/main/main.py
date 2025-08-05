# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

import bpy   # pyright: ignore [reportMissingModuleSource]
from bpy.types import Operator   # pyright: ignore [reportMissingModuleSource]
from bpy.props import BoolProperty   # pyright: ignore [reportMissingModuleSource]

import bhqmain4 as bhqmain
import bhqrprt4 as bhqrprt

from . chunk_main import Main
log = logging.getLogger(__name__)
_err = log.error


class RENDER_OT_multiple_camera_render(Operator):
    bl_idname = "render.multiple_camera_render"
    bl_label = "Multiple Camera Render"

    preview: BoolProperty(default=False, options={'HIDDEN', 'SKIP_SAVE'})  # pyright: ignore [reportInvalidTypeForm]
    animation: BoolProperty(default=False, options={'HIDDEN', 'SKIP_SAVE'})  # pyright: ignore [reportInvalidTypeForm]
    quit: BoolProperty(default=False, options={'HIDDEN', 'SKIP_SAVE'})  # pyright: ignore [reportInvalidTypeForm]

    @bhqrprt.operator_report(log)
    def invoke(self, context, event):
        main = Main.get_instance()
        if main and main():
            return {'CANCELLED'}

        main = Main.create()
        main().animation = self.animation
        main().preview = self.preview
        main().quit = self.quit

        if main().invoke(context) == bhqmain.InvokeState.SUCCESSFUL:
            wm = context.window_manager
            wm.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            bhqrprt.report_and_log(log, self, level=logging.WARNING, message="Failed to invoke render")
            return {'CANCELLED'}

    def modal(self, context, event):
        main = Main.get_instance()
        if not (main and main()):
            return {'CANCELLED'}

        return main().modal(context, event)

    @bhqrprt.operator_report(log)
    def execute(self, context):
        if not bpy.app.background:
            _err("Can be executed directly only in background mode")
            return {'CANCELLED'}
        if self.preview:
            _err("Preview not available in background mode")
            return {'CANCELLED'}

        main = Main.create()
        main().animation = self.animation

        if main().invoke(context) != bhqmain.InvokeState.SUCCESSFUL:
            bhqrprt.report_and_log(
                log, self,
                level=logging.WARNING,
                message="Failed to invoke multiple camera render in background mode, see previous logs."
            )
            return {'CANCELLED'}

        while (main := Main.get_instance()):
            main().modal(context, None)

        return {'FINISHED'}

    @classmethod
    def description(cls, context, properties: RENDER_OT_multiple_camera_render):
        if properties.animation:
            if properties.preview:
                return "Preview animation process. Not actual render would be performed"
            return "Render animation sequentially from multiple cameras"
        else:
            if properties.preview:
                return "Preview camera order. Not actual render would be performed"
            return "Sequentional render of current frame from multiple cameras"
