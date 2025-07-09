# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging

from bpy.types import PropertyGroup, Context
from bpy.props import BoolProperty

import bhqrprt4 as bhqrprt

from .. import main

log = logging.getLogger(__name__)

from .. import icons


class SceneProps(PropertyGroup, main.CameraProperties, main.PersistentPerCamera.eval_scene_flag_properties()):
    keep_frame_in_filepath: BoolProperty(
        default=True,
        options={'SKIP_SAVE'},
        name="Keep Frame Number",
        description="Write frame number even if not rendering animation",
        update=bhqrprt.update_log_setting_changed(log, "keep_frame_in_filepath"),
    )

    _update_log_select_camera = bhqrprt.update_log_setting_changed(log, "select_camera")

    def _select_camera_update(self, context: Context):
        self._update_log_select_camera(context)

        pmain = main.PersistentMain.get_instance()
        if pmain and pmain():
            pmain().select_camera.conditional_handler_register(scene_props=self)

    select_camera: BoolProperty(
        update=_select_camera_update,
        default=False,
        name="Set Selected as Active Camera",
        description="Select camera would make it scene active",
        options={'SKIP_SAVE'},
    )
