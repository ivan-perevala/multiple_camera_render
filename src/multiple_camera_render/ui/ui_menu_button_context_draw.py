# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from bpy.types import Menu, Context

from .. import main


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
