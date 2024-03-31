from __future__ import annotations

import os

from .. import langs
from .. import Reports
from .. import (
    ADDON_PKG,
    DATA_DIR
)
from .. lib import bhqab
from .. import icons

from bpy.types import (
    AddonPreferences,
    UILayout,
)
from bpy.props import (
    EnumProperty,
)


class Preferences(AddonPreferences):
    bl_idname = ADDON_PKG

    _update_info_section = Reports.update_log_setting_changed("info_section")

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
        ),
        update=_update_info_section,
        options={'ENUM_FLAG', 'SKIP_SAVE'},
        translation_context='Preferences',
        name="Info Section",
        description="Sections with information about the addon",
    )

    log_level: Reports.prop_log_level

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        def _intern_show_info_section(*, flag: str) -> bool:
            return bhqab.utils_ui.template_disclosure_enum_flag(
                layout=layout, item=self, prop_enum_flag="info_section", flag=flag)

        for flag in ('README', 'CREDITS', 'LICENSE'):
            if _intern_show_info_section(flag=flag):
                text = bhqab.utils_ui.request_localization_from_file(
                    module=ADDON_PKG,
                    langs=langs.LANGS,
                    msgctxt=flag,
                    src=os.path.join(DATA_DIR, f"{flag}.txt"),
                    dst={
                        "uk": os.path.join(DATA_DIR, f"{flag}_uk.txt"),
                    }
                )

                bhqab.utils_ui.draw_wrapped_text(context, layout, text=text, text_ctxt=flag)

        if _intern_show_info_section(flag='LINKS'):
            col = layout.column(align=False)

            col_flow = col.column_flow(columns=3, align=True)

            def _intern_large_url_col(icon: str) -> UILayout:
                col = col_flow.column(align=True)
                box = col.box()
                box.template_icon(icons.get_id(identifier=icon), scale=3.0)
                scol = box.column()
                scol.emboss = 'NONE'
                return scol

            scol = _intern_large_url_col(icon='patreon')
            scol.operator(
                "wm.url_open",
                text="Support Project on Patreon",
                text_ctxt="Preferences"
            ).url = "https://www.patreon.com/BlenderHQ"

            scol = _intern_large_url_col(icon='github')
            scol.operator(
                "wm.url_open",
                text="Project on GitHub",
                text_ctxt="Preferences"
            ).url = "https://github.com/BlenderHQ/multiple_camera_render"

            scol = _intern_large_url_col(icon='youtube')
            scol.operator(
                "wm.url_open",
                text="BlenderHQ on YouTube",
                text_ctxt="Preferences"
            ).url = "https://www.youtube.com/@BlenderHQ"

            Reports.template_ui_draw_paths(col)

        if bhqab.utils_ui.developer_extras_poll(context):
            col = layout.column(align=True)
            bhqab.utils_ui.template_developer_extras_warning(context, col)

            col.prop(self, "log_level")
