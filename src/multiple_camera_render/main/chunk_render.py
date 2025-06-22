# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

from enum import IntEnum, auto
from typing import TYPE_CHECKING
import logging
import math
import numpy as np
import os
import time
import inspect
import importlib

import bpy
from bpy.types import Scene, Context
from mathutils import Vector

import bhqmain4 as bhqmain
import bhqui4 as bhqui

from . chunk_restore import CONFLICTING_HANDLERS
from . clockwise_iter import ClockwiseIterator
from . validate_id import validate_camera_object
from .. import ADDON_PKG

if TYPE_CHECKING:
    from . chunk_main import Main

log = logging.getLogger(__name__)
_dbg = log.debug
_err = log.error
_info = log.info


class RenderStatus(IntEnum):
    NONE = 0
    PREVIEW = auto()
    NEED_LAUNCH = auto()
    RENDERING = auto()
    COMPLETE = auto()
    CANCELLED = auto()


def check_handlers_conflicts() -> tuple[set, set]:
    r_addons = set()
    r_modules = set()

    whitelist = (
        ADDON_PKG.split('.'),
    )

    for handler_name in CONFLICTING_HANDLERS:
        functions = getattr(bpy.app.handlers, handler_name, [])
        for func in functions:
            mod = inspect.getmodule(func)

            pkg = mod.__package__

            if pkg.startswith('bl_ext.'):
                pkg_split = pkg.split('.')

                if pkg_split[0:3] in whitelist:
                    continue

                if len(pkg_split) > 3:
                    try:
                        mod = importlib.import_module(name='.'.join(pkg_split[0:3]))
                    except ModuleNotFoundError:
                        pass

                r_addons.add(mod)

            else:
                r_modules.add(mod)

    return r_addons, r_modules


class Render(bhqmain.MainChunk['Main', 'Context']):
    "Handles render pipeline and camera change."

    camera_iterator: None | ClockwiseIterator

    status: RenderStatus

    _PROGRESS_ID = "mcr"

    def __init__(self, main):
        super().__init__(main)
        self.camera_iterator = None
        self.status = RenderStatus.NONE

    def _eval_render_filename_frame(self, context: Context, name: str) -> str:
        scene = context.scene

        end_index = start_index = name.rfind('#')
        if end_index != -1:
            for i in range(end_index, 0, -1):
                if name[i - 1] != '#':
                    start_index = i
                    break

            digits = end_index - start_index + 1
            name = f"{name[:start_index]}{scene.frame_current:0{digits}d}{name[end_index + 1:]}"
        else:
            name += f"{scene.frame_current:04d}"  # Default behaviour

        return name

    def _eval_render_filepath(self, context: Context):
        scene = context.scene
        camera = scene.camera

        initial_filepath = self.main.restore.render_filepath
        directory, filename = os.path.split(initial_filepath)
        name, ext = os.path.splitext(filename)

        camera_suffix = f"{'_' if name else ''}{camera.name_full}"

        name = f"{name}{camera_suffix}"

        if not self.main.animation and scene.mcr.keep_frame_in_filepath:
            name = self._eval_render_filename_frame(context, name)

        scene.render.filepath = os.path.join(directory, f"{name}{ext}")

    def handler_render_pre(self, scene: Scene, _=None):
        self.status = RenderStatus.RENDERING

    def handler_frame_change(self, scene: Scene, _=None):
        if self.main.preview:
            self.handler_render_post(scene)

    def handler_render_post(self, scene: Scene, _=None):
        context = bpy.context

        def _intern_eval_next_camera():
            next_camera = None

            while True:
                next_camera = next(self.camera_iterator, None)
                if next_camera is None:
                    self.status = RenderStatus.COMPLETE
                    _info("All cameras from initially evaluated has been processed, processing complete.")
                    return

                if validate_camera_object(next_camera):
                    break
                else:
                    _err("Camera from initial array was removed by user")

            if next_camera:
                scene.camera = next_camera
                self._eval_render_filepath(context)
                self.status = RenderStatus.NEED_LAUNCH
                _dbg(f"Updated camera to \"{scene.camera.name_full}\"")

        if self.main.animation:
            if scene.frame_current_final == scene.frame_end:
                _intern_eval_next_camera()
        else:
            _intern_eval_next_camera()

    def handler_render_cancel(self, scene: Scene, _=None):
        self.status = RenderStatus.CANCELLED
        _info("Render has been cancelled by user")

    def handler_animation_playback_post(self, scene: Scene, _=None):
        if self.main.preview:
            self.status = RenderStatus.CANCELLED
            _info("Animation playback has been cancelled by user")

    def handler_load_pre(self, scene: Scene, _=None):
        _info("Cancelling because user loaded new file")
        self.main.cancel(bpy.context)

    def _get_handler_callbacks(self):
        return (
            (bpy.app.handlers.render_pre, self.handler_render_pre),
            (bpy.app.handlers.render_post, self.handler_render_post),
            (bpy.app.handlers.render_cancel, self.handler_render_cancel),
            (bpy.app.handlers.frame_change_pre, self.handler_frame_change),
            (bpy.app.handlers.animation_playback_post, self.handler_animation_playback_post),
            (bpy.app.handlers.load_pre, self.handler_load_pre),
        )

    def _register_handlers(self):
        for bl_handlers, callback in self._get_handler_callbacks():
            if callback not in bl_handlers:
                bl_handlers.append(callback)

    def _unregister_handlers(self):
        for bl_handlers, callback in reversed(self._get_handler_callbacks()):
            if callback in bl_handlers:
                bl_handlers.remove(callback)

    def _eval_cameras(self, context: Context) -> bool:
        _dbg("Evaluating camera queue")

        dt = time.time()

        scene = context.scene
        scene_props = scene.mcr
        curr_camera = scene.camera
        need_switch_camera = False

        match scene_props.cameras_usage:
            case 'VISIBLE':
                objects = context.visible_objects
            case 'SELECTED':
                objects = context.selected_objects
                # Active scene camera might be not in selected objects. In this case, switch required.
                if curr_camera not in objects:
                    need_switch_camera = True

        if not objects:
            return False

        cameras = np.array(objects)

        angles = np.full(len(objects), np.nan, dtype=np.float32)
        for i, ob in enumerate(objects):
            if 'CAMERA' == ob.type:
                x, y = -Vector([ob.matrix_world[0][2], ob.matrix_world[1][2]]).normalized()
                angles[i] = math.atan2(x, y)

        mask = ~np.isnan(angles)
        if not mask.any():
            return False

        indices = np.argsort(angles[mask])
        cameras = cameras[mask][indices]

        if curr_camera is None or curr_camera.type != 'CAMERA' or need_switch_camera:
            # In case of missing active scene camera or active camera is any other object type than 'CAMERA'.
            curr_camera = scene.camera = cameras[0]
            curr_camera_index = 0
        else:
            curr_camera_index = np.argmax(cameras == curr_camera)
        self.camera_iterator = ClockwiseIterator(cameras, curr_camera_index)

        if scene_props.direction == 'COUNTER':
            self.camera_iterator = reversed(self.camera_iterator)

        pop_current_camera = next(self.camera_iterator, None)
        assert pop_current_camera == curr_camera
        self._eval_render_filepath(context)

        if cameras.size:
            _dbg(
                f"Evaluated {cameras.size} cameras (active camera \"{curr_camera.name_full}\", index: {curr_camera_index}) "
                f"in {time.time() - dt:.6f} sec."
            )
            return True
        else:
            _err(f"Missing camera objects, search time {time.time() - dt:.6f}")
            return False

    def launch_render(self, context: Context) -> bool:

        self._increase_progress(context)

        if self.main.preview:
            if self.main.animation:
                if not context.screen.is_animation_playing:
                    scene = context.scene
                    scene.frame_set(scene.frame_start)
                    bpy.ops.screen.animation_play()
            else:
                bpy.ops.screen.frame_offset(delta=0)

            self.status = RenderStatus.PREVIEW
            return True

        res = bpy.ops.render.render(
            'INVOKE_DEFAULT',
            animation=self.main.animation,
            use_viewport=True,
            write_still=True
        )
        return res == {'RUNNING_MODAL'}

    def _setup_progress(self):
        progress = bhqui.progress.get(identifier=self._PROGRESS_ID)
        progress.label = "Multiple Camera Render"
        progress.subtype = 'STEP'
        progress.num_steps = len(self.camera_iterator)

    def _increase_progress(self, context: Context):
        progress = bhqui.progress.get(identifier=self._PROGRESS_ID)
        progress.step += 1
        progress.label = context.scene.camera.name

    def _cancel_progress(self):
        bhqui.progress.complete(identifier=self._PROGRESS_ID)

    def clear_conflicting_handlers(self):
        for handler_name in CONFLICTING_HANDLERS:
            handlers: list = getattr(bpy.app.handlers, handler_name)
            if handlers:
                log.warning(f"Cleared \"{handler_name}\" handlers which may cause incorrect behavior:")
                for handle in handlers:
                    log.warning(f"\t{handle}")

            handlers.clear()

    def invoke(self, context):
        if not self._eval_cameras(context):
            return bhqmain.InvokeState.FAILED

        self.clear_conflicting_handlers()
        self._register_handlers()

        scene = context.scene
        scene.render.use_lock_interface = True

        self.status = RenderStatus.NEED_LAUNCH

        self._setup_progress()

        return super().invoke(context)

    def cancel(self, context):
        self._cancel_progress()
        self._unregister_handlers()

        if self.main.preview and context.screen.is_animation_playing:
            bpy.ops.screen.animation_cancel(restore_frame=True)

        return super().cancel(context)
