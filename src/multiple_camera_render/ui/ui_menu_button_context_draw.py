# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from bpy.types import Menu, Context  # pyright: ignore [reportMissingModuleSource]

from .. import main


def additional_UI_MT_button_context_menu(self: Menu, context: Context):
    if not context.property:
        return

    layout = self.layout

    pmain = main.PersistentMain.get_instance()
    if pmain and pmain():

        data_block, data_path, _array_index = context.property

        scene = context.scene

        if data_block == scene and (md5_hash := pmain().per_camera.hash_from_data_path(data_path)):
            layout.separator(type='LINE')

            col = layout.column(align=True)
            col.use_property_split = False
            col.use_property_decorate = True

            col.prop(scene.mcr, main.PersistentPerCamera.scene_flag_name(md5_hash), text="Use Per Camera")
