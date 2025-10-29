# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import hashlib
import json
import os
import typing


import bpy
# NOTE: Cycles is actually an addon, so it imported separately from Blender module
import cycles  # type: ignore

_CACHE_FILE = os.path.join(os.path.dirname(__file__), "out.json")


_STRUCT_NAME_MAP = {
    bpy.types.RenderSettings: "Render",
    cycles.properties.CyclesRenderSettings: "Cycles",
}
"""
Mapping to make label map more readable
"""

_STRUCT_BLACKLIST = (
    bpy.types.BakeSettings,
)
"""
Black list of data structures which should not be processed due to usage of Multiple Camera Render addon
"""

_PROPERTY_TEST_DATA_COUNT = 3
"""
A number of test data values to be generated, for now 3 as far as there is 3 cameras in test files
"""


class RNA_Dump:
    data: dict[typing.Literal['info', 'data'], dict]

    def __init__(self):
        self.data = dict()

    def read_cache(self):
        if os.path.isfile(_CACHE_FILE):
            with open(_CACHE_FILE, 'r') as file:
                self.data = json.load(file)

    def write_cache(self):
        with open(_CACHE_FILE, 'w') as file:
            file.write(json.dumps(self.data, indent=4))

    def _cb_pointer_property(self, prop: bpy.types.PointerProperty):
        pass

    def _cb_bool_property(self, prop: bpy.types.BoolProperty):
        pass

    def _cb_int_property(self, prop: bpy.types.IntProperty):
        pass

    def _cb_float_property(self, prop: bpy.types.FloatProperty):
        pass

    def _cb_string_property(self, prop: bpy.types.StringProperty):
        pass

    def _cb_enum_property(self, prop: bpy.types.EnumProperty):
        pass

    def _recursive_process_rna_item(self, prop: bpy.types.PointerProperty | bpy.types.Property, data_path: list[str], label_path: list[str]):
        if prop.identifier in {'rna_type', 'name'}:
            return

        if prop.type == 'POINTER':
            if prop.is_readonly:
                prop: bpy.types.PointerProperty
                struct = prop.fixed_type

                if type(struct) in _STRUCT_BLACKLIST:
                    return

                label = _STRUCT_NAME_MAP.get(type(prop.fixed_type), prop.name)

                for derived_prop in prop.fixed_type.bl_rna.properties:
                    self._recursive_process_rna_item(
                        derived_prop,
                        data_path + [prop.identifier],
                        label_path + [label]
                    )

        else:
            data_path = '.'.join(data_path + [prop.identifier])
            md5_hash = hashlib.md5(
                bytes(data_path, encoding='utf-8'),
                usedforsecurity=False,
            ).hexdigest()

            _PROPERTY_CALLBACK_MAP = {
                'POINTER': self._cb_pointer_property,
                'BOOLEAN': self._cb_bool_property,
                'INT': self._cb_int_property,
                'FLOAT': self._cb_float_property,
                'STRING': self._cb_string_property,
                'ENUM': self._cb_enum_property,
            }
            test_gen_callback = _PROPERTY_CALLBACK_MAP.get(prop.type)
            if not test_gen_callback:
                print(prop, data_path)

            if not label_path:
                label_path = ["Scene"]

            label = " > ".join(label_path + [prop.name])

            if md5_hash not in self.data['data']:
                self.data["data"][md5_hash] = dict()

            cache_info = self.data["data"][md5_hash]

            cache_info['data_path'] = data_path

            if ((old_label_path := cache_info.get('label_path')) and (old_label_path != label)):
                print(f"Label path for property: \"{data_path}\" has been updated (\"{old_label_path}\" > \"{label}\")")
            cache_info['label_path'] = label

    def dump(self):
        if "info" not in self.data:
            self.data["info"] = dict()
        if "data" not in self.data:
            self.data["data"] = dict()

        struct = bpy.types.Scene

        level_0_props = (
            "frame_current",
            "frame_start",
            "frame_end",
            "frame_step",
            "world",
            "render",
            "view_settings",
            "cycles",
            "eevee",
        )

        for name in level_0_props:
            prop = struct.bl_rna.properties.get(name, None)

            if prop is None:
                # TODO: logging here?
                continue

            data_path = []
            label_path = []

            self._recursive_process_rna_item(prop, data_path, label_path)


def dump():
    rna_dump = RNA_Dump()

    rna_dump.read_cache()

    rna_dump.dump()

    rna_dump.write_cache()
