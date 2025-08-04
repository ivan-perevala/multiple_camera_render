# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from bpy.types import Panel

import bhqui4 as bhqui

from .. import main


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
