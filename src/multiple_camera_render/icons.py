# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os

import bhqui

from . import DATA_DIR


_DATA_ICON_NAMES = (
    "credits",
    "github",
    "info",
    "license",
    "links",
    "patreon",
    "preferences",
    "readme",
    "update",
    "youtube",
)

_ICONS_DIRECTORY = os.path.join(DATA_DIR, "icons")


class MultipleCameraRenderIcons(bhqui.IconsCache):
    pass


def get_id(identifier: str) -> int:
    MultipleCameraRenderIcons.initialize(
        directory=_ICONS_DIRECTORY,
        data_identifiers=_DATA_ICON_NAMES,
        image_identifiers=(),
    )
    return MultipleCameraRenderIcons.get_id(identifier)
