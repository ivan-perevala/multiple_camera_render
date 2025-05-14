# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging

import bpy
from bpy.types import Context, Object, Scene
from bpy.app.handlers import persistent

import bhqmain
import bhqrprt

log = logging.getLogger(__name__)
_err = log.error


class ObjectSequence(bhqmain.MainChunk['ObjectSequence', 'Context']):

    def __init__(self, main):
        super().__init__(main)

        pass

    def invoke(self, context):

        return super().invoke(context)

    def cancel(self, context):

        return super().cancel(context)


@persistent
def _handler_load_pre(scene: Scene):
    seq_main = ObjectSequence.get_instance()
    if seq_main:
        seq_main().cancel(bpy.context) != bhqmain.InvokeState.SUCCESSFUL:
            _err("Object sequence cancel failed")


@persistent
def _handler_load_post(scene: Scene):
    seq_main = ObjectSequence.create()
    if seq_main().invoke(bpy.context) != bhqmain.InvokeState.SUCCESSFUL:
        _err("Object sequence invoke failed")


_handlers = (
    (bpy.app.handlers.load_pre, _handler_load_pre),
    (bpy.app.handlers.load_post, _handler_load_post),
)


def register_mesh_sequence_handlers():
    for handler, callback in _handlers:
        handler.append(callback)


def unregister_mesh_sequence_handlers():
    for handler, callback in reversed(_handlers):
        handler.remove(callback)
