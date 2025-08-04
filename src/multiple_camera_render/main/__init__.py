# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


def __reload_submodules(lc):
    from importlib import reload

    if "validate_id" in lc:
        reload(validate_id)
    if "register_handlers" in lc:
        reload(register_handlers)
    if "clockwise_iter" in lc:
        reload(clockwise_iter)
    if "markers" in lc:
        reload(markers)

    if "chunk_persistent_main" in lc:
        reload(chunk_persistent_main)
    if "per_camera_data_paths" in lc:
        reload(per_camera_data_paths)
    if "chunk_persistent_per_camera" in lc:
        reload(chunk_persistent_per_camera)

    if "chunk_main" in lc:
        reload(chunk_main)
    if "chunk_render" in lc:
        reload(chunk_render)
    if "chunk_restore" in lc:
        reload(chunk_restore)
    if "chunk_timers" in lc:
        reload(chunk_timers)

    if "per_camera_enable" in lc:
        reload(per_camera_enable)
    if "per_camera_preset" in lc:
        reload(per_camera_preset)
    if "per_camera_dump" in lc:
        reload(per_camera_dump)
    if "per_camera_clear" in lc:
        reload(per_camera_clear)
    if "main" in lc:
        reload(main)


__reload_submodules(locals())
del __reload_submodules


from . import validate_id
from . import register_handlers
from . import clockwise_iter
from . import markers

from . import chunk_persistent_main
from . import per_camera_data_paths
from . import chunk_persistent_per_camera

from . import chunk_main
from . import chunk_render
from . import chunk_restore
from . import chunk_timers

from . import per_camera_enable
from . import per_camera_preset
from . import per_camera_dump
from . import per_camera_clear
from . import main

from . main import RENDER_OT_multiple_camera_render
from . chunk_persistent_main import PersistentMain
from . chunk_persistent_per_camera import PersistentPerCamera
from . per_camera_enable import SCENE_OT_mcr_per_camera_enable
from . per_camera_preset import SCENE_MT_mcr_per_camera_presets, SCENE_OT_mcr_per_camera_preset_add
from . per_camera_dump import OBJECT_OT_per_camera_dump
from . per_camera_clear import OBJECT_OT_per_camera_clear
from . markers import MARKER_create_from_cameras
from . clockwise_iter import CameraUsage, CameraOrder, CameraProperties, FrameUsage

__all__ = (
    # file://./main.py
    "RENDER_OT_multiple_camera_render",
    # file://./chunk_main_persistent.py
    "PersistentMain",
    # file://./chunk_persistent_per_camera.py
    "PersistentPerCamera",
    # file://./per_camera_enable.py
    "SCENE_OT_mcr_per_camera_enable",
    # file://./per_camera_preset.py
    "SCENE_MT_mcr_per_camera_presets",
    "SCENE_OT_mcr_per_camera_preset_add",
    # file://./per_camera_dump.py
    "OBJECT_OT_per_camera_dump",
    # file://./per_camera_clear.py
    "OBJECT_OT_per_camera_clear",
    # file://./markers.py
    "MARKER_create_from_cameras",
    # file://./clockwise_iter.py
    "CameraUsage",
    "CameraOrder",
    "CameraProperties",
    "FrameUsage",
)
