# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import UILayout, Menu, Panel

from . import icons


class MCR_MT_camera_usage(Menu):
    bl_idname = "MCR_MT_camera_usage"
    bl_label = "Camera Usage"

    def draw(self, context):
        layout = self.layout

        scene_props = context.scene.mcr
        layout.prop(scene_props, "cameras_usage", expand=True)


class MCR_MT_direction(Menu):
    bl_idname = "MCR_MT_direction"
    bl_label = "Direction"

    def draw(self, context):
        layout = self.layout

        scene_props = context.scene.mcr
        layout.prop(scene_props, "direction", expand=True)


def additional_TOPBAR_MT_render_draw(self, context):
    from . import main

    layout: UILayout = self.layout
    layout.separator()
    col = layout.column()
    col.operator_context = 'INVOKE_DEFAULT'

    col.operator(
        operator=main.MCR_OT_render.bl_idname,
        text="Render Multiple Cameras",
        icon_value=icons.get_id('render'),
    )

    props = col.operator(
        operator=main.MCR_OT_render.bl_idname,
        text="Render Animation from Multiple Cameras",
        icon_value=icons.get_id('render_animation'),
    )
    props.animation = True

    props = col.operator(
        operator=main.MCR_OT_render.bl_idname,
        text="Preview",
        icon_value=icons.get_id('preview'),
    )
    props.preview = True

    props = col.operator(
        operator=main.MCR_OT_render.bl_idname,
        text="Preview Animation",
        icon_value=icons.get_id('preview_animation'),
    )
    props.preview = True
    props.animation = True

    scene_props = context.scene.mcr

    def _get_menu_icon(attr: str):
        return col.enum_item_icon(scene_props, attr, getattr(scene_props, attr))

    col.menu(menu=MCR_MT_camera_usage.bl_idname, icon_value=_get_menu_icon("cameras_usage"))
    col.menu(menu=MCR_MT_direction.bl_idname, icon_value=_get_menu_icon("direction"))

    col.prop(scene_props, "keep_frame_in_filepath")


class OBJECT_PT_mesh_sequence(Panel):
    bl_idname = "OBJECT_PT_mesh_sequence"
    bl_label = "Mesh Sequence"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    # bl_options = {'DEFAULT_CLOSED'} # TODO: Should be closed at release

    @classmethod
    def poll(cls, context):
        ob = context.active_object
        return ob and ob.type == 'MESH' and context.mode == 'OBJECT'

    def draw(self, context):
        layout = self.layout

        ob = context.active_object

        col = layout.column(align=True)
        col.prop(ob, "frame_start")
        col.prop(ob, "frame_end")
        col.prop(ob, "frame_step")
        col.separator()
        col.prop(ob, "frame_offset")
