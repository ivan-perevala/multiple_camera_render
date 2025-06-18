# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.app.handlers import persistent


@persistent
def depsgraph_update_pre(scene):
    print(scene.camera)


@persistent
def depsgraph_update_post(scene):
    print(scene.camera)
