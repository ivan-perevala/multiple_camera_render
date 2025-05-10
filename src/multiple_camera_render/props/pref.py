# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import os
import logging

import bhqrprt
import bhqui

from bpy.types import AddonPreferences, Context
from bpy.props import EnumProperty, FloatProperty

from .. import icons
from .. import __package__ as ADDON_PKG
assert ADDON_PKG


log = logging.getLogger(__name__)

_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

with open(os.path.join(_DATA_DIR, "LICENSE.txt"), 'r') as file:
    _LICENSE_TEXT = file.read()

with open(os.path.join(_DATA_DIR, "README.txt"), 'r') as file:
    _README_TEXT = file.read()

with open(os.path.join(_DATA_DIR, "CREDITS.txt"), 'r') as file:
    _CREDITS_TEXT = file.read()


class Preferences(AddonPreferences):
    bl_idname = ADDON_PKG

    tab: EnumProperty(
        items=(
            ('GENERAL', 'General', "General extension options", icons.get_id('preferences'), 0),
            ('INFO', 'Info', "Info and useful links", icons.get_id('info'), 1),
        ),
        default='GENERAL',
        options={'HIDDEN', 'SKIP_SAVE'},
        name="Tab",
        description="Active preferences tab",
    )

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

    preview_timestep: FloatProperty(
        options={'SKIP_SAVE'},
        default=0.1,
        min=1e-2,
        max=1.0,
        soft_min=0.1,
        subtype='TIME_ABSOLUTE',
        name="Preview Timestep",
        description="Time step for cameras to be changed in preview mode",
    )

    links: EnumProperty(
        items=(
            ('GITHUB', "Github", "https://github.com/blenderhq", icons.get_id('github'), 1 << 0),
            ('PATREON', "Support project on Patreon", "https://www.patreon.com/BlenderHQ", icons.get_id('patreon'), 1 << 1),
        ),
        default=set(),
        options={'ENUM_FLAG'},
    )

    def draw(self, context: Context):
        layout = self.layout
        layout.use_property_split = True

        row = layout.row()
        row.prop_tabs_enum(self, "tab")

        col = layout.column(align=False)

        match self.tab:
            case 'GENERAL':
                header, panel = col.panel("mcr_pref_preview", default_closed=False)
                header.label(text="Preview", icon_value=icons.get_id('preview'))
                if panel:
                    col.prop(self, "preview_timestep")

            case 'INFO':

                header, panel = col.panel("mcr_pref_readme", default_closed=False)
                header.label(text="Readme", icon_value=icons.get_id('readme'))
                if panel:
                    col = panel.column(align=True)
                    bhqui.draw_wrapped_text(context, col, text=_README_TEXT)

                header, panel = col.panel("mcr_pref_links", default_closed=False)
                header.label(text="Links and Support", icon_value=icons.get_id('links'))
                if panel:
                    col = panel.column(align=True)
                    bhqrprt.template_ui_draw_paths(log, col, msgctxt="Preferences")

                    panel.separator()

                    col = panel.column(align=True)

                    bhqui.draw_wrapped_text(context, col, text="Please, attach log file(s) alongside with issue:")

                    scol = col.column(align=True)
                    scol.alert = True

                    bhqrprt.template_submit_issue(
                        scol,
                        url="https://github.com/BlenderHQ/multiple_camera_render/issues/new/"
                    )

                    props = col.operator('wm.url_open', text="BlenderHQ on Github", icon_value=icons.get_id('github'))
                    props.url = "https://github.com/blenderhq"

                    props = col.operator(
                        'wm.url_open',
                        text="Support project on Patreon",
                        icon_value=icons.get_id('patreon')
                    )
                    props.url = "https://github.com/blenderhq"

                header, panel = col.panel("mcr_pref_license", default_closed=True)
                header.label(text="License", icon_value=icons.get_id('license'), text_ctxt="Preferences")
                if panel:
                    col = panel.column(align=True)
                    bhqui.draw_wrapped_text(context, col, text=_LICENSE_TEXT, text_ctxt="Preferences")

                header, panel = col.panel("mcr_pref_credits", default_closed=True)
                header.label(text="Credits", icon_value=icons.get_id('credits'))
                if panel:
                    col = panel.column(align=True)
                    bhqui.draw_wrapped_text(context, col, text=_CREDITS_TEXT)
