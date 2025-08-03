# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


def __reload_submodules(lc):
    from importlib import reload

    if "pref" in lc:
        reload(pref)
    if "scene" in lc:
        reload(scene)
    if "camera" in lc:
        reload(camera)
    if "wm" in lc:
        reload(wm)


__reload_submodules(locals())

from . import pref
from . import scene
from . import camera
from . import wm

from . pref import Preferences
from . scene import SceneProps
from . camera import CameraProps
from . wm import WMProps

__all__ = (
    # file://./pref.py
    "Preferences",
    # file://./scene.py
    "SceneProps",
    # file://./camera.py
    "CameraProps",
    # file://./wm.py
    "WMProps",
)
