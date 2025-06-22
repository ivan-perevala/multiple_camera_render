# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


def __reload_submodules(lc):
    from importlib import reload

    if "validate_id" in lc:
        reload(validate_id)
    if "chunk_main" in lc:
        reload(chunk_main)
    if "chunk_render" in lc:
        reload(chunk_render)
    if "chunk_restore" in lc:
        reload(chunk_restore)
    if "chunk_timers" in lc:
        reload(chunk_timers)
    if "clockwise_iter" in lc:
        reload(clockwise_iter)
    if "chunk_persistent_main" in lc:
        reload(chunk_persistent_main)
    if "chunk_persistent_per_camera" in lc:
        reload(chunk_persistent_per_camera)
    if "main" in lc:
        reload(main)


__reload_submodules(locals())
del __reload_submodules


from . import validate_id
from . import chunk_main
from . import chunk_render
from . import chunk_restore
from . import chunk_timers
from . import clockwise_iter
from . import chunk_persistent_main
from . import chunk_persistent_per_camera
from . import main

from . main import RENDER_OT_multiple_camera_render
from . chunk_render import check_handlers_conflicts
from . chunk_persistent_main import PersistentMain
from . chunk_persistent_per_camera import PersistentPerCamera, SCENE_OT_mcr_per_camera_enable, SCENE_MT_mcr_per_camera_presets, SCENE_OT_mcr_per_camera_preset_add

__all__ = (
    # file://./main.py
    "RENDER_OT_multiple_camera_render",
    # file://./chunk_render.py
    "check_handlers_conflicts",
    # file://./chunk_main_persistent.py
    "PersistentMain",
    # file://./chunk_persistent_per_camera.py
    "PersistentPerCamera",
    "SCENE_OT_mcr_per_camera_enable",
    "SCENE_MT_mcr_per_camera_presets",
    "SCENE_OT_mcr_per_camera_preset_add",
)
