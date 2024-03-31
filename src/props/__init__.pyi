from . import scene
from . import pref

import bpy


class Scene(bpy.types.Scene):
    mcr: scene.SceneProps


def register():
    pass


def unregister():
    pass
