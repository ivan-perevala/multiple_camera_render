# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# NOTE: This test case work in pair with setup script which runs in separate Blender instance:
# file://./../../tests/test_scripts/_test_per_camera_prepare_save_case.py

import bpy  # pyright: ignore [reportMissingModuleSource]


def test_per_camera_active_camera_saved():
    context = bpy.context
    scene = context.scene

    assert scene.render.resolution_x == 123
    assert scene.camera.name == 'Camera'

    cam = scene.camera.data

    assert 'render_resolution_x' in cam.mcr
