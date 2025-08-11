# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy  # pyright: ignore [reportMissingModuleSource]

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. multiple_camera_render.main import PersistentPerCamera


def test_per_camera_attr_coverage(multiple_camera_render_module):
    if not TYPE_CHECKING:
        PersistentPerCamera = multiple_camera_render_module.main.PersistentPerCamera

    struct_api_map: dict[str, set[str]] = dict()

    for item in PersistentPerCamera.SCENE_DATA_PATHS_SPLIT.values():
        if len(item) == 2:
            struct_attr, attr = item

            if attributes := struct_api_map.get(struct_attr):
                attributes.add(attr)
            else:
                struct_api_map[struct_attr] = {attr}

    for struct_attr, attributes in struct_api_map.items():
        struct = getattr(bpy.context.scene, struct_attr, None)
        assert struct

        blacklist = {'name', 'rna_type', 'bl_rna', 'register', 'unregister'}

        if struct_attr == 'view_settings':
            blacklist.update({
                # The color which gets mapped to white (automatically converted to/from temperature and tint)
                "white_balance_whitepoint",
                # TODO: Investigate a ways to store curve mapping per camera.
                "curve_mapping",

            })
        elif struct_attr == 'cycles':
            blacklist.update({
                '',
            })
        elif struct_attr == 'render':
            blacklist.update({
                # We dont care about baking options for addon use cases:
                'bake',
                'bake_bias',
                'bake_margin',
                'bake_margin_type',
                'bake_samples',
                'bake_type',
                'bake_user_scale',
                'use_bake_clear',
                'use_bake_lores_mesh',
                'use_bake_multires',
                'use_bake_selected_to_active',
                'use_bake_user_scale',
                # Editor option, would be changed for addon functionality anyway.
                'use_lock_interface',
                # TODO: Investigate a ways to store curve mapping per camera.
                'motion_blur_shutter_curve',
                # Function member.
                'frame_path',
                # Readonly
                'has_multiple_engines',
                'is_movie_format',
                'use_spherical_stereo',
                'stereo_views',
                # TODO: Investigate stereoscopy possibilities.
                'use_multiview',
                'views',
                'views_format',
                # TODO: Investigate this option.
                "sequencer_gl_preview",

            })

        actual_attributes = set(_ for _ in dir(struct) if not (_.startswith('_') or _ in blacklist))

        print(f"{struct_attr}: {len(attributes) / len(actual_attributes) * 100 :.1f} % covered:")
        for _ in sorted(actual_attributes.difference(attributes)):
            print(f"    {_}")
