# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

import logging
import numpy as np

from bpy.types import Operator
from bpy.props import IntProperty, BoolProperty

import bhqrprt4 as bhqrprt

from . clockwise_iter import ClockwiseCameraIterator, CameraOrder, CameraUsage, CameraProperties

log = logging.getLogger(__name__)


class MARKER_create_from_cameras(Operator, CameraProperties):
    bl_idname = "marker.create_from_cameras"
    bl_label = "Markers From Cameras"
    bl_options = {'REGISTER', 'UNDO'}

    step: IntProperty(
        default=1,
        min=1,
        options={'HIDDEN', 'SKIP_SAVE'},
        name="Step",
        description="Step between markers"
    )

    clear_range: BoolProperty(
        default=False,
        options={'HIDDEN', 'SKIP_SAVE'},
        name="Clear Range",
        description="Clear existing markers within range"
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        layout.prop(self, "step")
        layout.prop(self, "clear_range")

        layout.separator(type='LINE')

        self.draw_camera_usage_properties(layout)

    @bhqrprt.operator_report(log)
    def execute(self, context):
        scene = context.scene

        camera_iterator = ClockwiseCameraIterator(
            context,
            usage=CameraUsage[self.usage],
            order=CameraOrder[self.order],
        )

        if not len(camera_iterator):
            bhqrprt.report_and_log(
                log, self,
                level=logging.WARNING,
                message="Missing cameras to create markers from",
            )
            return {'CANCELLED'}

        if self.reverse:
            camera_iterator = reversed(camera_iterator)

        used_frames = np.empty(len(scene.timeline_markers), dtype=np.int32)
        scene.timeline_markers.foreach_get('frame', used_frames)
        existing_map = dict(zip(used_frames, scene.timeline_markers))
        initial_frame = scene.frame_current

        num_removed = 0

        # Clear existing markers within frame range.
        if self.clear_range:
            start = scene.frame_current
            end = start + self.step * len(camera_iterator)

            should_remove = used_frames[np.logical_and(used_frames >= start, end >= used_frames)]

            num_removed += len(should_remove)

            for i in should_remove:
                scene.timeline_markers.remove(existing_map[i])
                del existing_map[i]

        # Create camera markers.
        for i, ob in enumerate(camera_iterator):
            frame = initial_frame + (self.step * i)

            if existing_marker := existing_map.get(frame):
                scene.timeline_markers.remove(existing_marker)
                num_removed += 1

            marker = scene.timeline_markers.new(name=ob.name, frame=frame)
            marker.camera = ob

        num_created = i + 1

        if num_removed:
            bhqrprt.report_and_log(
                log, self,
                level=logging.INFO,
                message="Created {_num_created} markers, removed {_num_replaced} overlapping",
                _num_created=num_created,
                _num_replaced=num_removed,
            )
        else:
            bhqrprt.report_and_log(
                log, self,
                level=logging.INFO,
                message="Created {_num_created} markers",
                _num_created=num_created,
            )

        return {'FINISHED'}
