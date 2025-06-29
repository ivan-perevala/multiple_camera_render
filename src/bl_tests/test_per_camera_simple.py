# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from . conftest import set_camera_and_update_depsgraph, update_depsgraph

import bpy


def test_per_camera_none(with_select_camera):
    context = bpy.context
    scene = context.scene

    scene.mcr.select_camera = with_select_camera
    scene.mcr.use_per_camera_render_resolution_x = False
    update_depsgraph(context)

    set_camera_and_update_depsgraph(0)
    scene.render.resolution_x = 128

    set_camera_and_update_depsgraph(1)
    scene.render.resolution_x = 256

    set_camera_and_update_depsgraph(2)
    scene.render.resolution_x = 512

    set_camera_and_update_depsgraph(0)
    assert scene.render.resolution_x == 512

    set_camera_and_update_depsgraph(1)
    assert scene.render.resolution_x == 512

    set_camera_and_update_depsgraph(2)
    assert scene.render.resolution_x == 512


def test_per_camera_resolution_x(with_select_camera):

    context = bpy.context
    scene = context.scene
    
    scene.mcr.select_camera = with_select_camera
    scene.mcr.use_per_camera_render_resolution_x = True
    #update_depsgraph(context)

    set_camera_and_update_depsgraph(0)
    scene.render.resolution_x = 128

    set_camera_and_update_depsgraph(1)
    scene.render.resolution_x = 256

    set_camera_and_update_depsgraph(2)
    scene.render.resolution_x = 512

    set_camera_and_update_depsgraph(0)
    assert scene.render.resolution_x == 128

    set_camera_and_update_depsgraph(1)
    assert scene.render.resolution_x == 256

    set_camera_and_update_depsgraph(2)
    assert scene.render.resolution_x == 512
