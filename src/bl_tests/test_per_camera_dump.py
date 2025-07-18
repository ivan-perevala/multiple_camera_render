# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from . conftest import set_camera_and_update_depsgraph

import bpy


def test_dump():
    context = bpy.context
    scene = context.scene

    scene.mcr.use_per_camera_render_resolution_x = True

    set_camera_and_update_depsgraph(0)
    scene.render.resolution_x = 128
    set_camera_and_update_depsgraph(1)

    cam0 = scene.objects["Camera"]
    cam1 = scene.objects["Camera.001"]
    cam2 = scene.objects["Camera.002"]

    assert 'render_resolution_x' in cam0.data.mcr
    assert 'render_resolution_x' not in cam1.data.mcr
    assert 'render_resolution_x' not in cam2.data.mcr

    cam0.select_set(False)
    cam1.select_set(False)
    cam2.select_set(True)

    bpy.ops.object.per_camera_dump()

    assert 'render_resolution_x' in cam0.data.mcr
    assert 'render_resolution_x' not in cam1.data.mcr
    assert 'render_resolution_x' in cam2.data.mcr
