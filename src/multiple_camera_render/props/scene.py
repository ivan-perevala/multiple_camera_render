# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging

from bpy.types import PropertyGroup, Context
from bpy.props import BoolProperty, EnumProperty

import bhqrprt4 as bhqrprt

from .. import icons
from .. import main

log = logging.getLogger(__name__)


class SceneProps(PropertyGroup, main.PersistentPerCamera.eval_scene_flag_properties()):
    cameras_usage: EnumProperty(
        items=[
            (
                'VISIBLE',
                "Visible",
                "Render from all visible cameras",
                icons.get_id('visible'),
                0
            ),
            (
                'SELECTED',
                "Selected",
                "Render only from selected cameras",
                icons.get_id('selected'),
                1
            )
        ],
        default='VISIBLE',
        options={'SKIP_SAVE'},
        name="Cameras Usage",
        description="Which cameras to use for rendering",
        update=bhqrprt.update_log_setting_changed(log, "cameras_usage"),
    )

    direction: EnumProperty(
        name="Direction",
        items=(
            (
                'CLOCKWISE',
                "Clockwise",
                "",
                icons.get_id('clockwise'),
                0
            ),
            (
                'COUNTER',
                "Counter",
                "",
                icons.get_id('counter'),
                1
            ),
        ),
        default='CLOCKWISE',
        options={'SKIP_SAVE'},
        description=(
            "The direction in which the cameras will change during the rendering of the sequence (Starting from the "
            "current camera of the scene)"
        ),
        update=bhqrprt.update_log_setting_changed(log, "direction"),
    )

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
            pmain().select_camera.conditional_handler_register(self)

    select_camera: BoolProperty(
        update=_select_camera_update,
        default=False,
        name="Set Selected as Active Camera",
        description="Select camera would make it scene active",
        options={'SKIP_SAVE'},
    )
