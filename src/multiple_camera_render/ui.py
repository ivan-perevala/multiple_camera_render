# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import UILayout, Menu, Panel

from . import icons
from . import main
from . import ADDON_PKG
assert ADDON_PKG

import bhqui4 as bhqui


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


class MCR_PT_scene_use_per_camera(Panel):
    bl_label = "Per Camera"

    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 36

    def draw(self, context):
        layout = self.layout
        layout.use_property_decorate = False
        layout.use_property_split = False
        scene_props = context.scene.mcr

        row = layout.row()
        row.label(text="Use Flags")

        bhqui.template_preset(
            row,
            menu=main.SCENE_MT_mcr_per_camera_presets,
            operator=main.SCENE_OT_mcr_per_camera_preset_add.bl_idname,
        )

        srow = row.row()
        srow.alignment = 'RIGHT'
        srow.label(text="Select")
        srow.operator(operator=main.SCENE_OT_mcr_per_camera_enable.bl_idname, text="All").disable = False
        srow.operator(operator=main.SCENE_OT_mcr_per_camera_enable.bl_idname, text="None").disable = True

        layout.separator(type='LINE')

        row = layout.row()

        for category, data_paths in main.PersistentPerCamera.SCENE_DATA_PATHS_GROUPED.items():
            col = row.column(align=True)
            col.label(text=category)

            for data_path in data_paths:
                if data_path is None:
                    col.separator(type='LINE')
                else:
                    col.prop(scene_props, main.PersistentPerCamera.SCENE_FLAG_MAP[data_path])


def additional_TOPBAR_MT_render_draw(self, context):
    from . import main

    layout: UILayout = self.layout
    layout.separator()
    col = layout.column()
    col.operator_context = 'INVOKE_DEFAULT'

    conflicting_addons, conflicting_modules = main.check_handlers_conflicts()
    if conflicting_addons or conflicting_modules:
        col.operator(
            operator="preferences.addon_show",
            text="Conflicting Add-ons Detected",
            icon_value=icons.get_id('conflicting_addons')
        ).module = ADDON_PKG

    col.operator(
        operator=main.RENDER_OT_multiple_camera_render.bl_idname,
        text="Render Multiple Cameras",
        icon_value=icons.get_id('render'),
    )

    props = col.operator(
        operator=main.RENDER_OT_multiple_camera_render.bl_idname,
        text="Render Animation from Multiple Cameras",
        icon_value=icons.get_id('render_animation'),
    )
    props.animation = True

    props = col.operator(
        operator=main.RENDER_OT_multiple_camera_render.bl_idname,
        text="Preview",
        icon_value=icons.get_id('preview'),
    )
    props.preview = True

    props = col.operator(
        operator=main.RENDER_OT_multiple_camera_render.bl_idname,
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

    col.popover(panel=MCR_PT_scene_use_per_camera.__name__, icon_value=icons.get_id('per_camera'))
