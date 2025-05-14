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
    if "main" in lc:
        reload(main)
    if "chunk_object_sequence" in lc:
        reload(chunk_object_sequence)


__reload_submodules(locals())
del __reload_submodules


from . import chunk_main
from . import chunk_render
from . import chunk_restore
from . import chunk_timers
from . import clockwise_iter
from . import main
from . import chunk_object_sequence

from . main import MCR_OT_render
from . chunk_object_sequence import ObjectSequence, register_mesh_sequence_handlers, unregister_mesh_sequence_handlers

__all__ = (
    # file://./main.py
    "MCR_OT_render",
    # file://./chunk_object_sequence.py
    "ObjectSequence",
    "register_mesh_sequence_handlers",
    "unregister_mesh_sequence_handlers",
)
