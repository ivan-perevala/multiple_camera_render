# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from typing import TYPE_CHECKING

import bpy
from bpy.types import Window, Timer, Context

import bhqmain

from .. import get_preferences

if TYPE_CHECKING:
    from . chunk_main import Main


class Timers(bhqmain.MainChunk['Main', 'Context']):
    "Handles event timers for window updates. Do nothing in background mode."

    _timers: dict[Window, Timer]

    def __init__(self, main):
        super().__init__(main)

        self._timers = dict()

    def invoke(self, context):
        if not bpy.app.background:
            self._ensure_window_timers(context)

        return super().invoke(context)

    def cancel(self, context):
        if not bpy.app.background:
            self._remove_window_timers(context)

        return super().cancel(context)

    def _ensure_window_timers(self, context: Context):
        wm = context.window_manager

        timestep = 1e-1
        if self.main.preview:
            addon_pref = get_preferences()
            timestep = addon_pref.preview_timestep

        for window in wm.windows:
            if window not in self._timers:
                self._timers[window] = wm.event_timer_add(timestep, window=window)

    def _remove_window_timers(self, context: Context):
        wm = context.window_manager
        for timer in self._timers.values():
            wm.event_timer_remove(timer)
