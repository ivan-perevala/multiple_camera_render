# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations


def __reload_submodules(lc):
    from importlib import reload

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
    if "render_preset" in lc:
        reload(render_preset)
    if "main" in lc:
        reload(main)


__reload_submodules(locals())
del __reload_submodules


from . import chunk_main
from . import chunk_render
from . import chunk_restore
from . import chunk_timers
from . import clockwise_iter
from . import render_preset
from . import main

from . main import RENDER_OT_multiple_camera_render
from . chunk_render import check_handlers_conflicts
from . render_preset import depsgraph_update_pre, depsgraph_update_post

__all__ = (
    # file://./main.py
    "RENDER_OT_multiple_camera_render",
    # file://./chunk_render.py
    "check_handlers_conflicts",
    # file://./render_preset.py
    "depsgraph_update_pre",
    "depsgraph_update_post"
)
