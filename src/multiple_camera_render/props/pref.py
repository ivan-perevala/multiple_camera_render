# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

from __future__ import annotations

import os
import logging

import bhqrprt4 as bhqrprt
import bhqui4 as bhqui

from bpy.types import AddonPreferences, Context
from bpy.props import EnumProperty, FloatProperty, BoolProperty
import addon_utils

from .. import icons
from .. import main
from .. import ADDON_PKG
assert ADDON_PKG


log = logging.getLogger(__name__)

_CREDITS_TEXT = """
Vladlen Kuzmin (ssh4) - the idea of creating an extension.
Ivan Perevala (ivpe) - engineering, development, maintenance.
"""[1:]


_LICENSE_TEXT = """
Multiple Camera Render addon.
Copyright © 2020-2025 Vladlen Kuzmin (ssh4), Ivan Perevala (ivpe)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""[1:]

_README_TEXT = """
Multiple Camera Render

Extension for sequential rendering from multiple cameras.

You can find all the functionality in Topbar > Render section. There you would find a bunch of operators for rendering and simulating sequential rendering as well as options for running them.

If you have any issues, please, use GitHub issue tracker to submit the issue. It would be nice if you would attach some related log files to tracker.

Thank you for reading and using our software!
"""[1:]


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

    select_camera: BoolProperty(
        default=False,
        options={'SKIP_SAVE'},
        name="Set Selected as Active Camera",
        description="Selecting camera would make it active by default",
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
                    bhqui.draw_wrapped_text(context, col, text=_README_TEXT, text_ctxt='README')

                header, panel = col.panel("mcr_pref_license", default_closed=True)
                header.label(text="License", icon_value=icons.get_id('license'), text_ctxt="Preferences")
                if panel:
                    col = panel.column(align=True)
                    bhqui.draw_wrapped_text(context, col, text=_LICENSE_TEXT, text_ctxt='LICENSE')

                header, panel = col.panel("mcr_pref_credits", default_closed=True)
                header.label(text="Credits", icon_value=icons.get_id('credits'))
                if panel:
                    col = panel.column(align=True)
                    bhqui.draw_wrapped_text(context, col, text=_CREDITS_TEXT, text_ctxt='CREDITS')
