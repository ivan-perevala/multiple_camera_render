# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import os
import logging
from typing import ClassVar

import bpy
from bpy.props import PointerProperty
from bpy.types import Scene, Camera, TOPBAR_MT_render
from bpy.app.handlers import persistent
import addon_utils


ADDON_PKG = __package__


import bhqrprt4 as bhqrprt
import bhqmain4 as bhqmain

log = logging.getLogger(__name__)


def get_preferences() -> props.Preferences:
    return bpy.context.preferences.addons[ADDON_PKG].preferences


def __reload_submodules(lc):
    from importlib import reload
    if "icons" in lc:
        reload(icons)
    if "props" in lc:
        reload(props)
    if "ui" in lc:
        reload(ui)
    if "main" in lc:
        reload(main)


__reload_submodules(locals())
del __reload_submodules

from . import icons
from . import props
from . import ui
from . import main

_classes = (
    props.Preferences,
    props.SceneProps,
    props.CameraProps,
    main.RENDER_OT_multiple_camera_render,
    main.SCENE_OT_mcr_per_camera_enable,
    main.SCENE_MT_mcr_per_camera_presets,
    main.SCENE_OT_mcr_per_camera_preset_add,
    ui.MCR_PT_options,
    ui.MCR_PT_scene_use_per_camera,
)

_cls_register, _cls_unregister = bpy.utils.register_classes_factory(_classes)


@persistent
def handler_load_pre(_=None):
    p_main = main.PersistentMain.get_instance()
    if p_main and p_main():
        if p_main().cancel(bpy.context) != bhqmain.InvokeState.SUCCESSFUL:
            log.error("Failed to cancel PersistentMain")


@persistent
def handler_load_post(_=None):
    scene = bpy.context.scene
    bhqrprt.log_bpy_struct_properties(log, struct=scene.mcr)

    p_main = main.PersistentMain.get_instance()
    if p_main is not None:
        raise RuntimeError("PersistentMain instance already exists, this should not happen.")

    p_main = main.PersistentMain.create()
    if p_main and p_main():
        if p_main().invoke(bpy.context) != bhqmain.InvokeState.SUCCESSFUL:
            log.error("Failed to invoke PersistentMain")


_handlers = (
    (bpy.app.handlers.load_pre, handler_load_pre),
    (bpy.app.handlers.load_post, handler_load_post),
)


@bhqrprt.register_reports(log, props.Preferences, directory=os.path.join(os.path.dirname(__file__), "logs"))
def register():
    icons.Icons.register()

    _cls_register()
    Scene.mcr = PointerProperty(type=props.SceneProps)
    Camera.mcr = PointerProperty(type=props.CameraProps)
    TOPBAR_MT_render.append(ui.additional_TOPBAR_MT_render_draw)

    for handler, func in _handlers:
        if func not in handler:
            handler.append(func)
        else:
            log.warning(f"Handler {func} already registered, skipping.")


@bhqrprt.unregister_reports(log)
def unregister():
    p_main = main.PersistentMain.get_instance()
    if p_main is not None:
        if p_main().cancel(bpy.context) != bhqmain.InvokeState.SUCCESSFUL:
            log.warning("Unable to cancel persistent chunk at unregistering")

    for handler, func in reversed(_handlers):
        if func in handler:
            handler.remove(func)
        else:
            log.warning(f"Handler {func} not found, skipping removal.")

    icons.Icons.cache.release()
    TOPBAR_MT_render.remove(ui.additional_TOPBAR_MT_render_draw)
    _cls_unregister()
    del Camera.mcr
    del Scene.mcr

    icons.Icons.unregister()
