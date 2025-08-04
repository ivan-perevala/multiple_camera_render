# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from bpy.types import Panel, Context, UILayout

from .. import icons


def additional_VIEW3D_HT_header_draw(self: Panel, context: Context):
    layout: UILayout = self.layout
    row = layout.row()

    scene = context.scene

    row.prop(scene.mcr, "select_camera", icon_only=True, icon_value=icons.get_id('select_camera'))
