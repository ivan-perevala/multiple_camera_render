# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging

from bpy.types import Operator
from bpy.props import BoolProperty

import bhqrprt4 as bhqrprt

from . chunk_persistent_per_camera import PersistentPerCamera

log = logging.getLogger(__name__)


class SCENE_OT_mcr_per_camera_enable(Operator):
    bl_idname = "scene.mcr_per_camera_enable"
    bl_label = "Enable"
    bl_options = {'REGISTER'}

    disable: BoolProperty(
        default=False,
        options={'SKIP_SAVE'},
    )

    @classmethod
    def poll(cls, context):
        per_camera = PersistentPerCamera.get_instance()
        return per_camera and per_camera()

    @classmethod
    def description(cls, context, properties):
        if properties.get('disable'):
            return "Disable all flags, so nothing would be captured"
        else:
            return "Enable all flags, capture everything in the list"

    @bhqrprt.operator_report(log)
    def execute(self, context):
        per_camera = PersistentPerCamera.get_instance()

        if per_camera and per_camera():
            per_camera().set_scene_flags_no_update(scene=context.scene, state=not self.disable)

        return {'FINISHED'}
