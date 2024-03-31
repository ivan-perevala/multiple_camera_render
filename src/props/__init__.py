from __future__ import annotations

if "bpy" in locals():
    from importlib import reload

    reload(pref)
else:
    from . import scene
    from . import pref

import bpy
from bpy.props import PointerProperty

_classes = (
    pref.Preferences,
    scene.SceneProps,
)

_cls_register, _cls_unregister = bpy.utils.register_classes_factory(_classes)


def register():
    _cls_register()

    bpy.types.Scene.mcr = PointerProperty(
        type=scene.SceneProps,
        options={'HIDDEN'},
    )


def unregister():
    del bpy.types.Scene.mcr

    _cls_unregister()
