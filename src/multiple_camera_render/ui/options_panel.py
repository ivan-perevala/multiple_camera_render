# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from bpy.types import Panel

from .. import main


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
