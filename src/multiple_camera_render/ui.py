# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import UILayout, Panel

from . import icons
from . import main
from . import ADDON_PKG
assert ADDON_PKG

import bhqui4 as bhqui


class MCR_PT_options(Panel):
    bl_label = "Options"

    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'
    bl_ui_units_x = 12

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene_props = context.scene.mcr

        col = layout.column()

        col.prop(scene_props, "cameras_usage", expand=True)
        col.prop(scene_props, "direction", expand=True)
        col.prop(scene_props, "keep_frame_in_filepath")


class MCR_PT_scene_use_per_camera(Panel):
    bl_label = "Per Camera"

    bl_space_type = 'TOPBAR'
    bl_region_type = 'HEADER'

    def draw(self, context):
        layout = self.layout

        layout.use_property_decorate = False
        layout.use_property_split = False
        layout.ui_units_x = 32

        skip_cycles = not main.PersistentPerCamera.check_cycles()
        if skip_cycles:
            layout.ui_units_x = 26

        scene_props = context.scene.mcr

        row = layout.row()
        row.label(text="Per Camera")

        srow = row.row()
        srow.alignment = 'RIGHT'
        srow.operator(operator=main.OBJECT_OT_per_camera_dump.bl_idname)
        srow.operator(operator=main.OBJECT_OT_per_camera_clear.bl_idname)

        layout.separator(type='LINE')

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
            if category == "Cycles" and skip_cycles:
                continue

            col = row.column(align=True)
            col.label(text=category)

            for data_path in data_paths:
                if data_path is None:
                    col.separator(type='LINE')
                else:
                    col.prop(
                        scene_props,
                        main.PersistentPerCamera.SCENE_FLAG_MAP[data_path],
                        text=main.PersistentPerCamera.eval_scene_flag_ui_label(data_path)
                    )


def additional_TOPBAR_MT_render_draw(self, context):
    from . import main

    layout: UILayout = self.layout
    layout.separator()
    col = layout.column()
    col.operator_context = 'INVOKE_DEFAULT'

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

    def _get_menu_icon(attr: str):
        scene_props = context.scene.mcr
        return col.enum_item_icon(scene_props, attr, getattr(scene_props, attr))

    col.popover(panel=MCR_PT_options.__name__, icon_value=_get_menu_icon("cameras_usage"))
    col.popover(panel=MCR_PT_scene_use_per_camera.__name__, icon_value=icons.get_id('per_camera'))
