# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import bpy
from bpy.types import Context, STATUSBAR_HT_header, UILayout

import bhqmain4 as bhqmain

from . chunk_persistent_per_camera import PersistentPerCamera
from . chunk_persistent_select_camera import PersistentSelectCamera

from .. import icons


class PersistentMain(bhqmain.MainChunk['PersistentMain', 'Context']):
    per_camera: PersistentPerCamera
    select_camera: PersistentSelectCamera

    chunks = {
        "select_camera": PersistentSelectCamera,
        "per_camera": PersistentPerCamera,
    }

    @staticmethod
    def _statusbar_draw_status(self, context):
        layout: UILayout = self.layout

        pmain = PersistentMain.get_instance()
        if pmain and pmain():
            if pmain().per_camera.is_handler_active():
                layout.label(text="Per Camera Active", icon_value=icons.get_id('per_camera_dimmed'))
            if pmain().select_camera.is_handler_active():
                layout.label(text="Select Camera Active", icon_value=icons.get_id('select_camera_dimmed'))

    def __init__(self, main):
        super().__init__(main)

    def invoke(self, context):
        STATUSBAR_HT_header.append(self._statusbar_draw_status)
        return super().invoke(context)

    def cancel(self, context):
        STATUSBAR_HT_header.remove(self._statusbar_draw_status)
        return super().cancel(context)
