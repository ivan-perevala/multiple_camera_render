# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from bpy.types import Context

import bhqmain4 as bhqmain

from . import chunk_persistent_per_camera


class PersistentMain(bhqmain.MainChunk['PersistentMain', 'Context']):
    chunks = {
        "per_camera": chunk_persistent_per_camera.PersistentPerCamera,
    }

    def __init__(self, main):
        super().__init__(main)

    def invoke(self, context):
        return super().invoke(context)

    def cancel(self, context):
        return super().cancel(context)
