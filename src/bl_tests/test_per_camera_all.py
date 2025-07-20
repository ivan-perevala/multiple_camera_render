# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from . conftest import set_camera_and_update_depsgraph

import bpy
import pytest

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. multiple_camera_render.main import PersistentPerCamera


DATA = {
    "render.resolution_x": (128, 256, 512),
    "render.resolution_y": (512, 256, 128),
    "render.resolution_percentage": (10, 20, 30),
    #
    "render.pixel_aspect_x": (1.0, 2.0, 3.0),
    'render.pixel_aspect_y': (3.0, 2.0, 1.0),
    #
    "render.use_border": (True, False, True),
    "render.use_crop_to_border": (False, True, False),
    #
    "render.fps": (30, 60, 90),
    "render.fps_base": (0.5, 0.7, 1.0),
    #
    "render.use_motion_blur": (True, False, False),
    "render.motion_blur_position": ('START', 'CENTER', 'END'),
    "render.motion_blur_shutter": (0.1, 0.5, 0.9),
    #
    "render.use_simplify": (True, False, True),
    "render.simplify_subdivision": (3, 4, 5),
    "render.simplify_child_particles": (0.1, 0.2, 0.3),
    "render.simplify_volumes": (0.1, 0.2, 0.3),
    "render.simplify_subdivision_render": (20, 30, 40),
    ##
    "view_settings.view_transform": ('AgX', 'Standard', 'Filmic'),
    "view_settings.look": ('None', 'Medium Contrast', 'High Contrast'),
    "view_settings.exposure": (0.1, 0.5, 1.0),
    "view_settings.gamma": (1.0, 1.5, 2.0),
    ##
    "cycles.use_adaptive_sampling": (True, False, True),
    "cycles.samples": (64, 128, 256),
    "cycles.time_limit": (1.1, 2.2, 3.3),
    #
    "cycles.denoiser": ('OPENIMAGEDENOISE', 'OPENIMAGEDENOISE', 'OPENIMAGEDENOISE'), # 'OPTIX' is omitted as far as its not supported for GitHub actions
    #
    "cycles.use_denoising": (False, True, False),
    "cycles.denoising_input_passes": ('RGB', 'RGB_ALBEDO', 'RGB_ALBEDO_NORMAL'),
    #
    "cycles.max_bounces": (12, 6, 3),
    "cycles.diffuse_bounces": (1, 2, 3),
    "cycles.glossy_bounces": (4, 5, 6),
    "cycles.transmission_bounces": (0, 1, 4),
    "cycles.volume_bounces": (2, 1, 9),
    "cycles.transparent_max_bounces": (4, 2, 1),
    #
    "cycles.blur_glossy": (0.1, 0.2, 0.3),
    #
    "cycles.caustics_reflective": (True, False, True),
    "cycles.caustics_refractive": (False, True, False),
    "cycles.use_fast_gi": (True, False, False),
    "cycles.fast_gi_method": ('REPLACE', 'ADD', 'ADD'),
    "cycles.ao_bounces": (0, 1, 3),
    "cycles.ao_bounces_render": (4, 5, 6),
    #
    "cycles.texture_limit": ('128', '256', '512'),
    "cycles.texture_limit_render": ('OFF', '128', '256'),
    ##
    "world": ('World', 'World.001', 'World.002'),
}

def test_all_cases_match_to_addon(multiple_camera_render_module):
    if not TYPE_CHECKING:
        PersistentPerCamera = multiple_camera_render_module.main.PersistentPerCamera

    assert set(PersistentPerCamera.SCENE_DATA_PATHS) == set(DATA.keys())

def test_per_camera_all(multiple_camera_render_module, with_select_camera):
    if not TYPE_CHECKING:
        PersistentPerCamera = multiple_camera_render_module.main.PersistentPerCamera

    context = bpy.context
    scene = context.scene

    scene.mcr.select_camera = with_select_camera

    for data_path, flag_name in PersistentPerCamera.SCENE_FLAG_MAP.items():
        setattr(scene.mcr, flag_name, True)

    for index in range(3):
        set_camera_and_update_depsgraph(index)

        _sentinel = object()

        for data_path, values in DATA.items():
            path_split = PersistentPerCamera.SCENE_DATA_PATHS_SPLIT.get(data_path)
            assert path_split, f"{data_path} is missing path split"

            struct = scene
            for name in path_split[:-1]:
                struct = getattr(struct, name, _sentinel)

                assert struct is not _sentinel, f"Scene structure \"{name}\" is missing for \"{data_path}\""

            attr_name = path_split[-1]

            assert hasattr(struct, attr_name), (
                f"Structure \"{struct}\" of data path \"{data_path}\" is missing attribute \"{attr_name}\""
            )

            curr_value = scene.path_resolve(data_path)
            new_value = values[index]
            if isinstance(curr_value, bpy.types.World):
                new_value = bpy.data.worlds.get(new_value)

            setattr(struct, attr_name, new_value)

    for index in range(3):
        set_camera_and_update_depsgraph(index)

        for data_path, values in DATA.items():
            curr_value = scene.path_resolve(data_path)
            expected_value = values[index]

            if isinstance(curr_value, float):
                curr_value = pytest.approx(curr_value, rel=1e-3)
            elif isinstance(curr_value, bpy.types.World):
                expected_value = bpy.data.worlds[expected_value]

            assert expected_value == curr_value, (
                f"Data path \"{data_path}\" value check failed ({curr_value} (current) != {expected_value} (expected))"
            )
