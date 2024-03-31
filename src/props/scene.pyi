from bpy.types import PropertyGroup


class SceneProps(PropertyGroup):
    use_multiple_camera_render: bool
    ".. versionadded:: 3.6.3"
    use_viewport: bool
    ".. versionadded:: 3.6.3"
