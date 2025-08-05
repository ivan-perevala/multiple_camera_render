# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# NOTE: This script prepares data for:
# file://./../../src/bl_tests/test_per_camera_active_camera_saved.py
# What it doing is sets render resolution and scene flag. Camera id properties should stay untouched before saving.

import bpy  # pyright: ignore [reportMissingModuleSource]

import os
import sys

if __name__ == '__main__':
    test_blend_filepath = sys.argv[sys.argv.index("test_blend_filepath") + 1]
    assert os.path.isdir(os.path.dirname(test_blend_filepath))
    assert not os.path.isfile(test_blend_filepath)

    context = bpy.context
    scene = context.scene

    assert scene.camera.name == 'Camera'

    scene.mcr.use_per_camera_render_resolution_x = True
    scene.render.resolution_x = 123

    cam = scene.camera.data
    assert 'render_resolution_x' not in cam.mcr

    bpy.ops.wm.save_mainfile(filepath=test_blend_filepath)
