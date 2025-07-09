# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

import math
import numpy as np
from enum import auto, IntEnum
from typing import TYPE_CHECKING

from bpy.types import Object, Context, UILayout
from bpy.props import BoolProperty, EnumProperty
from mathutils import Vector

from . validate_id import validate_camera_object
from .. import icons

if TYPE_CHECKING:
    import numpy.typing as npt


class ClockwiseIterator:
    "Clockwise iterator, loops from and to specified index of array."

    array: np.ndarray[Object]
    start_index: int
    _i: int
    _is_first_elem: bool

    def __init__(self, array, start_index):
        self.array = array
        self.start_index = start_index
        self._i = start_index
        self._is_first_elem = False

    def __iter__(self):
        self._i = self.start_index
        return self

    def __next__(self):
        if self._i == self.start_index:
            if self._is_first_elem:
                raise StopIteration
            else:
                self._is_first_elem = True

        item = self.array[self._i]
        self._i += 1

        if self._i == len(self.array):
            self._i = 0

        return item

    def __len__(self):
        return len(self.array)

    def __reversed__(self):
        return CounterClockwiseIterator(self.array, self.start_index)


class CounterClockwiseIterator(ClockwiseIterator):
    "Reversed clockwise iterator."

    def __next__(self):
        if self._i == self.start_index:
            if self._is_first_elem:
                raise StopIteration
            else:
                self._is_first_elem = True

        item = self.array[self._i]

        if self._i == 0:
            self._i = len(self.array)

        self._i -= 1

        return item


class CameraUsage(IntEnum):
    VISIBLE = auto()
    SELECTED = auto()


class CameraOrder(IntEnum):
    CLOCKWISE = auto()
    ORIGINAL = auto()


class CameraProperties:
    def _usage_items(self, context: Context):
        return (
            (
                CameraUsage.VISIBLE.name,
                "Visible",
                "Render from all visible cameras",
                icons.get_id('visible'),
                CameraUsage.VISIBLE.value
            ),
            (
                CameraUsage.SELECTED.name,
                "Selected",
                "Render only from selected cameras",
                icons.get_id('selected'),
                CameraUsage.SELECTED.value,
            )
        )

    usage: EnumProperty(
        items=_usage_items,
        default=CameraUsage.VISIBLE.value,
        options={'SKIP_SAVE'},
        name="Cameras Usage",
        description="Which cameras to use for rendering",
    )

    def _order_items(self, context: Context):
        return (
            (
                CameraOrder.CLOCKWISE.name,
                "Clockwise",
                "",
                icons.get_id('counter' if self.reverse else 'clockwise'),
                CameraOrder.CLOCKWISE.value
            ),
            (
                CameraOrder.ORIGINAL.name,
                "Original",
                "",
                icons.get_id('outliner_reverse' if self.reverse else 'outliner'),
                CameraOrder.ORIGINAL.value
            ),
        )

    order: EnumProperty(
        name="Direction",
        items=_order_items,
        default=CameraOrder.ORIGINAL.value,
        options={'SKIP_SAVE'},
        description=(
            "The direction in which the cameras will change during the rendering of the sequence (Starting from the "
            "current camera of the scene)"
        ),
    )

    reverse: BoolProperty(
        default=False,
        options={'SKIP_SAVE'},
        name="Reverse",
        description="Iterate cameras in reverse order",
    )

    def draw_camera_usage_properties(self, layout: UILayout):
        col = layout.column()
        col.use_property_split = True
        col.use_property_decorate = False

        col.prop(self, "usage", expand=True)
        col.prop(self, "order", expand=True)
        col.prop(self, "reverse")


class ClockwiseCameraIterator(ClockwiseIterator):
    def __init__(self, context: Context, usage: CameraUsage, order: CameraOrder):
        match usage:
            case CameraUsage.VISIBLE:
                objects = context.visible_objects
            case CameraUsage.SELECTED:
                objects = context.selected_objects

        active_camera = context.scene.camera

        cameras: list | npt.NDArray[Object] = []

        if len(objects):
            match order:
                case CameraOrder.CLOCKWISE:

                    cameras = np.asarray(objects)

                    angles = np.full(len(objects), np.nan, dtype=np.float32)
                    for i, ob in enumerate(objects):
                        if 'CAMERA' == ob.type:
                            x, y = -Vector([ob.matrix_world[0][2], ob.matrix_world[1][2]]).normalized()
                            angles[i] = math.atan2(x, y)

                    mask = ~np.isnan(angles)
                    if mask.any():
                        indices = np.argsort(angles[mask])
                        cameras = cameras[mask][indices]

                case CameraOrder.ORIGINAL:
                    cameras = [ob for ob in objects if ob.type == 'CAMERA']

        if active_camera in cameras and validate_camera_object(active_camera):
            start_index = np.argmax(cameras == active_camera)
        else:
            start_index = 0

        super().__init__(array=cameras, start_index=start_index)
