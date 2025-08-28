# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import bpy   # pyright: ignore [reportMissingModuleSource]
from bpy.types import Context, Camera, Scene, Depsgraph, PropertyGroup   # pyright: ignore [reportMissingModuleSource]
from bpy.props import BoolProperty   # pyright: ignore [reportMissingModuleSource]
import addon_utils   # pyright: ignore [reportMissingModuleSource]

import bhqmain4 as bhqmain

from . register_handlers import register_handler, unregister_handler
from . validate_id import validate_id, validate_camera_object
from . per_camera_data_paths import PerCameraDataPaths

if TYPE_CHECKING:
    from . chunk_persistent_main import PersistentMain

log = logging.getLogger(__name__)


class PersistentPerCamera(bhqmain.MainChunk['PersistentMain', 'Context'], PerCameraDataPaths):
    prev_camera: Camera | None

    hash_data_path_map: dict[str, str]
    hash_label_map: dict[str, str]

    def __init__(self, main):
        super().__init__(main)

        self.prev_camera = None
        self.hash_data_path_map = dict()
        self.hash_label_map = dict()

    def invoke(self, context):
        scene = context.scene

        if scene.camera:
            self.prev_camera = scene.camera.data
            log.debug(f"Initial camera: {self.prev_camera.name_full}")
        else:
            log.debug("No initial camera set in the scene")

        self.conditional_handler_register(scene)
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

    def conditional_handler_register(self, scene: Scene):
        for md5_hash in self.DATA_PATHS.keys():
            if getattr(scene.mcr, self.scene_flag_name(md5_hash), False):
                self.register_per_camera_handler()
                break
        else:
            self.unregister_per_camera_handler()

    def is_handler_active(self):
        return self.depsgraph_update_post in bpy.app.handlers.depsgraph_update_post

    @staticmethod
    def scene_flag_name(md5_hash: str) -> str:
        return f"use_per_camera_{md5_hash}"

    @staticmethod
    def camera_idprop_name(md5_hash: str) -> str:
        return f"scene_{md5_hash}"

    @staticmethod
    def md5_hash_from_camera_idprop_name(idprop_name: str) -> str:
        return idprop_name[6:]  # len("scene_")

    def hash_from_data_path(self, data_path: str) -> str:
        if not self.hash_data_path_map:
            self.hash_data_path_map = {
                _data_path: md5_hash for md5_hash, [_label, _data_path, _split] in self.DATA_PATHS.items()
            }

        return self.hash_data_path_map.get(data_path, "")

    def hash_from_label(self, label: str) -> str:
        if not self.hash_label_map:
            self.hash_label_map = {
                _label: md5_hash for md5_hash, [_label, _path, _split] in self.DATA_PATHS.items()
            }

        return self.hash_label_map.get(label, "")

    @staticmethod
    def check_cycles() -> bool:
        loaded_default, loaded_state = addon_utils.check("cycles")
        return loaded_default or loaded_state

    def depsgraph_update_post(self, scene: Scene, dg: Depsgraph):
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

        def _property_update(self: PropertyGroup, context: Context):
            pmain = PersistentMain.get_instance()

            if pmain and pmain():
                scene: Scene = self.id_data
                pmain().per_camera.conditional_handler_register(scene)

            # Resetting search after setting up scene flag.
            wm = context.window_manager
            wm.mcr.scene_per_camera_flag_search = ""

        for md5_hash, [label, _data_path, _path_split] in cls.DATA_PATHS.items():
            annotations[cls.scene_flag_name(md5_hash)] = BoolProperty(
                update=_property_update,
                options={'SKIP_SAVE'},
                name=label,
                description="Enable per-camera value"
            )

        r_type = type("PerCameraProperties", tuple(), dict(__annotations__=annotations))

        return r_type

    def set_scene_flags_no_update(self, scene: Scene, state: bool):
        for md5_hash in self.DATA_PATHS.keys():
            scene.mcr[self.scene_flag_name(md5_hash)] = state

        if state:
            self.register_per_camera_handler()
        else:
            self.unregister_per_camera_handler()

    @classmethod
    def dump_scene_properties_to_camera(cls, scene: Scene, cam: Camera):
        for md5_hash, [_label, data_path, _path_split] in cls.DATA_PATHS.items():
            if scene.mcr.path_resolve(cls.scene_flag_name(md5_hash)):
                idprop_name = cls.camera_idprop_name(md5_hash)

                try:
                    value = scene.path_resolve(data_path)
                except ValueError:
                    log.warning(f"Unable to dump scene data path {data_path} to camera")
                    continue

                cam.mcr[idprop_name] = value

    @classmethod
    def clear_per_camera_data(cls, cam: Camera):
        for md5_hash in cls.DATA_PATHS.keys():
            idprop_name = cls.camera_idprop_name(md5_hash)

            if idprop_name in cam.mcr:
                del cam.mcr[idprop_name]

    def update_scene_properties_from_camera(self, scene: Scene, cam: Camera):
        _sentinel = object()

        for idprop_name in cam.mcr.keys():
            md5_hash = self.md5_hash_from_camera_idprop_name(idprop_name)

            value = cam.mcr.get(idprop_name, _sentinel)
            if value is _sentinel:
                log.warning(f"Unable to get value of \"{idprop_name}\" for camera \"{cam.name}\", skipping")
                continue

            item = self.DATA_PATHS.get(md5_hash, None)
            if item is None:
                log.warning(f"Unknown md5 hash for ID property: {idprop_name}, skipping")
                continue

            if scene.mcr.path_resolve(self.scene_flag_name(md5_hash)):
                path_split = item[2]  # [label, data_path, path_split]

                struct = scene

                for name in path_split[:-1]:
                    struct = getattr(struct, name, _sentinel)

                    if struct is _sentinel:
                        break

                attr_name = path_split[-1]
                if struct is _sentinel:
                    log.warning(f"Sentinel value reached while trying to resolve path: {path_split}, skipping")
                elif hasattr(struct, attr_name):
                    setattr(struct, attr_name, value)
                else:
                    log.warning(f"Struct \"{struct}\" has no attribute to set: {attr_name}")

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
