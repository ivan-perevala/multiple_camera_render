# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from bpy.types import Menu, Operator   # pyright: ignore [reportMissingModuleSource]
from bl_operators.presets import AddPresetBase   # pyright: ignore [reportMissingModuleSource]

from . chunk_persistent_per_camera import PersistentPerCamera


class SCENE_MT_mcr_per_camera_presets(Menu):
    bl_label = "Per Camera Presets"
    preset_subdir = "scene/multiple_camera_render/per_camera"
    preset_operator = "script.execute_preset"
    draw = Menu.draw_preset


class SCENE_OT_mcr_per_camera_preset_add(AddPresetBase, Operator):
    bl_idname = "scene.mcr_per_camera_preset_add"
    bl_label = "Add Scene Per Camera Preset"
    preset_menu = "SCENE_MT_mcr_per_camera_presets"

    preset_defines = [
        "scene = bpy.context.scene",
        "scene_props = scene.mcr",
    ]

    preset_values = [
        f"scene_props.{PersistentPerCamera.scene_flag_name(md5_hash)}"
        for md5_hash in PersistentPerCamera.DATA_PATHS.keys()
    ]

    preset_subdir = SCENE_MT_mcr_per_camera_presets.preset_subdir
