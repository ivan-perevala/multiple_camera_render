# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

from bpy.types import Operator   # pyright: ignore [reportMissingModuleSource]

import bhqrprt4 as bhqrprt

from . chunk_persistent_per_camera import PersistentPerCamera

log = logging.getLogger(__name__)


class OBJECT_OT_per_camera_clear(Operator):
    bl_idname = "object.per_camera_clear"
    bl_label = "Clear Settings for Selected Cameras"
    bl_description = "Clear all per-camera settings for selected cameras"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        for ob in context.selected_objects:
            if ob.type == 'CAMERA':
                return True
        return False

    def execute(self, context):
        num_processed = 0

        for ob in context.selected_objects:
            if ob.type == 'CAMERA':
                PersistentPerCamera.clear_per_camera_data(ob.data)
                num_processed += 1

        bhqrprt.report_and_log(
            log, self,
            level=logging.INFO,
            message="Cleared all per-camera settings for {num_processed} camera object(s)",
            num_processed=num_processed,
        )

        return {'FINISHED'}
