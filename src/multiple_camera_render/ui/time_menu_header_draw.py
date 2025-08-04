# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from bpy.types import UILayout

from .. import main
from .. import icons


def additional_TIME_MT_marker_draw(self, context):
    layout: UILayout = self.layout
    col = layout.column()

    col.separator(type='LINE')

    col.operator(operator=main.MARKER_create_from_cameras.bl_idname, icon_value=icons.get_id('markers'))
