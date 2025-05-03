# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import logging

import bhqrprt
import bhqui

from bpy.types import AddonPreferences, Context
from bpy.props import EnumProperty

from .. import icons
from .. import __package__ as ADDON_PKG
assert ADDON_PKG


log = logging.getLogger(__name__)


class Preferences(AddonPreferences):
    bl_idname = ADDON_PKG

    info_section: EnumProperty(
        items=(
            (
                'README',
                "Readme",
                "Information about the addon and how to use it",
                icons.get_id("readme"),
                (1 << 0),
            ),
            (
                'CREDITS',
                "Credits",
                "Thanks to those thanks to whom this addon was created and maintained",
                icons.get_id("credits"),
                (1 << 1),
            ),
            (
                'LINKS',
                "Links",
                "Useful links related to this addon",
                icons.get_id("links"),
                (1 << 2),
            ),
            (
                'LICENSE',
                "License",
                "Information about addon license",
                icons.get_id("license"),
                (1 << 3),
            )
        ),  # type: ignore
        update=bhqrprt.update_log_setting_changed(log, "info_section"),
        options={'ENUM_FLAG', 'SKIP_SAVE'},
        translation_context='Preferences',
        name="Info Section",
        description="Sections with information about the addon",
    )

    log_level: bhqrprt.get_prop_log_level(log, identifier="log_level")

    def draw(self, context: Context):
        layout = self.layout
        layout.use_property_split = True

        col = layout.column(align=False)

        bhqrprt.template_ui_draw_paths(log, col, msgctxt="Preferences")

        if bhqui.developer_extras_poll(context):
            header, panel = col.panel("dev_log", default_closed=True)
            header.label(text="Developer Extras", text_ctxt="Preferences")
            header.alert = True
            if panel:
                bhqui.template_developer_extras_warning(context, panel)

                panel.prop(self, "log_level")
