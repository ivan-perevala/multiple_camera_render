# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import os

from typing import Literal

import bhqui4 as bhqui


class Icons:
    cache: None | bhqui.IconsCache = None

    DATA_ICONS_DEFAULT = (
        'render',
        'render_animation',
        'preview',
        'preview_animation',
        'clockwise',
        'counter',
        'visible',
        'selected',
        'credits',
        'info',
        'license',
        'preferences',
        'readme',
        'per_camera',
        'per_camera_dimmed',
        'select_camera',
        'select_camera_dimmed',
    )

    @classmethod
    def register(cls):
        if cls.cache is None:
            cls.cache = bhqui.IconsCache(
                directory=os.path.dirname(__file__),
                data_identifiers=cls.DATA_ICONS_DEFAULT,
            )

    @classmethod
    def unregister(cls) -> None:
        cls.cache = None


IdentifierType = Literal[
    'render',
    'render_animation',
    'preview',
    'preview_animation',
    'clockwise',
    'counter',
    'visible',
    'selected',
    'credits',
    'info',
    'license',
    'preferences',
    'readme',
    'per_camera',
    'per_camera_dimmed',
    'select_camera',
    'select_camera_dimmed',
]


def get_id(identifier: IdentifierType) -> int:
    if Icons.cache:
        return Icons.cache.get_id(identifier)
    return 0
