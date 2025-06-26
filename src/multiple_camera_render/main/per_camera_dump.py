# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging

from bpy.types import Operator

import bhqrprt4 as bhqrprt

from . chunk_persistent_per_camera import PersistentPerCamera

log = logging.getLogger(__name__)


class OBJECT_OT_per_camera_dump(Operator):
    bl_idname = "object.per_camera_dump"
    bl_label = "Current Settings to Selected Cameras"
    bl_description = (
        "Apply current per camera scene data to selected camera objects. "
        "Only selected scene flags would be applied."
    )
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        for ob in context.selected_objects:
            if ob.type == 'CAMERA':
                return True
        return False

    @bhqrprt.operator_report(log)
    def execute(self, context):
        scene = context.scene

        num_processed = 0

        for ob in context.selected_objects:
            if ob.type == 'CAMERA':
                PersistentPerCamera.dump_scene_properties_to_camera(scene, ob.data)
                num_processed += 1

        bhqrprt.report_and_log(
            log, self,
            level=logging.INFO,
            message="Applied current settings to {num_processed} camera object(s)",
            num_processed=num_processed,
        )

        return {'FINISHED'}
