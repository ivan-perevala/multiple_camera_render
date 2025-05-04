# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import UILayout


def additional_TOPBAR_MT_render_draw(self, context):
    from . import main

    layout: UILayout = self.layout
    layout.separator()
    col = layout.column()
    col.operator_context = 'INVOKE_DEFAULT'

    col.operator(operator=main.MCR_OT_render.bl_idname, text="Render Multiple Cameras")
    col.operator(operator=main.MCR_OT_render.bl_idname, text="Render Animation from Multiple Cameras").animation = True

    col.operator(operator=main.MCR_OT_render.bl_idname, text="Preview").preview = True
    props = col.operator(operator=main.MCR_OT_render.bl_idname, text="Preview Animation")
    props.preview = True
    props.animation = True

    scene_props = context.scene.mcr

    layout.prop_menu_enum(scene_props, "cameras_usage")
    layout.prop_menu_enum(scene_props, "direction")
    layout.prop(scene_props, "keep_frame_in_filepath")
