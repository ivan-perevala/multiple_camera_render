# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

from bpy.types import Operator   # pyright: ignore [reportMissingModuleSource]
from bpy.props import BoolProperty   # pyright: ignore [reportMissingModuleSource]

import bhqrprt4 as bhqrprt

from . chunk_persistent_main import PersistentMain

log = logging.getLogger(__name__)


class SCENE_OT_mcr_per_camera_enable(Operator):
    bl_idname = "scene.mcr_per_camera_enable"
    bl_label = "Enable"
    bl_options = {'REGISTER'}

    disable: BoolProperty(
        default=False,
        options={'SKIP_SAVE'},
    )   # pyright: ignore [reportInvalidTypeForm]

    @classmethod
    def poll(cls, context):
        pmain = PersistentMain.get_instance()
        return pmain and pmain()

    @classmethod
    def description(cls, context, properties):
        if properties.get('disable'):
            return "Disable all flags, so nothing would be captured"
        else:
            return "Enable all flags, capture everything in the list"

    @bhqrprt.operator_report(log)
    def execute(self, context):
        pmain = PersistentMain.get_instance()

        if pmain and pmain():
            pmain().per_camera.set_scene_flags_no_update(scene=context.scene, state=not self.disable)

        return {'FINISHED'}
