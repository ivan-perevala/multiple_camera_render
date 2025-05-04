# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import os
import logging

import bpy
from bpy.props import PointerProperty
from bpy.types import Scene, TOPBAR_MT_render

import bhqrprt

_CUR_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(_CUR_DIR, "data")

bhqrprt.setup_logger(directory=os.path.join(_CUR_DIR, "logs"))
log = logging.getLogger()

def get_preferences() -> props.Preferences:
    return bpy.context.preferences.addons[__package__].preferences

def __reload_submodules(lc):
    from importlib import reload
    if "props" in lc:
        reload(props)
    if "ui" in lc:
        reload(ui)
    if "main" in lc:
        reload(main)


__reload_submodules(locals())
del __reload_submodules

from . import props
from . import ui
from . import main


_classes = (
    props.Preferences,
    props.SceneProps,
    main.MCR_OT_render,
)

_cls_register, _cls_unregister = bpy.utils.register_classes_factory(_classes)


def register():
    _cls_register()
    Scene.mcr = PointerProperty(type=props.SceneProps)
    TOPBAR_MT_render.append(ui.additional_TOPBAR_MT_render_draw)

    addon_pref = bpy.context.preferences.addons[__package__].preferences
    addon_pref.log_level = addon_pref.log_level


def unregister():
    TOPBAR_MT_render.remove(ui.additional_TOPBAR_MT_render_draw)
    _cls_unregister()
    del Scene.mcr
    bhqrprt.teardown_logger()
