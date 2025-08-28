# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

from bpy.types import PropertyGroup, Context   # pyright: ignore [reportMissingModuleSource]
from bpy.props import StringProperty, EnumProperty   # pyright: ignore [reportMissingModuleSource]

import bhqrprt4 as bhqrprt

from .. import main

log = logging.getLogger(__name__)


class WMProps(PropertyGroup):
    def _search_scene_per_camera_flag(self, context: Context, edit_text: str):
        return tuple(
            label
            for _md5_hash, [label, _data_path, _path_split] in main.PersistentPerCamera.DATA_PATHS.items()
        )

    scene_per_camera_flag_search: StringProperty(
        options={'SKIP_SAVE'},
        search=_search_scene_per_camera_flag,
        name="Search",
        description="Search for option flag",
        update=bhqrprt.update_log_setting_changed(log, "scene_per_camera_flag_search")
    )  # pyright: ignore [reportInvalidTypeForm]

    scene_per_camera_flag_show: EnumProperty(
        items=(
            (
                'ENABLED',
                "Enabled",
                "Show only enabled flags",
                'HIDE_OFF',
                (1 << 1)
            ),
            (
                'DISABLED',
                "Disabled",
                "Show only disabled flags",
                'HIDE_ON',
                (1 << 2)
            ),
        ),
        default={'ENABLED'},
        options={'ENUM_FLAG', 'SKIP_SAVE'},
        name="Show Scene Flags",
        description="Which scene per-camera flags should be shown",
        update=bhqrprt.update_log_setting_changed(log, "scene_per_camera_flag_show")
    )  # pyright: ignore [reportInvalidTypeForm]
