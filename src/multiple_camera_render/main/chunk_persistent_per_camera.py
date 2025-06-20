# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, ClassVar

import bpy
from bpy.types import Context, Camera, Scene, Operator, STATUSBAR_HT_header, UILayout
from bpy.props import BoolProperty

import bhqmain4 as bhqmain
import bhqrprt4 as bhqrprt

from .. import icons

if TYPE_CHECKING:
    from . chunk_persistent_main import PersistentMain

log = logging.getLogger(__name__)


class PersistentPerCamera(bhqmain.MainChunk['PersistentMain', 'Context']):

    SCENE_DATA_PATHS: ClassVar[tuple[str, ...]] = (
        #
        "render.resolution_x",
        "render.resolution_y",
        "render.resolution_percentage",
        "render.pixel_aspect_x",
        'render.pixel_aspect_y',
        #
        "render.use_border",
        "render.use_crop_to_border",
        "render.fps",
        "render.fps_base",
        #
        "render.use_motion_blur",
        "render.motion_blur_position",
        "render.motion_blur_shutter",
        #
        "render.use_simplify",
        "render.simplify_subdivision",
        "render.simplify_child_particles",
        "render.simplify_volumes",
        "render.simplify_subdivision_render",
        #
        "view_settings.view_transform",
        "view_settings.look",
        "view_settings.exposure",
        "view_settings.gamma",
        #
        "cycles.use_adaptive_sampling",
        "cycles.samples",
        "cycles.time_limit",
        "cycles.use_denoising",
        "cycles.denoiser",
        "cycles.denoising_input_passes",
        "cycles.max_bounces",
        "cycles.diffuse_bounces",
        "cycles.glossy_bounces",
        "cycles.transmission_bounces",
        "cycles.volume_bounces",
        "cycles.transparent_max_bounces",
        "cycles.blur_glossy",
        "cycles.caustics_reflective",
        "cycles.caustics_refractive",
        "cycles.use_fast_gi",
        "cycles.fast_gi_method",
        "cycles.ao_bounces",
        "cycles.ao_bounces_render",
        "cycles.texture_limit",
        "cycles.texture_limit_render",
        #
        "world",
    )

    _SCENE_DATA_PATHS_SPLIT: ClassVar[dict[str, tuple[str, ...]]] = dict()
    _SCENE_FLAG_MAP: ClassVar[dict[str, str]] = dict()
    _CAMERA_IDPROP_MAP: ClassVar[dict[str, str]] = dict()

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

        return super().invoke(context)

    def cancel(self, context):
        self._unregister_per_camera_handler()
        return super().cancel(context)

    @staticmethod
    def _statusbar_draw_status(self, context):
        layout = self.layout
        layout.label(text="Per Camera Active", icon_value=icons.get_id('per_camera_dimmed'))

    def _register_per_camera_handler(self):
        if self.depsgraph_update_post not in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.append(self.depsgraph_update_post)
            STATUSBAR_HT_header.append(self._statusbar_draw_status)
            log.debug("Handler added to \"depsgraph_update_post\"")

    def _unregister_per_camera_handler(self):
        if self.depsgraph_update_post in bpy.app.handlers.depsgraph_update_post:
            STATUSBAR_HT_header.remove(self._statusbar_draw_status)
            bpy.app.handlers.depsgraph_update_post.remove(self.depsgraph_update_post)
            log.debug("Handler \"depsgraph_update_post\" removed")

    def conditional_handler_register(self, *, scene_props):
        if self.check_scene_props_use_flags(scene_props=scene_props):
            self._register_per_camera_handler()
        else:
            self._unregister_per_camera_handler()

    def depsgraph_update_post(self, scene, dg):
        curr_camera = None
        if scene.camera and scene.camera.type == 'CAMERA':
            curr_camera = scene.camera.data

        if self.prev_camera != curr_camera:
            prev_camera = self.prev_camera
            try:
                getattr(prev_camera, "name_full", None)
            except ReferenceError:
                log.warning("Previous camera data is no longer valid, resetting to None")
                prev_camera = None

            self.prev_camera = curr_camera

            self.on_camera_change(scene, prev_camera, curr_camera)

    def on_camera_change(self, scene: Scene, prev_camera: Camera | None = None, curr_camera: Camera | None = None):
        print(
            f"Camera changed from {prev_camera.name_full if prev_camera else 'None'} "
            f"to: {curr_camera.name_full if curr_camera else 'None'}"
        )

        if prev_camera:
            self.dump_scene_properties_to_camera(scene, prev_camera)

        if curr_camera:
            self.update_scene_properties_from_camera(scene, curr_camera)

    @classmethod
    def eval_scene_flag_name(cls, data_path: str) -> str:
        if name := cls._SCENE_FLAG_MAP.get(data_path):
            return name

        name = f"use_per_camera_{data_path.replace('.', '_')}"
        cls._SCENE_FLAG_MAP[data_path] = name

        return name

    @classmethod
    def eval_camera_idprop_name(cls, data_path: str) -> str:
        if name := cls._CAMERA_IDPROP_MAP.get(data_path):
            return name

        name = data_path.replace('.', '_')
        cls._CAMERA_IDPROP_MAP[data_path] = name

        return name

    @classmethod
    def eval_data_path_split(cls, data_path: str) -> tuple[str, ...]:
        if path_split := cls._SCENE_DATA_PATHS_SPLIT.get(data_path):
            return path_split

        path_split = data_path.split('.')

        cls._SCENE_DATA_PATHS_SPLIT[data_path] = tuple(path_split)

        return path_split

    @classmethod
    def check_scene_props_use_flags(cls, *, scene_props) -> bool:
        for data_path in cls.SCENE_DATA_PATHS:
            if getattr(scene_props, cls.eval_scene_flag_name(data_path), False):
                return True
        return False

    @classmethod
    def eval_scene_flag_properties(cls):
        annotations = dict()

        def _property_update(self, context):
            per_camera = cls.get_instance()
            if per_camera and per_camera():
                per_camera().conditional_handler_register(scene_props=self)

        for data_path in cls.SCENE_DATA_PATHS:
            path_split = cls.eval_data_path_split(data_path)

            item = Scene
            for key in path_split:
                item = item.bl_rna.properties.get(key)
                if key != path_split[-1] and isinstance(item, bpy.types.PointerProperty):
                    item = item.fixed_type

            assert isinstance(item, bpy.types.Property), f"{item} is not a property"

            annotations[cls.eval_scene_flag_name(data_path)] = BoolProperty(
                name=item.name,
                description=item.description,
                update=_property_update,
                options={'SKIP_SAVE'}
            )

        r_type = type("PerCameraProperties", tuple(), dict(__annotations__=annotations))

        return r_type

    def dump_scene_properties_to_camera(self, scene: Scene, cam: Camera):
        for data_path in self.SCENE_DATA_PATHS:
            if scene.mcr.path_resolve(self.eval_scene_flag_name(data_path)):
                value = scene.path_resolve(data_path)
                cam.mcr[self.eval_camera_idprop_name(data_path)] = value

    def update_scene_properties_from_camera(self, scene: Scene, cam: Camera):
        _sentinel = object()

        for data_path in self.SCENE_DATA_PATHS:
            if scene.mcr.path_resolve(self.eval_scene_flag_name(data_path)):
                idprop_name = self.eval_camera_idprop_name(data_path)

                value = cam.mcr.get(idprop_name, _sentinel)
                if value is not _sentinel:
                    path_split = self.eval_data_path_split(data_path)

                    struct = scene
                    for name in path_split[:-1]:
                        struct = getattr(struct, name, _sentinel)

                        if struct is _sentinel:
                            break

                    attr_name = path_split[-1]
                    if struct is not _sentinel:
                        if hasattr(struct, attr_name):
                            setattr(struct, attr_name, value)

    def set_scene_flags_no_update(self, scene: Scene, state: bool):
        for data_path in self.SCENE_DATA_PATHS:
            scene.mcr[self.eval_scene_flag_name(data_path)] = state

        if state:
            self._register_per_camera_handler()
        else:
            self._unregister_per_camera_handler()


class SCENE_OT_mcr_per_camera_enable(Operator):
    bl_idname = "scene.mcr_per_camera_enable"
    bl_label = "Enable"
    bl_options = {'REGISTER'}

    disable: BoolProperty(
        default=False,
        options={'SKIP_SAVE'},
    )

    @classmethod
    def poll(cls, context):
        per_camera = PersistentPerCamera.get_instance()
        return per_camera and per_camera()

    @bhqrprt.operator_report(log)
    def execute(self, context):
        per_camera = PersistentPerCamera.get_instance()

        if per_camera and per_camera():
            per_camera().set_scene_flags_no_update(scene=context.scene, state=not self.disable)

        return {'FINISHED'}
