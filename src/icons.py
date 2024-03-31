from __future__ import annotations

import os
from . import DATA_DIR
from . lib import bhqab

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


class MultipleCameraRenderIcons(bhqab.utils_ui.IconsCache):
    pass


def get_id(identifier: str) -> int:
    MultipleCameraRenderIcons.initialize(
        directory=_ICONS_DIRECTORY,
        data_identifiers=_DATA_ICON_NAMES,
        image_identifiers=(),
    )
    return MultipleCameraRenderIcons.get_id(identifier)
