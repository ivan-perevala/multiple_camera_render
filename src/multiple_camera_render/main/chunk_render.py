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

import bpy
from bpy.types import Scene, Context, Camera
from mathutils import Vector

import bhqmain4 as bhqmain
import bhqui4 as bhqui

from . chunk_persistent_main import PersistentMain
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
    NONE = auto()
    NEED_LAUNCH = auto()
    RENDERING = auto()
    COMPLETE = auto()
    CANCELLED = auto()


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

    def cancel_main_on_load_pre(self, scene: Scene, _=None):
        _info("Cancelling because user loaded new file")
        self.main.cancel(bpy.context)

    def mark_render_started_on_render_pre(self, scene: Scene, _=None):
        self.status = RenderStatus.RENDERING

    def mark_need_evaluation_on_render_post(self, scene: Scene, _=None):
        self.status = RenderStatus.NEED_LAUNCH

    def mark_cancelled_on_render_cancel(self, scene: Scene, _=None):
        self.status = RenderStatus.CANCELLED
        _info("Render has been cancelled by user")

    def update_camera_on_first_frame_animation_preview(self, scene: Scene, _=None):
        assert self.main.preview
        assert self.main.animation

        if scene.frame_current == scene.frame_start:
            self.next_camera_update_eval(bpy.context)

    def mark_cancelled_on_animation_playback_post(self, scene: Scene, _=None):
        assert self.main.preview

        self.status = RenderStatus.CANCELLED
        _info("Animation playback has been cancelled by user")

    def get_handler_callbacks(self):
        r_handlers = [(bpy.app.handlers.load_pre, self.cancel_main_on_load_pre),]

        if self.main.preview:
            r_handlers.append((bpy.app.handlers.animation_playback_post,
                              self.mark_cancelled_on_animation_playback_post))
            if self.main.animation:
                r_handlers.append((bpy.app.handlers.frame_change_pre,
                                  self.update_camera_on_first_frame_animation_preview))

        else:
            r_handlers.extend([
                (bpy.app.handlers.render_pre, self.mark_render_started_on_render_pre),
                (bpy.app.handlers.render_post, self.mark_need_evaluation_on_render_post),
                (bpy.app.handlers.render_cancel, self.mark_cancelled_on_render_cancel),
            ])
        return r_handlers

    def register_handlers(self):
        for bl_handlers, callback in self.get_handler_callbacks():
            if callback not in bl_handlers:
                bl_handlers.append(callback)

    def unregister_handlers(self):
        for bl_handlers, callback in reversed(self.get_handler_callbacks()):
            if callback in bl_handlers:
                bl_handlers.remove(callback)

    def eval_cameras(self, context: Context) -> bool:
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

        if not objects:
            return False

        if curr_camera not in objects:
            need_switch_camera = True

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

        if (not validate_camera_object(curr_camera)) or need_switch_camera:
            curr_camera = cameras[0]
            curr_camera_index = 0
        else:
            curr_camera_index = np.argmax(cameras == curr_camera)

        self.camera_iterator = ClockwiseIterator(cameras, curr_camera_index)

        if scene_props.direction == 'COUNTER':
            self.camera_iterator = reversed(self.camera_iterator)

        if cameras.size:
            _dbg(
                f"Evaluated {cameras.size} cameras (active camera \"{curr_camera.name_full}\", index: {curr_camera_index}) "
                f"in {time.time() - dt:.6f} sec."
            )
            return True
        else:
            _err(f"Missing camera objects, search time {time.time() - dt:.6f}")
            return False

    def next_camera_update_eval(self, context: Context) -> bool:
        scene = context.scene

        next_camera = None
        while True:
            next_camera = next(self.camera_iterator, None)
            if next_camera is None:
                self.status = RenderStatus.COMPLETE
                _info("All cameras from initially evaluated has been processed, processing complete.")
                return False

            elif validate_camera_object(next_camera):
                break
            else:
                next_camera = None
                _err("Camera from initial array was removed by user")

        if next_camera is None:
            _info("Unable to get any valid camera from the originally evaluated")
            self.status = RenderStatus.CANCELLED
            return False

        scene.camera = next_camera

        pmain = PersistentMain.get_instance()
        if pmain and pmain():
            pmain().per_camera.update_scene_properties_from_camera(scene, next_camera.data)

        self._eval_render_filepath(context)
        self.increase_progress(context)
        _dbg(f"Updated camera to \"{scene.camera.name_full}\"")

        if self.main.preview:
            for area in context.screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            region.tag_redraw()
        return True

    def launch_render(self, context: Context) -> bool:
        if self.main.preview:
            if not self.main.animation:
                self.next_camera_update_eval(context)

            return True

        if self.next_camera_update_eval(context):
            res = bpy.ops.render.render(
                'INVOKE_DEFAULT',
                animation=self.main.animation,
                use_viewport=True,
                write_still=True
            )

            return next(iter(res)) in {'FINISHED', 'RUNNING_MODAL'}

        return True

    def setup_progress(self):
        progress = bhqui.progress.get(identifier=self._PROGRESS_ID)
        progress.label = "Multiple Camera Render"
        progress.subtype = 'STEP'
        progress.num_steps = len(self.camera_iterator)

    def increase_progress(self, context: Context):
        progress = bhqui.progress.get(identifier=self._PROGRESS_ID)
        progress.step += 1
        progress.label = context.scene.camera.name

    def cancel_progress(self):
        bhqui.progress.complete(identifier=self._PROGRESS_ID)

    def invoke(self, context):
        pmain = PersistentMain.get_instance()
        if pmain and pmain():
            pmain().per_camera.unregister_per_camera_handler()
            pmain().select_camera.unregister_select_camera_handler()

        if not self.eval_cameras(context):
            return bhqmain.InvokeState.FAILED

        self.register_handlers()

        scene = context.scene
        scene.render.use_lock_interface = True

        if self.main.preview:
            if self.main.animation:
                scene.frame_set(scene.frame_start)
                bpy.ops.screen.animation_play()
            else:
                bpy.ops.screen.animation_cancel()

        self.status = RenderStatus.NEED_LAUNCH

        self.setup_progress()

        return super().invoke(context)

    def cancel(self, context):
        self.cancel_progress()
        self.unregister_handlers()

        if self.main.preview and context.screen.is_animation_playing:
            bpy.ops.screen.animation_cancel(restore_frame=True)

        pmain = PersistentMain.get_instance()
        if pmain and pmain():
            scene_props = context.scene.mcr
            pmain().per_camera.conditional_handler_register(scene_props=scene_props)
            pmain().select_camera.conditional_handler_register(scene_props=scene_props)

        return super().cancel(context)
