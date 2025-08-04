# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import bpy
from bpy.types import Context, Camera, Scene
from bpy.props import BoolProperty
import addon_utils

import bhqmain4 as bhqmain

from . register_handlers import register_handler, unregister_handler
from . validate_id import validate_id, validate_camera_object
from . per_camera_data_paths import PerCameraDataPaths

if TYPE_CHECKING:
    from . chunk_persistent_main import PersistentMain

log = logging.getLogger(__name__)


class PersistentPerCamera(bhqmain.MainChunk['PersistentMain', 'Context'], PerCameraDataPaths):
    prev_camera: Camera | None

    def __init__(self, main):
        super().__init__(main)

        self.prev_camera = None

    def invoke(self, context):
        scene = context.scene

        if scene.camera:
            self.prev_camera = scene.camera.data
            log.debug(f"Initial camera: {self.prev_camera.name_full}")
        else:
            log.debug("No initial camera set in the scene")

        self.conditional_handler_register(scene_props=scene.mcr)
        self.register_save_pre_handler()

        return super().invoke(context)

    def cancel(self, context):
        self.unregister_save_pre_handler()
        self.unregister_per_camera_handler()
        return super().cancel(context)

    def register_per_camera_handler(self):
        if register_handler(bpy.app.handlers.depsgraph_update_post, self.depsgraph_update_post):
            log.debug("Handler added to \"depsgraph_update_post\"")

    def unregister_per_camera_handler(self):
        if unregister_handler(bpy.app.handlers.depsgraph_update_post, self.depsgraph_update_post):
            log.debug("Handler \"depsgraph_update_post\" removed")

    def conditional_handler_register(self, *, scene_props):
        for name in self.SCENE_FLAG_MAP.values():
            if getattr(scene_props, name, False):
                self.register_per_camera_handler()
                break
        else:
            self.unregister_per_camera_handler()

    def is_handler_active(self):
        return self.depsgraph_update_post in bpy.app.handlers.depsgraph_update_post

    @staticmethod
    def check_cycles() -> bool:
        loaded_default, loaded_state = addon_utils.check("cycles")
        return loaded_default or loaded_state

    def depsgraph_update_post(self, scene, dg):
        curr_camera = None
        if validate_camera_object(scene.camera):
            curr_camera = scene.camera.data

        if self.prev_camera != curr_camera:
            prev_camera = self.prev_camera

            if not validate_id(prev_camera):
                log.warning("Previous camera data is no longer valid, resetting to None")
                prev_camera = None

            self.prev_camera = curr_camera

            if prev_camera:
                self.dump_scene_properties_to_camera(scene, prev_camera)

            if curr_camera:
                self.update_scene_properties_from_camera(scene, curr_camera)

    @classmethod
    def eval_scene_flag_properties(cls):
        annotations = dict()

        from . chunk_persistent_main import PersistentMain

        def _property_update(self, context):
            pmain = PersistentMain.get_instance()
            if pmain and pmain():
                pmain().per_camera.conditional_handler_register(scene_props=self)

        for data_path, name in cls.SCENE_FLAG_MAP.items():
            annotations[name] = BoolProperty(
                update=_property_update,
                options={'SKIP_SAVE'}
            )

        r_type = type("PerCameraProperties", tuple(), dict(__annotations__=annotations))

        return r_type

    def set_scene_flags_no_update(self, scene: Scene, state: bool):
        for name in self.SCENE_FLAG_MAP.values():
            scene.mcr[name] = state

        if state:
            self.register_per_camera_handler()
        else:
            self.unregister_per_camera_handler()

    @classmethod
    def eval_scene_flag_ui_label(cls, data_path: str) -> None | str:
        if label := cls.SCENE_DATA_PATHS_LABEL_MAP.get(data_path):
            return label

        _sentinel = object()

        item = Scene
        path_split = cls.SCENE_DATA_PATHS_SPLIT[data_path]
        for key in path_split:
            item = item.bl_rna.properties.get(key, _sentinel)

            if item is _sentinel:
                log.debug(f"Item \"{key}\" of data path \"{data_path}\" is missing, would be skipped")
                break

            if key != path_split[-1] and isinstance(item, bpy.types.PointerProperty):
                item = item.fixed_type
        else:
            if isinstance(item, bpy.types.Property):
                label = cls.SCENE_DATA_PATHS_LABEL_MAP[data_path] = item.name
                return label

    @classmethod
    def dump_scene_properties_to_camera(cls, scene: Scene, cam: Camera):
        for data_path, flag_name in cls.SCENE_FLAG_MAP.items():
            if scene.mcr.path_resolve(flag_name):
                idprop_name = cls.CAMERA_IDPROP_MAP[data_path]

                try:
                    value = scene.path_resolve(data_path)
                except ValueError:
                    continue

                cam.mcr[idprop_name] = value

    @classmethod
    def clear_per_camera_data(cls, cam: Camera):
        for data_path, idprop_name in cls.CAMERA_IDPROP_MAP.items():
            if idprop_name in cam.mcr:
                del cam.mcr[idprop_name]

    def update_scene_properties_from_camera(self, scene: Scene, cam: Camera):
        _sentinel = object()

        for data_path, flag_name in self.SCENE_FLAG_MAP.items():
            if scene.mcr.path_resolve(flag_name):
                idprop_name = self.CAMERA_IDPROP_MAP[data_path]

                value = cam.mcr.get(idprop_name, _sentinel)
                if value is not _sentinel:
                    path_split = self.SCENE_DATA_PATHS_SPLIT[data_path]

                    struct = scene
                    for name in path_split[:-1]:
                        struct = getattr(struct, name, _sentinel)

                        if struct is _sentinel:
                            break

                    attr_name = path_split[-1]
                    if struct is not _sentinel:
                        if hasattr(struct, attr_name):
                            setattr(struct, attr_name, value)

    def register_save_pre_handler(self):
        if self.save_pre_handler not in bpy.app.handlers.save_pre:
            bpy.app.handlers.save_pre.append(self.save_pre_handler)

    def unregister_save_pre_handler(self):
        if self.save_pre_handler in bpy.app.handlers.save_pre:
            bpy.app.handlers.save_pre.remove(self.save_pre_handler)

    def save_pre_handler(self, fp, _):
        scene = bpy.context.scene
        camera = scene.camera
        if validate_camera_object(camera):
            self.dump_scene_properties_to_camera(scene, camera.data)
