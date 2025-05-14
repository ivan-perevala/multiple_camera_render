# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# NOTE: This file should be used only for development of the extension, never for releases. Even than - here is required
# check if package imported from within Blender. Reason is that, for example, `pytest` would try to import package, but
# as far as there is no `bpy` module available, tests wouldn't run properly.

HAS_BPY = False
try:
    import bpy
except ImportError:
    pass
else:
    if hasattr(bpy, "app"):
        HAS_BPY = True

if HAS_BPY:
    from .src.multiple_camera_render import register, unregister
else:
    def register():
        pass

    def unregister():
        pass
