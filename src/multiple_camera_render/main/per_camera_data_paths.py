# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import ClassVar


class PerCameraDataPaths:
    SCENE_DATA_PATHS_GROUPED: ClassVar[dict[str, list[None | str]]] = {
        "Render": [
            "render.resolution_x",
            "render.resolution_y",
            "render.resolution_percentage",
            None,
            "render.pixel_aspect_x",
            'render.pixel_aspect_y',
            None,
            "render.use_border",
            "render.use_crop_to_border",
            None,
            "render.fps",
            "render.fps_base",
            None,
            "render.use_motion_blur",
            "render.motion_blur_position",
            "render.motion_blur_shutter",
            "cycles.rolling_shutter_type",
            "cycles.rolling_shutter_duration",
            None,
            "render.use_simplify",
            "render.simplify_subdivision",
            "render.simplify_child_particles",
            "render.simplify_volumes",
            "render.simplify_subdivision_render",
            "render.simplify_child_particles_render",
            None,
            "render.simplify_gpencil",
            "render.simplify_gpencil_onplay",
            "render.simplify_gpencil_view_fill",
            "render.simplify_gpencil_modifier",
            "render.simplify_gpencil_shader_fx",
            "render.simplify_gpencil_tint",
            "render.simplify_gpencil_antialiasing",
            None,
            "render.film_transparent",
            None,
            "render.threads_mode",
            "render.threads",
        ],
        "View Settings": [
            "view_settings.view_transform",
            "view_settings.look",
            "view_settings.exposure",
            "view_settings.gamma",
        ],
        "Cycles": [
            # Sampling
            "cycles.use_adaptive_sampling",
            "cycles.adaptive_threshold",
            "cycles.samples",
            "cycles.adaptive_min_samples",
            "cycles.time_limit",
            None,
            # Denoise
            "cycles.use_denoising",
            "cycles.denoiser",
            "cycles.denoising_input_passes",
            "cycles.denoising_prefilter",
            "cycles.denoising_quality",
            "cycles.denoising_use_gpu",
            None,
            # Path Guiding
            "cycles.use_guiding",
            "cycles.guiding_training_samples",
            "cycles.use_surface_guiding",
            "cycles.use_volume_guiding",
            "cycles.use_light_tree",
            "cycles.light_sampling_threshold",
            "cycles.sampling_pattern",
            "cycles.seed",
            "cycles.auto_scrambling_distance",
            "cycles.preview_scrambling_distance",
            "cycles.scrambling_distance",
            "cycles.min_light_bounces",
            "cycles.min_transparent_bounces",
            "cycles.use_sample_subset",
            "cycles.sample_offset",
            "cycles.sample_subset_length",
            None,
            # Light Path
            "cycles.max_bounces",
            "cycles.diffuse_bounces",
            "cycles.glossy_bounces",
            "cycles.transmission_bounces",
            "cycles.volume_bounces",
            "cycles.transparent_max_bounces",
            "cycles.sample_clamp_direct",
            "cycles.sample_clamp_indirect",
            None,
            "cycles.blur_glossy",
            "cycles.caustics_reflective",
            "cycles.caustics_refractive",
            None,
            "cycles.use_fast_gi",
            "cycles.fast_gi_method",
            "cycles.fast_gi_method",
            "cycles.ao_bounces",
            "cycles.ao_bounces_render",
            None,
            # Volumes
            "cycles.volume_step_rate",
            "cycles.volume_max_steps",
            None,
            "cycles_curves.shape",
            "cycles_curves.subdivisions",
            None,
            "cycles.texture_limit",
            "cycles.texture_limit_render",
            "cycles.use_camera_cull",
            "cycles.camera_cull_margin",
            "cycles.use_distance_cull",
            "cycles.distance_cull_margin",
            None,
            # Film
            "cycles.film_exposure",
            "cycles.pixel_filter_type",
            "cycles.filter_width",
            "cycles.film_transparent_glass",
            "cycles.film_transparent_roughness",
            None,
            # Performance
            "cycles.use_auto_tile",
            "cycles.tile_size",
            "cycles.debug_use_spatial_splits",
            "cycles.debug_use_compact_bvh",
            "render.use_persistent_data",
        ],
        "Scene": [
            "world",
            None,
            "frame_start",
            "frame_end",
            "frame_step",
        ],
    }

    SCENE_DATA_PATHS: ClassVar[tuple[str, ...]] = tuple(
        data_path
        for names in SCENE_DATA_PATHS_GROUPED.values()
        for data_path in names
        if data_path is not None
    )

    # NOTE: Evaluated from UI, because Cycles might be registered after Multiple Camera Render or just disabled.
    # Similar behavior might take place if some properties was renames/removed/not exist yet in different Blender
    # versions. That is the only reason why this map is used for UI display and labels not used as `name` argument
    # for `use_per_camera_*`` flag properties.
    SCENE_DATA_PATHS_LABEL_MAP: ClassVar[dict[str, str]] = dict()

    SCENE_DATA_PATHS_SPLIT: ClassVar[dict[str, list[str]]] = {
        data_path: data_path.split('.')
        for data_path in SCENE_DATA_PATHS
    }
    SCENE_FLAG_MAP: ClassVar[dict[str, str]] = {
        data_path: f"use_per_camera_{data_path.replace('.', '_')}"
        for data_path in SCENE_DATA_PATHS
    }
    CAMERA_IDPROP_MAP: ClassVar[dict[str, str]] = {
        data_path: data_path.replace('.', '_')
        for data_path in SCENE_DATA_PATHS
    }
