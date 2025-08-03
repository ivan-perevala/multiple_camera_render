# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from bpy.types import Object, Context, TimelineMarker

import bhqmain4 as bhqmain

from . validate_id import validate_camera_object, validate_id
from . chunk_persistent_main import PersistentMain

log = logging.getLogger(__name__)
_err = log.error

if TYPE_CHECKING:
    from . chunk_main import Main


class Restore(bhqmain.MainChunk['Main', 'Context']):
    "Contains blend data which was modified during execution, so it can be restored."

    frame_current: int
    render_filepath: str
    camera_ob: None | Object
    use_lock_interface: bool
    marker_cameras: list[tuple[TimelineMarker, Object]]

    def __init__(self, main):
        super().__init__(main)

        self.frame_current = 0
        self.render_filepath = ""
        self.camera_ob = None
        self.use_lock_interface = False
        self.marker_cameras = []

    def invoke(self, context):
        super().invoke(context)

        scene = context.scene

        self.frame_current = scene.frame_current
        self.render_filepath = scene.render.filepath
        self.camera_ob = scene.camera
        self.use_lock_interface = scene.render.use_lock_interface
        self.marker_cameras = [(marker, marker.camera) for marker in scene.timeline_markers if marker.camera]

        return bhqmain.InvokeState.SUCCESSFUL

    def cancel(self, context):
        super().cancel(context)

        scene = context.scene

        for marker, camera in self.marker_cameras:
            if validate_id(marker, "frame"):
                if validate_id(camera):
                    marker.camera = camera
                else:
                    _err(f"Unable to restore camera for marker \"{marker.frame}\", invalid object")
            else:
                _err(f"Unable to restore marker camera for deleted marker")

        scene.frame_current = self.frame_current
        scene.render.filepath = self.render_filepath
        scene.render.use_lock_interface = self.use_lock_interface

        if validate_camera_object(self.camera_ob):
            scene.camera = self.camera_ob
        else:
            _err("Initial camera was removed by user, it would not be restored")

        if validate_camera_object(scene.camera):
            pmain = PersistentMain.get_instance()
            if pmain and pmain():
                pmain().per_camera.update_scene_properties_from_camera(scene=context.scene, cam=scene.camera.data)
        else:
            _err("There is no valid active camera to update scene properties at restore")

        return bhqmain.InvokeState.SUCCESSFUL
