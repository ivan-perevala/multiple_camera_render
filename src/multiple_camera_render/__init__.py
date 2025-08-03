# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import os
import logging

import bpy
from bpy.props import PointerProperty
from bpy.types import Scene, Camera, TOPBAR_MT_render, VIEW3D_HT_header, TIME_MT_marker, UI_MT_button_context_menu
from bpy.app.handlers import persistent

ADDON_PKG = __package__

log = logging.getLogger(__name__)

import bhqrprt4 as bhqrprt


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
from . import main
from . import ui

_classes = (
    props.Preferences,
    props.SceneProps,
    props.CameraProps,
    main.RENDER_OT_multiple_camera_render,
    main.SCENE_OT_mcr_per_camera_enable,
    main.SCENE_MT_mcr_per_camera_presets,
    main.SCENE_OT_mcr_per_camera_preset_add,
    main.OBJECT_OT_per_camera_dump,
    main.OBJECT_OT_per_camera_clear,
    main.MARKER_create_from_cameras,
    ui.MCR_PT_options,
    ui.MCR_PT_scene_use_per_camera,
)

from . main.register_handlers import register_handler, unregister_handler

_cls_register, _cls_unregister = bpy.utils.register_classes_factory(_classes)


@persistent
def log_scene_properties_on_load_post(_=None):
    scene = bpy.context.scene
    bhqrprt.log_bpy_struct_properties(log, struct=scene.mcr)

@bhqrprt.register_reports(log, props.Preferences, directory=os.path.join(os.path.dirname(__file__), "logs"))
def register():
    icons.Icons.register()

    _cls_register()
    Scene.mcr = PointerProperty(type=props.SceneProps)
    Camera.mcr = PointerProperty(type=props.CameraProps)

    TOPBAR_MT_render.append(ui.additional_TOPBAR_MT_render_draw)
    VIEW3D_HT_header.append(ui.additional_VIEW3D_HT_header_draw)
    TIME_MT_marker.append(ui.additional_TIME_MT_marker_draw)
    UI_MT_button_context_menu.append(ui.additional_UI_MT_button_context_menu)

    register_handler(bpy.app.handlers.load_post, log_scene_properties_on_load_post)
    main.PersistentMain.register()


@bhqrprt.unregister_reports(log)
def unregister():
    main.PersistentMain.unregister()

    unregister_handler(bpy.app.handlers.load_post, log_scene_properties_on_load_post)

    icons.Icons.cache.release()

    UI_MT_button_context_menu.remove(ui.additional_UI_MT_button_context_menu)
    VIEW3D_HT_header.remove(ui.additional_VIEW3D_HT_header_draw)
    TOPBAR_MT_render.remove(ui.additional_TOPBAR_MT_render_draw)
    TIME_MT_marker.remove(ui.additional_TIME_MT_marker_draw)

    _cls_unregister()
    del Camera.mcr
    del Scene.mcr

    icons.Icons.unregister()
