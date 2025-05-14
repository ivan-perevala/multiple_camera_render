# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import PropertyGroup
from bpy.props import IntProperty, StringProperty


class ObjectProps(PropertyGroup):
    filepath: StringProperty(
        options={'SKIP_SAVE'},
        subtype='FILE_PATH',
        name="Filepath",
        description="File path to one of objects in sequence",
    )

    frame_start: IntProperty(
        default=0,
        options={'SKIP_SAVE'},
        name="Frame Start",
        description="Starting frame for object sequence animation"
    )

    frame_end: IntProperty(
        default=1,
        options={'SKIP_SAVE'},
        name="Frame End",
        description="Last frame for object sequence animation",
    )

    frame_step: IntProperty(
        default=1,
        options={'SKIP_SAVE'},
        name="Frame Step",
        description="Step for object sequence animation",
    )

    frame_offset: IntProperty(
        default=1,
        options={'SKIP_SAVE'},
        name="Frame Offset",
        description="Offset frame to start animation at",
    )
