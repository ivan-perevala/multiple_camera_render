# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

import bpy   # pyright: ignore [reportMissingModuleSource]
from bpy.types import Context, STATUSBAR_HT_header   # pyright: ignore [reportMissingModuleSource]
from bpy.app.handlers import persistent   # pyright: ignore [reportMissingModuleSource]
import bl_ui   # pyright: ignore [reportMissingModuleSource]

import bhqmain4 as bhqmain

from . chunk_persistent_per_camera import PersistentPerCamera
from . chunk_persistent_select_camera import PersistentSelectCamera
from . register_handlers import register_handler, unregister_handler
from .. import icons

log = logging.getLogger(__name__)


class PersistentMain(bhqmain.MainChunk['PersistentMain', 'Context']):
    per_camera: PersistentPerCamera
    select_camera: PersistentSelectCamera

    chunks = {
        "select_camera": PersistentSelectCamera,
        "per_camera": PersistentPerCamera,
    }

    def __init__(self, main):
        super().__init__(main)

    def invoke(self, context):
        STATUSBAR_HT_header.append(self._statusbar_draw_status)
        return super().invoke(context)

    def cancel(self, context):
        STATUSBAR_HT_header.remove(self._statusbar_draw_status)
        return super().cancel(context)

    @classmethod
    def register(cls):
        register_handler(bpy.app.handlers.load_post, cls.create_and_invoke_on_load_post)
        bpy.app.timers.register(cls.create_and_invoke, first_interval=0.1)

        register_handler(bpy.app.handlers.load_pre, cls.cancel_on_load_pre)

    @classmethod
    def unregister(cls):
        unregister_handler(bpy.app.handlers.load_pre, cls.cancel_on_load_pre)
        unregister_handler(bpy.app.handlers.load_post, cls.create_and_invoke_on_load_post)

        pmain = cls.get_instance()
        if pmain and pmain():
            if pmain().cancel(bpy.context) != bhqmain.InvokeState.SUCCESSFUL:
                log.warning(f"Unable to unregister {cls.__name__} instance")

    @staticmethod
    def _statusbar_draw_status(self: bl_ui.space_statusbar.STATUSBAR_HT_header, context: Context):
        layout = self.layout

        pmain = PersistentMain.get_instance()
        if pmain and pmain():
            if pmain().per_camera.is_handler_active():
                layout.label(text="Per Camera Active", icon_value=icons.get_id('per_camera_dimmed'))
            if pmain().select_camera.is_handler_active():
                layout.label(text="Select Camera Active", icon_value=icons.get_id('select_camera_dimmed'))

    @classmethod
    def create_and_invoke(cls):
        context = bpy.context

        pmain = cls.get_instance()

        if not pmain:
            pmain = cls.create()

            if pmain and pmain():
                if pmain().invoke(context) != bhqmain.InvokeState.SUCCESSFUL:
                    log.warning(f"Unable to invoke {cls.__name__} instance with {context}")

    @classmethod
    @persistent
    def create_and_invoke_on_load_post(cls, *args, **kwargs):
        if bpy.app.timers.is_registered(cls.create_and_invoke):
            bpy.app.timers.unregister(cls.create_and_invoke)
            log.debug(f"Unregistered {cls.create_and_invoke.__name__} timer callback (load post executed first)")

        cls.create_and_invoke()

    @classmethod
    @persistent
    def cancel_on_load_pre(cls, *args, **kwargs):
        pmain = cls.get_instance()
        if pmain and pmain():
            if pmain().cancel(bpy.context) != bhqmain.InvokeState.SUCCESSFUL:
                log.warning(f"Failed to cancel {cls.__name__} instance before loading new file")
            else:
                log.debug(f"{cls.__name__} was cancelled on load pre")
        else:
            log.warning("There is no instance to cancel before loading new file")
