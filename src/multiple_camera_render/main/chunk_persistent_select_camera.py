# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import bpy
from bpy.types import Context, Object

import bhqmain4 as bhqmain

from .. import get_preferences
from . validate_id import validate_camera_object
from . register_handlers import register_handler, unregister_handler

if TYPE_CHECKING:
    from . chunk_persistent_main import PersistentMain

log = logging.getLogger(__name__)


class PersistentSelectCamera(bhqmain.MainChunk['PersistentMain', 'Context']):
    prev_active_ob: None | Object

    def __init__(self, main):
        self.prev_active_ob = None

        super().__init__(main)

    def invoke(self, context):
        scene = context.scene
        addon_pref = get_preferences()
        scene.mcr.select_camera = addon_pref.select_camera

        self.prev_active_ob = context.active_object

        self.conditional_handler_register(scene_props=scene.mcr)

        return super().invoke(context)

    def cancel(self, context):
        if unregister_handler(bpy.app.handlers.depsgraph_update_post, self.depsgraph_update_post):
            log.debug("Unregistered select camera depsgraph handler")

        return super().cancel(context)

    def conditional_handler_register(self, *, scene_props):
        if scene_props.select_camera:
            if register_handler(
                bpy.app.handlers.depsgraph_update_post,
                self.depsgraph_update_post,
                before=self.main.per_camera.depsgraph_update_post
            ):
                log.debug("Registered select camera depsgraph handler")
        else:
            self.unregister_select_camera_handler()

    def unregister_select_camera_handler(self):
        if unregister_handler(bpy.app.handlers.depsgraph_update_post, self.depsgraph_update_post):
            log.debug("Unregistered select camera depsgraph handler")

    def is_handler_active(self):
        return self.depsgraph_update_post in bpy.app.handlers.depsgraph_update_post

    def depsgraph_update_post(self, scene, dg):
        context = bpy.context

        ob = context.view_layer.objects.active
        if validate_camera_object(ob) and ob != self.prev_active_ob:
            context.scene.camera = ob

        self.prev_active_ob = ob
