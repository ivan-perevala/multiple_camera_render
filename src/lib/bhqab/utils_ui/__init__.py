from __future__ import annotations

############################
# Імпорт під час виконання #
############################

# Стандартні бібліотеки
if __debug__:
    from importlib import reload
# Зовнішній пакунок
# Цей пакунок
if __debug__:
    if '_' in locals():
        reload(_unique_name)
        reload(_wrapped_text)
        reload(_developer_extras)
        reload(_progress)
        reload(_icons_cache)
        reload(_preset)
        reload(_localization)
    else:
        _ = None
        from . import _unique_name
        from . import _wrapped_text
        from . import _developer_extras
        from . import _progress
        from . import _icons_cache
        from . import _preset
        from . import _localization
from . _unique_name import *
from . _wrapped_text import *
from . _developer_extras import *
from . _progress import *
from . _icons_cache import *
from . _preset import *
from . _localization import *
# Внутрішній пакунок
# Бібліотеки Blender

##############################
# Імпорт для перевірки типів #
##############################
if __debug__:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        # Стандартні бібліотеки
        # Зовнішній пакунок
        # Цей пакунок
        # Внутрішній пакунок
        # Бібліотеки Blender
        pass

__all__ = (
    # _unique_name
    "eval_unique_name",

    # _wrapped_text
    "eval_text_pixel_dimensions",
    "draw_wrapped_text",

    # _developer_extras
    "developer_extras_poll",
    "template_developer_extras_warning",

    # _progress
    "progress",

    # _icons_cache
    "IconsCache",

    # _preset
    "copy_default_presets_from",
    "template_preset",

    # _localization
    "update_localization",
    "request_localization_from_file",
)
