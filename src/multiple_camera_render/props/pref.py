# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import logging
from typing import ClassVar

import bhqrprt4 as bhqrprt
import bhqui4 as bhqui

from bpy.types import AddonPreferences, Context
from bpy.props import EnumProperty, FloatProperty, BoolProperty

from .. import icons
from .. import ADDON_PKG
assert ADDON_PKG


log = logging.getLogger(__name__)


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
    )  # pyright: ignore [reportInvalidTypeForm]

    preview_timestep: FloatProperty(
        options={'SKIP_SAVE'},
        default=0.1,
        min=1e-2,
        max=1.0,
        soft_min=0.1,
        subtype='TIME_ABSOLUTE',
        name="Preview Timestep",
        description="Time step for cameras to be changed in preview mode",
    )  # pyright: ignore [reportInvalidTypeForm]

    select_camera: BoolProperty(
        default=False,
        options={'SKIP_SAVE'},
        name="Set Selected as Active Camera",
        description="Selecting camera would make it active by default",
    )  # pyright: ignore [reportInvalidTypeForm]

    _text_cache: ClassVar[dict[str, str]] = {}

    @classmethod
    def get_text_block(cls, filename: str) -> str:
        if data := cls._text_cache.get(filename):
            return data

        with open(os.path.join(os.path.dirname(__file__), "data", filename), 'r') as file:
            data = cls._text_cache[filename] = file.read()
            return data

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

                header, panel = col.panel("mcr_pref_select_camera", default_closed=False)
                header.label(text="Select Camera", icon_value=icons.get_id('select_camera'))
                if panel:
                    col.prop(self, "select_camera")

            case 'INFO':

                bhqrprt.template_submit_issue(col, url="https://github.com/ivan-perevala/multiple_camera_render/issues")

                header, panel = col.panel("mcr_pref_readme", default_closed=False)
                header.label(text="Readme", icon_value=icons.get_id('readme'))
                if panel:
                    col = panel.column(align=True)
                    bhqui.draw_wrapped_text(context, col, text=self.get_text_block("pref_readme_en_US.txt"))

                header, panel = col.panel("mcr_pref_license", default_closed=True)
                header.label(text="License", icon_value=icons.get_id('license'), text_ctxt="Preferences")
                if panel:
                    col = panel.column(align=True)
                    bhqui.draw_wrapped_text(context, col, text=self.get_text_block("pref_license_en_US.txt"))

                header, panel = col.panel("mcr_pref_credits", default_closed=True)
                header.label(text="Credits", icon_value=icons.get_id('credits'))
                if panel:
                    col = panel.column(align=True)
                    bhqui.draw_wrapped_text(context, col, text=self.get_text_block("pref_credits_en_US.txt"))
