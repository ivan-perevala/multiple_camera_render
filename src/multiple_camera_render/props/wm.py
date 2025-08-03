# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import PropertyGroup, Context
from bpy.props import StringProperty

from .. import main


class WMProps(PropertyGroup):
    def _search_scene_per_camera_flag(self, context: Context, edit_text: str):
        return tuple(
            (f"{category}: {main.PersistentPerCamera.eval_scene_flag_ui_label(data_path)}", data_path)
            for category, names in main.PersistentPerCamera.SCENE_DATA_PATHS_GROUPED.items()
            for data_path in names
            if data_path is not None
        )

    scene_per_camera_flag_search: StringProperty(
        options={'SKIP_SAVE'},
        search=_search_scene_per_camera_flag,
        name="Search",
        description="Search for option flag",
    )
