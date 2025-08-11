# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from . conftest import set_camera_and_update_depsgraph

import bpy  # pyright: ignore [reportMissingModuleSource]
import pytest

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. multiple_camera_render.main import PersistentPerCamera


DATA = {
    'cycles.sampling_pattern': ('AUTOMATIC', 'TABULATED_SOBOL', 'BLUE_NOISE'),
    'render.pixel_aspect_y': (3.0, 2.0, 1.0),
    "cycles_curves.shape": ('RIBBONS', 'THICK', 'RIBBONS'),
    "cycles_curves.subdivisions": (1, 2, 3),
    "cycles.adaptive_min_samples": (10, 20, 30),
    "cycles.adaptive_threshold": (0.01, 0.03, 0.07),
    "cycles.ao_bounces_render": (4, 5, 6),
    "cycles.ao_bounces": (0, 1, 3),
    "cycles.auto_scrambling_distance": (True, False, True),
    "cycles.blur_glossy": (0.1, 0.2, 0.3),
    "cycles.camera_cull_margin": (0.2, 0.5, 0.7),
    "cycles.caustics_reflective": (True, False, True),
    "cycles.caustics_refractive": (False, True, False),
    "cycles.debug_use_compact_bvh": (True, False, True),
    "cycles.debug_use_spatial_splits": (True, False, True),
    # 'OPTIX' is omitted as far as its not supported for GitHub actions.
    "cycles.denoiser": ('OPENIMAGEDENOISE', 'OPENIMAGEDENOISE', 'OPENIMAGEDENOISE'),
    "cycles.denoising_input_passes": ('RGB', 'RGB_ALBEDO', 'RGB_ALBEDO_NORMAL'),
    "cycles.denoising_prefilter": ('NONE', 'FAST', 'ACCURATE'),
    "cycles.denoising_quality": ('HIGH', 'BALANCED', 'FAST'),
    "cycles.denoising_use_gpu": (True, False, True),
    "cycles.diffuse_bounces": (1, 2, 3),
    "cycles.distance_cull_margin": (50, 70, 80),
    "cycles.fast_gi_method": ('REPLACE', 'ADD', 'ADD'),
    "cycles.film_exposure": (1.0, 1.1, 1.2),
    "cycles.film_transparent_glass": (True, False, True),
    "cycles.film_transparent_roughness": (0.1, 0.2, 0.3),
    "cycles.filter_width": (1.6, 1.8, 2.0),
    "cycles.glossy_bounces": (4, 5, 6),
    "cycles.guiding_training_samples": (0, 128, 256),
    "cycles.light_sampling_threshold": (0.01, 0.03, 0.08),
    "cycles.max_bounces": (12, 6, 3),
    "cycles.min_light_bounces": (0, 1, 2),
    "cycles.min_transparent_bounces": (0, 1, 2),
    "cycles.pixel_filter_type": ('BOX', 'GAUSSIAN', 'BLACKMAN_HARRIS'),
    "cycles.preview_scrambling_distance": (True, False, True),
    "cycles.rolling_shutter_duration": (0.1, 0.3, 0.8),
    "cycles.rolling_shutter_type": ('NONE', 'TOP', 'NONE'),
    "cycles.sample_clamp_direct": (0.0, 0.5, 1.0),
    "cycles.sample_clamp_indirect": (0.1, 0.2, 0.3),
    "cycles.sample_offset": (0, 1, 2),
    "cycles.sample_subset_length": (512, 1024, 2048),
    "cycles.samples": (64, 128, 256),
    "cycles.scrambling_distance": (0.1, 0.2, 0.3),
    "cycles.seed": (0, 10, 20),
    "cycles.texture_limit_render": ('OFF', '128', '256'),
    "cycles.texture_limit": ('128', '256', '512'),
    "cycles.tile_size": (64, 128, 256),
    "cycles.time_limit": (1.1, 2.2, 3.3),
    "cycles.transmission_bounces": (0, 1, 4),
    "cycles.transparent_max_bounces": (4, 2, 1),
    "cycles.use_adaptive_sampling": (True, False, True),
    "cycles.use_auto_tile": (True, False, True),
    "cycles.use_camera_cull": (True, False, True),
    "cycles.use_denoising": (False, True, False),
    "cycles.use_distance_cull": (True, False, True),
    "cycles.use_fast_gi": (True, False, False),
    "cycles.use_guiding": (True, False, True),
    "cycles.use_light_tree": (True, False, True),
    "cycles.use_sample_subset": (True, False, True),
    "cycles.use_surface_guiding": (True, False, True),
    "cycles.use_volume_guiding": (True, False, True),
    "cycles.volume_bounces": (2, 1, 9),
    "cycles.volume_max_steps": (64, 128, 512),
    "cycles.volume_step_rate": (0.1, 1.0, 10.0),
    "frame_end": (100, 200, 300),
    "frame_start": (10, 20, 30),
    "frame_step": (1, 2, 3),
    "render.film_transparent": (True, False, True),
    "render.fps_base": (0.5, 0.7, 1.0),
    "render.fps": (30, 60, 90),
    "render.motion_blur_position": ('START', 'CENTER', 'END'),
    "render.motion_blur_shutter": (0.1, 0.5, 0.9),
    "render.pixel_aspect_x": (1.0, 2.0, 3.0),
    "render.resolution_percentage": (10, 20, 30),
    "render.resolution_x": (128, 256, 512),
    "render.resolution_y": (512, 256, 128),
    "render.simplify_child_particles_render": (0.1, 0.2, 0.8),
    "render.simplify_child_particles": (0.1, 0.2, 0.3),
    "render.simplify_gpencil_antialiasing": (True, False, True),
    "render.simplify_gpencil_modifier": (True, False, True),
    "render.simplify_gpencil_onplay": (True, False, True),
    "render.simplify_gpencil_shader_fx": (True, False, True),
    "render.simplify_gpencil_tint": (True, False, True),
    "render.simplify_gpencil_view_fill": (True, False, True),
    "render.simplify_gpencil": (True, False, True),
    "render.simplify_subdivision_render": (20, 30, 40),
    "render.simplify_subdivision": (3, 4, 5),
    "render.simplify_volumes": (0.1, 0.2, 0.3),
    # NOTE: 'AUTO' is skipped because no known number of threads on test machine.
    "render.threads_mode": ('FIXED', 'FIXED', 'FIXED'),
    "render.threads": (1, 2, 3),
    "render.use_border": (True, False, True),
    "render.use_crop_to_border": (False, True, False),
    "render.use_motion_blur": (True, False, False),
    "render.use_persistent_data": (True, False, True),
    "render.use_simplify": (True, False, True),
    "view_settings.exposure": (0.1, 0.5, 1.0),
    "view_settings.gamma": (1.0, 1.5, 2.0),
    # NOTE: 'Standard' is always last one.
    "view_settings.view_transform": ('AgX', 'Filmic', 'Standard'),
    # NOTE: This is dependent from 'view_settings.view_transform', so always after it.
    "view_settings.look": ('None', 'Medium Contrast', 'High Contrast'),
    "world": ('World', 'World.001', 'World.002'),
    # Requires HDR monitor, but test environment is running in background mode, so no monitor available at all.
    "render.use_hdr_view": (False, False, False),
    "render.use_white_balance": (True, False, True),
    "render.white_balance_tint": (50, 60, 70),
    "render.white_balance_temperature": (5000, 6000, 7000),
    "render.use_curve_mapping": (True, False, True),
    "render.use_stamp": (True, False, True),
    "render.use_stamp_camera": (True, False, True),
    "render.use_stamp_date": (True, False, True),
    "render.use_stamp_filename": (True, False, True),
    "render.use_stamp_frame": (True, False, True),
    "render.use_stamp_frame_range": (True, False, True),
    "render.use_stamp_hostname": (True, False, True),
    "render.use_stamp_labels": (True, False, True),
    "render.use_stamp_lens": (True, False, True),
    "render.use_stamp_marker": (True, False, True),
    "render.use_stamp_memory": (True, False, True),
    "render.use_stamp_note": (True, False, True),
    "render.use_stamp_render_time": (True, False, True),
    "render.use_stamp_scene": (True, False, True),
    "render.use_stamp_sequencer_strip": (True, False, True),
    "render.use_stamp_time": (True, False, True),
    "render.stamp_background": ((1.0, 0.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0), (0.0, 0.0, 1.0, 1.0)),
    "render.stamp_font_size": (12, 14, 18),
    "render.stamp_foreground": ((0.0, 1.0, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), (1.0, 0.0, 1.0, 1.0)),
    "render.stamp_note_text": ("A", "B", "C"),
    "render.border_max_x": (0.5, 0.6, 0.7),
    "render.border_max_y": (0.5, 0.6, 0.7),
    "render.border_min_x": (0.1, 0.2, 0.3),
    "render.border_min_y": (0.1, 0.2, 0.3),
    "render.engine": ('CYCLES', 'EEVEE', 'CYCLES'),
    "render.use_sequencer": (True, False, True),
    "render.use_compositing": (True, False, True),
    "render.dither_intensity": (0.1, 0.2, 0.3),
    # No GPU on CI platforms
    "render.compositor_denoise_device": ('CPU', 'CPU', 'CPU'),
    "render.compositor_denoise_final_quality": ('HIGH', 'BALANCED', 'FAST'),
    "render.compositor_denoise_preview_quality": ('HIGH', 'BALANCED', 'FAST'),
    # No GPU on CI platforms
    "render.compositor_device": ('CPU', 'CPU', 'CPU'),
    "render.compositor_precision": ('AUTO', 'FULL', 'AUTO'),
    "render.frame_map_new": (50, 100, 150),
    "render.frame_map_old": (80, 120, 170),
    "render.use_single_layer": (True, False, True),
    "render.filepath": ("A", "B", "C"),
    "render.file_extension": ("PNG", "BMP", "PNG"),
    "render.filter_size": (1.5, 1.8, 2.0),
    "render.preview_pixel_size": ('1', '2', '4'),
    "render.hair_subdiv": (0, 1, 2),
    "render.hair_type": ('STRAND', 'STRIP', 'STRAND'),
    "render.use_freestyle": (True, False, True),
    # Line thickness is dependent, so only Absolute used for testing.
    "render.line_thickness_mode": ('ABSOLUTE', 'ABSOLUTE', 'ABSOLUTE'),
    "render.line_thickness": (1.0, 2.0, 3.0),
    "render.use_file_extension": (True, False, True),
    "render.use_render_cache": (True, False, True),
    "render.use_overwrite": (True, False, True),
    "render.use_placeholder": (True, False, True),
    "render.ppm_factor": (72.0, 96.0, 76.0),
    "render.ppm_base": (1.0, 2.0, 3.0),
    "render.metadata_input": ('SCENE', 'STRIPS', 'SCENE'),
    "render.use_sequencer_override_scene_strip": (True, False, True),
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
