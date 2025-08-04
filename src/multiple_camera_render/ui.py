# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import UILayout, Panel, Context, Menu, Scene

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

        scene_props.draw_camera_usage_properties(layout)

        layout.separator(type='LINE')

        col = layout.column()
        col.prop(scene_props, "frame_usage", expand=True)

        scol = layout.column()
        scol.enabled = scene_props.frame_usage in {
            main.FrameUsage.MARKERS_IN_RANGE.name,
            main.FrameUsage.SELECTED_MARKERS.name
        }

        scol.prop(scene_props, "frame_usage_reverse")

        layout.prop(scene_props, "keep_frame_in_filepath")


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

        wm = context.window_manager
        row.prop(wm.mcr, "scene_per_camera_flag_search", icon='VIEWZOOM', text="")

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

        if wm.mcr.scene_per_camera_flag_search:
            search_split = wm.mcr.scene_per_camera_flag_search.split(': ')
            row.alignment = 'CENTER'

            if len(search_split) == 2:
                category, label = search_split
                possible_data_paths = main.PersistentPerCamera.SCENE_DATA_PATHS_GROUPED[category]

                for data_path in possible_data_paths:
                    if data_path and main.PersistentPerCamera.eval_scene_flag_ui_label(data_path) == label:
                        if label := main.PersistentPerCamera.eval_scene_flag_ui_label(data_path):
                            row.prop(
                                scene_props,
                                main.PersistentPerCamera.SCENE_FLAG_MAP[data_path],
                                text=label
                            )
                            break
            else:
                row.label(text="Not Found", icon='ERROR')

        else:
            for category, data_paths in main.PersistentPerCamera.SCENE_DATA_PATHS_GROUPED.items():
                if category == "Cycles" and skip_cycles:
                    continue

                col = row.column(align=True)
                col.label(text=category)

                for data_path in data_paths:
                    if data_path is None:
                        col.separator(type='LINE')
                    else:
                        if label := main.PersistentPerCamera.eval_scene_flag_ui_label(data_path):
                            col.prop(
                                scene_props,
                                main.PersistentPerCamera.SCENE_FLAG_MAP[data_path],
                                text=label
                            )


def additional_TOPBAR_MT_render_draw(self: Panel, context: Context):
    from . import main

    layout: UILayout = self.layout
    layout.separator()

    col = layout.column()
    col.operator_context = 'INVOKE_DEFAULT'

    scene = context.scene
    scene_props = scene.mcr

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

    attr = "usage"
    icon_value = col.enum_item_icon(scene_props, attr, getattr(scene_props, attr))

    col.popover(panel=MCR_PT_options.__name__, icon_value=icon_value)
    col.popover(panel=MCR_PT_scene_use_per_camera.__name__, icon_value=icons.get_id('per_camera'))


def additional_VIEW3D_HT_header_draw(self: Panel, context: Context):
    layout: UILayout = self.layout
    row = layout.row()

    scene = context.scene

    row.prop(scene.mcr, "select_camera", icon_only=True, icon_value=icons.get_id('select_camera'))


def additional_TIME_MT_marker_draw(self, context):
    layout: UILayout = self.layout
    col = layout.column()

    col.separator(type='LINE')

    col.operator(operator=main.MARKER_create_from_cameras.bl_idname, icon_value=icons.get_id('markers'))


def additional_UI_MT_button_context_menu(self: Menu, context: Context):
    layout = self.layout

    if context.property:
        data_block, data_path, _array_index = context.property

        scene = context.scene

        if data_block == scene and data_path in main.PersistentPerCamera.SCENE_DATA_PATHS:
            layout.separator(type='LINE')

            col = layout.column(align=True)
            col.use_property_split = False
            col.use_property_decorate = True

            col.prop(scene.mcr, main.PersistentPerCamera.SCENE_FLAG_MAP[data_path], text="Use Per Camera")
