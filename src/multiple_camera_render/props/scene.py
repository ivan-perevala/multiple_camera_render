# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

from bpy.types import PropertyGroup, Context, Scene
from bpy.props import BoolProperty, EnumProperty

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
    )  # pyright: ignore [reportInvalidTypeForm]

    _update_log_select_camera = bhqrprt.update_log_setting_changed(log, "select_camera")

    def _select_camera_update(self: PropertyGroup, context: Context):
        self._update_log_select_camera(context)

        pmain = main.PersistentMain.get_instance()
        if pmain and pmain():
            scene: Scene = self.id_data
            pmain().select_camera.conditional_handler_register(scene)

    select_camera: BoolProperty(
        update=_select_camera_update,
        default=False,
        name="Set Selected as Active Camera",
        description="Select camera would make it scene active",
        options={'SKIP_SAVE'},
    )  # pyright: ignore [reportInvalidTypeForm]

    def _frame_usage_items(self, context: Context):
        return (
            (
                main.FrameUsage.CURRENT.name,
                "Current",
                "Render current frame from multiple cameras",
                icons.get_id('frame_current'),
                main.FrameUsage.CURRENT.value
            ),
            None,
            (
                main.FrameUsage.MARKERS_IN_RANGE.name,
                "Markers in Range",
                "Render from multiple cameras at each marker in scene frame range",
                icons.get_id('frame_markers_in_range_reverse' if self.frame_usage_reverse else 'frame_markers_in_range'),
                main.FrameUsage.MARKERS_IN_RANGE.value
            ),
            (
                main.FrameUsage.SELECTED_MARKERS.name,
                "Selected Markers",
                "Render from multiple cameras at each selected marker",
                icons.get_id('frame_selected_markers_reverse' if self.frame_usage_reverse else 'frame_selected_markers'),
                main.FrameUsage.SELECTED_MARKERS.value
            )
        )

    frame_usage: EnumProperty(
        items=_frame_usage_items,
        options={'SKIP_SAVE'},
        default=main.FrameUsage.CURRENT.value,
        name="Frame Usage",
        description="Which frames to use for sequential rendering. Does nothing for animation rendering"
    )  # pyright: ignore [reportInvalidTypeForm]

    frame_usage_reverse: BoolProperty(
        default=False,
        options={'SKIP_SAVE'},
        name="Reverse",
        description="Iterate markers in reverse"
    )  # pyright: ignore [reportInvalidTypeForm]
