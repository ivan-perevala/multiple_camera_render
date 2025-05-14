# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import PropertyGroup
from bpy.props import IntProperty, StringProperty, BoolProperty


class ObjectProps(PropertyGroup):
    filepath: StringProperty(
        options={'SKIP_SAVE'},
        subtype='FILE_PATH',
        name="Filepath",
        description="File path to one of objects in sequence",
    )

    frame_duration: IntProperty(
        default=100,
        min=0,
        options={'SKIP_SAVE'},
        name="Frames",
        description="Number of meshes of sequence to use"
    )

    frame_start: IntProperty(
        default=1,
        options={'SKIP_SAVE'},
        name="Start",
        description="Global starting frame of mesh sequence, assuming first mesh has #1",
    )

    frame_offset: IntProperty(
        default=0,
        options={'SKIP_SAVE'},
        name="Offset",
        description="Offset the number of the frame to use in the amination",
    )

    use_cyclic: BoolProperty(
        default=False,
        options={'SKIP_SAVE'},
        name="Cyclic",
        description="Cyclic the meshes"
    )
