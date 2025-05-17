# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging
import os

import bpy
from bpy.types import Context, Object, Scene
from bpy.app.handlers import persistent

import bhqmain
import bhqrprt


# DOC_SEQ_RELOAD
def __reload(lc):
    if "handler_load_pre" in lc:
        handler_load_pre(None)


__reload(locals())
del __reload
# \ DOC_SEQ_RELOAD

log = logging.getLogger(__name__)
_dbg = log.debug
_err = log.error


class _BasesData:
    indices: list[int]
    objects: set[Object]

    def __init__(self, initial_index: int):
        self.indices = [initial_index]
        self.objects = set()

    @staticmethod
    def _binary_search_insert_pos(arr, x):
        low = 0
        high = len(arr)

        while low < high:
            mid = (low + high) // 2
            if arr[mid] < x:
                low = mid + 1
            else:
                high = mid
        return low

    def put(self, index: int):
        self.indices.insert(self._binary_search_insert_pos(self.indices, index), index)


class _DirectoryCache:
    directory: str
    bases: dict[str, _BasesData]

    def __init__(self, directory: str):
        self.directory = directory
        self.bases = dict()
        self.update()

    @staticmethod
    def eval_base_and_index(name: str) -> tuple[str, int]:
        if name and name[-4:].lower() == '.obj':
            i = -4
            for char in name[-5::-1]:
                if not char.isnumeric():
                    break
                i -= 1

            if i != -4:
                base = name[0:i]
                index = int(name[i:-4])
            else:
                base = name[:-4]
                index = 0

            return base, index

        return "", -1

    def update(self):
        self.bases.clear()

        if not os.path.isdir(self.directory):
            return

        for name in os.listdir(self.directory):
            base, index = self.eval_base_and_index(name)

            if index != -1:
                if base not in self.bases:
                    self.bases[base] = _BasesData(index)
                else:
                    bases_data = self.bases[base]
                    bases_data.put(index)


class _Cache:
    directories: dict[str, _DirectoryCache]

    def __init__(self):
        self.directories = dict()

    def __repr__(self):
        ret = "Cache:\n"
        for d in self.directories.values():
            ret += f"\tDirectory: \"{d.directory}\"\n"
            for base, bases_data in d.bases.items():
                ret += (
                    f"\t\tBase: \"{base}\"\n"
                    "\t\tObjects:\n"
                )
                for ob in bases_data.objects:
                    ret += f"\t\t\t\"{ob.name_full}\"\n"
                ret += f"\t\tIndices: {', '.join(str(_) for _ in bases_data.indices)}"

        return ret

    def checkout_filepath(self, ob: Object) -> bool:
        fp = ob.mcr.filepath
        # There is also check in `_DirectoryCache.eval_base_and_index` but to improve overall performance, just skip here.
        if not fp:
            return

        base, index = _DirectoryCache.eval_base_and_index(fp)

        if index != -1:
            directory, base = os.path.split(base)

            dir_cache = self.directories.get(directory)
            if not dir_cache:
                dir_cache = _DirectoryCache(directory)
                self.directories[directory] = dir_cache

            bases_data = dir_cache.bases.get(base)
            assert bases_data
            bases_data.objects.add(ob)

            if os.path.isfile(fp):
                return True

        return False


class ObjectSequence(bhqmain.MainChunk['ObjectSequence', 'Context']):
    cache: _Cache
    objects: set[Object]

    def __init__(self, main):
        super().__init__(main)

        self.objects = set()
        self.cache = _Cache()

    def _eval_objects(self, context: Context):
        self.objects = set(
            ob for ob in context.scene.objects
            if (
                ob.type == 'MESH'
                and self.cache.checkout_filepath(ob)
            )
        )
        _dbg(f"Evaluated {len(self.objects)} objects marked as sequence")

    def mark_object(self, ob: Object):
        fp = ob.mcr.filepath

        if self.cache.checkout_filepath(fp):
            self.objects.add(ob)
            _dbg(f"Object {ob.name_full} marked as sequential")

        elif ob in self.objects:
            self.objects.remove(ob)
            _dbg(f"Object {ob.name_full} unmarked as sequential")

    def is_object_a_sequence(self, ob: Object):
        return ob in self.objects

    def invoke(self, context):
        self._eval_objects(context)

        print(self.cache)
        return super().invoke(context)

    def cancel(self, context):

        return super().cancel(context)


@persistent
def handler_load_pre(scene=None):
    if seq_main := ObjectSequence.get_instance():
        if seq_main().cancel(bpy.context) != bhqmain.InvokeState.SUCCESSFUL:
            _err("Object sequence cancel failed")


@persistent
def handler_load_post(scene=None):
    if bpy.app.timers.is_registered(handler_load_post):
        bpy.app.timers.unregister(handler_load_post)

    seq_main = ObjectSequence.create()
    if seq_main().invoke(bpy.context) != bhqmain.InvokeState.SUCCESSFUL:
        _err("Object sequence invoke failed")


def sequence_handlers_reload():
    # Here is a thricky part to handle module reloading. There is a different stages of it, search for "DOC_SEQ_RELOAD"
    bpy.app.timers.register(handler_load_post, first_interval=0.1)


_handlers = (
    (bpy.app.handlers.load_pre, handler_load_pre),
    (bpy.app.handlers.load_post, handler_load_post),
)


def register_mesh_sequence_handlers():
    for handler, callback in _handlers:
        handler.append(callback)


def unregister_mesh_sequence_handlers():
    for handler, callback in reversed(_handlers):
        handler.remove(callback)
