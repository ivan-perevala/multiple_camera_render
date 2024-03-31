from __future__ import annotations

from .. import Reports

from bpy.types import (
    PropertyGroup,
)
from bpy.props import (
    BoolProperty,
)


class SceneProps(PropertyGroup):

    _update_use_multiple_camera_render = Reports.update_log_setting_changed("use_multiple_camera_render")

    use_multiple_camera_render: BoolProperty(
        update=_update_use_multiple_camera_render,
        default=False,
        options={'SKIP_SAVE'},
        name="Use Multiple Camera Render",
        description="Render animation from multiple cameras for each frame",
    )

    _update_use_viewport = Reports.update_log_setting_changed("use_viewport")

    use_viewport: BoolProperty(
        update=_update_use_viewport,
        default=False,
        options={'SKIP_SAVE'},
        name="Use in Viewport",
        description="Show how cameras would be changed on frame change in viewport",
    )
