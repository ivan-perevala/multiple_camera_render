# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import Menu, Operator
from bl_operators.presets import AddPresetBase

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
        f"scene_props.{flag_name}"
        for flag_name in PersistentPerCamera.SCENE_FLAG_MAP.values()
    ]

    preset_subdir = SCENE_MT_mcr_per_camera_presets.preset_subdir
