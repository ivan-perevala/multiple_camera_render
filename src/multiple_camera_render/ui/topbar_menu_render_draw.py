# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from bpy.types import Panel, Context, UILayout

from .. import main
from .. import icons

from . import options_panel
from . import per_camera_panel


def additional_TOPBAR_MT_render_draw(self: Panel, context: Context):
    layout = self.layout
    layout.separator()

    col = layout.column()
    col.operator_context = 'INVOKE_DEFAULT'

    scene = context.scene
    scene_props = scene.mcr

    col.operator(
        operator=main.RENDER_OT_multiple_camera_render.bl_idname,
        text="Render Multiple Cameras",
        icon_value=icons.get_id('render'),
    )

    props: main.RENDER_OT_multiple_camera_render = col.operator(
        operator=main.RENDER_OT_multiple_camera_render.bl_idname,
        text="Render Animation from Multiple Cameras",
        icon_value=icons.get_id('render_animation'),
    )
    props.animation = True

    props: main.RENDER_OT_multiple_camera_render = col.operator(
        operator=main.RENDER_OT_multiple_camera_render.bl_idname,
        text="Preview",
        icon_value=icons.get_id('preview'),
    )
    props.preview = True

    props: main.RENDER_OT_multiple_camera_render = col.operator(
        operator=main.RENDER_OT_multiple_camera_render.bl_idname,
        text="Preview Animation",
        icon_value=icons.get_id('preview_animation'),
    )
    props.preview = True
    props.animation = True

    attr = "usage"
    icon_value = col.enum_item_icon(scene_props, attr, getattr(scene_props, attr))

    col.popover(panel=options_panel.MCR_PT_options.__name__, icon_value=icon_value)
    col.popover(panel=per_camera_panel.MCR_PT_scene_use_per_camera.__name__, icon_value=icons.get_id('per_camera'))
