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


__reload_submodules(locals())

from . import pref
from . import scene

from . pref import Preferences
from . scene import SceneProps

__all__ = (
    # file://./pref.py
    "Preferences",
    # file://./scene.py
    "SceneProps"
)
