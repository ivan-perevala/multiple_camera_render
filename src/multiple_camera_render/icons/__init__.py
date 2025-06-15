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
        'conflicting_addons',
        'conflicting_addon',
    )


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
    'conflicting_addons',
    'conflicting_addon',
]


def get_id(identifier: IdentifierType) -> int:
    if Icons.cache is None:
        Icons.cache = bhqui.IconsCache(
            directory=os.path.dirname(__file__),
            data_identifiers=Icons.DATA_ICONS_DEFAULT,
        )

    return Icons.cache.get_id(identifier)
