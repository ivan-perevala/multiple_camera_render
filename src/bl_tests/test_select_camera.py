# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

import bpy

from . conftest import get_camera, set_active_object


def test_select_camera_active():
    context = bpy.context
    scene = context.scene

    scene.mcr.select_camera = True

    camera0 = get_camera(0)
    assert scene.camera == camera0

    camera1 = get_camera(1)
    set_active_object(camera1)

    assert scene.camera == camera1


def test_select_camera_inactive():
    context = bpy.context
    scene = context.scene

    scene.mcr.select_camera = False

    camera0 = get_camera(0)
    assert scene.camera == camera0

    camera1 = get_camera(1)
    set_active_object(camera1)

    assert scene.camera == camera0
