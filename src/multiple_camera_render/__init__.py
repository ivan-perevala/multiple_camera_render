# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import os
import logging

import bpy
from bpy.props import PointerProperty
from bpy.types import Scene, Object, TOPBAR_MT_render

try:
    from ... import __package__ as ADDON_PKG
except ImportError:
    ADDON_PKG = __package__

import bhqrprt

_CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(_CUR_DIR, "data")

log = logging.getLogger()


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
    props.ObjectProps,
    main.MCR_OT_render,
    ui.MCR_MT_camera_usage,
    ui.MCR_MT_direction,
    ui.OBJECT_PT_mesh_sequence,
)

_cls_register, _cls_unregister = bpy.utils.register_classes_factory(_classes)


@bhqrprt.register_reports(log, props.Preferences, directory=os.path.join(_CUR_DIR, "logs"))
def register():
    _cls_register()
    Scene.mcr = PointerProperty(type=props.SceneProps)
    Object.mcr = PointerProperty(type=props.ObjectProps)
    TOPBAR_MT_render.append(ui.additional_TOPBAR_MT_render_draw)
    main.register_mesh_sequence_handlers()


@bhqrprt.unregister_reports(log)
def unregister():
    main.unregister_mesh_sequence_handlers()
    icons.Icons.cache.release()
    TOPBAR_MT_render.remove(ui.additional_TOPBAR_MT_render_draw)
    _cls_unregister()
    del Scene.mcr
    del Object.mcr
