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
        layout.ui_units_x = 13

        layout.use_property_decorate = False
        layout.use_property_split = False

        pmain = main.PersistentMain.get_instance()
        if pmain and pmain():
            col = layout.column(align=True)
            col.label(text='Selected Cameras Settings')
            col.operator(operator=main.OBJECT_OT_per_camera_dump.bl_idname, text="Apply Current")
            col.operator(operator=main.OBJECT_OT_per_camera_clear.bl_idname, text="Clear")

            col.label(text="Flags")

            bhqui.template_preset(
                col,
                menu=main.SCENE_MT_mcr_per_camera_presets,
                operator=main.SCENE_OT_mcr_per_camera_preset_add.bl_idname,
            )

            col.separator(type='SPACE')

            props: main.SCENE_OT_mcr_per_camera_enable = col.operator(
                operator=main.SCENE_OT_mcr_per_camera_enable.bl_idname,
                text="Enable All")
            props.disable = False

            props: main.SCENE_OT_mcr_per_camera_enable = col.operator(
                operator=main.SCENE_OT_mcr_per_camera_enable.bl_idname,
                text="Disable All")
            props.disable = True

            wm = context.window_manager
            scene = context.scene

            col.separator(type='SPACE')
            col.prop(wm.mcr, "scene_per_camera_flag_search", icon='VIEWZOOM', text="")
            col.separator(type='SPACE')

            if wm.mcr.scene_per_camera_flag_search:
                md5_hash = pmain().per_camera.hash_from_label(label=wm.mcr.scene_per_camera_flag_search)

                if md5_hash:
                    col.prop(scene.mcr, pmain().per_camera.scene_flag_name(md5_hash))
                else:
                    col.label(text="Not Found", icon='ERROR')
            else:
                row = col.row(align=True)
                row.alignment = 'RIGHT'
                row.prop(wm.mcr, "scene_per_camera_flag_show", expand=True, text="Show")

                col.separator(type='SPACE')

                is_none_enabled = True

                disabled_scene_flag_names = []

                show_enabled = 'ENABLED' in wm.mcr.scene_per_camera_flag_show

                for md5_hash in main.PersistentPerCamera.DATA_PATHS.keys():
                    scene_flag_name = pmain().per_camera.scene_flag_name(md5_hash)
                    is_enabled = getattr(scene.mcr, scene_flag_name, False)
                    if is_enabled and show_enabled:
                        col.prop(scene.mcr, scene_flag_name)
                        is_none_enabled = False
                    else:
                        disabled_scene_flag_names.append(scene_flag_name)

                if is_none_enabled and show_enabled:
                    col.label(text="No enabled flags")

                if 'DISABLED' in wm.mcr.scene_per_camera_flag_show:
                    if not is_none_enabled or show_enabled:
                        col.separator(type='LINE')

                    for scene_flag_name in disabled_scene_flag_names:
                        col.prop(scene.mcr, scene_flag_name)

        # layout.ui_units_x = 46

        # skip_cycles = not main.PersistentPerCamera.check_cycles()
        # if skip_cycles:
        #     layout.ui_units_x = 26

        # scene_props = context.scene.mcr

        # row = layout.row()
        # row.label(text="Per Camera")

        # srow = row.row()
        # srow.alignment = 'RIGHT'
        # srow.operator(operator=main.OBJECT_OT_per_camera_dump.bl_idname)
        # srow.operator(operator=main.OBJECT_OT_per_camera_clear.bl_idname)

        # layout.separator(type='LINE')

        # row = layout.row()
        # row.label(text="Use Flags")

        # wm = context.window_manager
        # row.prop(wm.mcr, "scene_per_camera_flag_search", icon='VIEWZOOM', text="")

        # bhqui.template_preset(
        #     row,
        #     menu=main.SCENE_MT_mcr_per_camera_presets,
        #     operator=main.SCENE_OT_mcr_per_camera_preset_add.bl_idname,
        # )

        # srow = row.row()
        # srow.alignment = 'RIGHT'
        # srow.label(text="Select")

        # props: main.SCENE_OT_mcr_per_camera_enable = srow.operator(
        #     operator=main.SCENE_OT_mcr_per_camera_enable.bl_idname,
        #     text="All")
        # props.disable = False

        # props: main.SCENE_OT_mcr_per_camera_enable = srow.operator(
        #     operator=main.SCENE_OT_mcr_per_camera_enable.bl_idname,
        #     text="None")
        # props.disable = True

        # layout.separator(type='LINE')

        # row = layout.row()

        # if wm.mcr.scene_per_camera_flag_search:
        #     row.alignment = 'CENTER'

        #     for md5_hash, [label, _data_path, _path_split] in main.PersistentPerCamera.DATA_PATHS.items():
        #         if label == wm.mcr.scene_per_camera_flag_search:
        #             row.prop(
        #                 scene_props,
        #                 main.PersistentPerCamera.scene_flag_name(md5_hash),
        #                 text=label
        #             )
        #             break
        #     else:
        #         row.label(text="Not Found", icon='ERROR')

        # else:
        #     col_flow = layout.column_flow(columns=4, align=True)

        #     for md5_hash, [label, data_path, path_split] in main.PersistentPerCamera.DATA_PATHS.items():
        #         col_flow.prop(
        #             scene_props,
        #             main.PersistentPerCamera.scene_flag_name(md5_hash)
        #         )
