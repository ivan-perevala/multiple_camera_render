# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

import sys

import bpy

if __name__ == '__main__':
    context = bpy.context
    scene = context.scene

    args = sys.argv[sys.argv.index('--'):]

    scene.mcr.select_camera = "--with-select-camera" in args

    bpy.ops.render.multiple_camera_render('INVOKE_DEFAULT', animation=False, preview=False, quit=True)
