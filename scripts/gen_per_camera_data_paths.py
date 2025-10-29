# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import bpy
import hashlib
import os
from datetime import datetime
from pathlib import Path
import random
import string

LEVEL0_SCENE_DATA_PATH_MAP: dict[str, tuple[str, ...]] = {
    "Scene": (
        # NOTE: Only a few scene properties are related to addon functionality, so they are written manually.
        # The rest of properties are contained in read-only pointer properties, such as scene.render.*, scene.cycles.*,
        # ect.
        "frame_current",
        "frame_start",
        "frame_end",
        "frame_step",
        "world"
    ),
    "Render": ("render",),
    "View Settings": ("view_settings",),
    "Cycles": ("cycles",),
    "Eevee": ("eevee",),
}

GEN_FILE_HEADER = f"""
# SPDX-FileCopyrightText: {datetime.now().year} Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

#############################################################
# This file is auto-generated, please, do not edit manually #
#############################################################
""".rstrip()

CURR_FILE = Path(__file__)
CURR_DIR = CURR_FILE.parent
ROOT_DIR = CURR_DIR.parent

MCR_DATA_PATH_FILE = ROOT_DIR / "src" / "multiple_camera_render" / "main" / "per_camera_data_paths.py"
TEST_DATA_PATH_FILE = ROOT_DIR / "src" / "bl_tests" / "per_camera_data_paths.py"

PerCameraPropsType = dict[str, tuple[str, str, list[str]]]
PerCameraPropsTestType = dict[str, tuple[bool, int, float, str]]
StatsType = dict[str, int]


def _test_data_enum_property(prop: bpy.types.EnumProperty, k: int) -> None | tuple[tuple[str, ...], tuple[str, ...]]:
    enum_items = tuple(_.identifier for _ in prop.enum_items_static)
    num_items = len(enum_items)

    if not num_items:
        return None, tuple()
    elif num_items == k:
        return enum_items, enum_items
    elif num_items > k:
        return enum_items[:k], enum_items
    else:
        quotient, remainder = divmod(k, num_items)
        items = list(enum_items)
        return tuple(items * quotient + items[:remainder]), enum_items


def _test_data_numeric_property(prop: bpy.types.IntProperty | bpy.types.FloatProperty, k: int) -> None | tuple[tuple[tuple[int | float, ...] | tuple[tuple[int | float, ...]]], tuple[int, int]] | tuple[float | float]:
    match prop.type:
        case 'INT':
            rand = random.randint
        case 'FLOAT':
            rand = random.uniform

    if prop.is_array:
        return tuple(
            tuple((rand(prop.soft_min, prop.soft_max) for _ in range(prop.array_length)))
            for __ in range(k)
        )
    else:
        return tuple((rand(prop.soft_min, prop.soft_max)) for _ in range(k))


def _test_data_bool_property(prop: bpy.types.BoolProperty, k: int) -> None | tuple[tuple[bool, ...], None]:
    if prop.is_array:
        return tuple(
            tuple(random.choice([True, False]) for _ in range(prop.array_length))
            for __ in range(k)
        ), None
    else:
        return tuple(random.choice([True, False]) for _ in range(k)), None


def _test_data_string_property(prop: bpy.types.StringProperty, k: int) -> None | tuple[tuple[str, ...], int]:
    length = min(32, prop.length_max)
    return tuple(
        ''.join(tuple(random.choice(string.ascii_letters) for _ in range(length)))
        for __ in range(k)
    ), prop.length_max


def _test_data_pointer_property(prop: bpy.types.PointerProperty, k: int) -> None | tuple[tuple[str, ...], int]:
    if type(prop.fixed_type) == bpy.types.World:
        assert k == 3

        available_worlds = ('World', 'World.001', 'World.002')

        return available_worlds
    else:
        raise NotImplementedError(
            "Please, manually adjust test file scene and test file generator, pointer properties require more attention"
        )


_TEST_DATA_CALLBACKS = {
    'ENUM': _test_data_enum_property,
    'FLOAT': _test_data_numeric_property,
    'INT': _test_data_numeric_property,
    'BOOLEAN': _test_data_bool_property,
    'STRING': _test_data_string_property,
    'POINTER': _test_data_pointer_property,
}

def a():
    struct = bpy.types.Scene

    def _eval(struct: bpy.types.Struct):
        struct.bl_rna.properties



def evaluate_scene_properties_data(scene_attributes: dict[str, tuple[str, ...]], test_camera_count: int) -> tuple[PerCameraPropsType, StatsType, PerCameraPropsTestType]:
    context = bpy.context

    scene = context.scene

    struct_blacklist = {
        bpy.types.BakeSettings,
        bpy.types.World,
    }

    per_camera_props: PerCameraPropsType = dict()

    per_camera_props_test: dict[str, tuple[bool, int, float, str]] = dict()

    stats: StatsType = dict()

    def _eval_scene_data_path_members_grouped(*, struct: bpy.types.Struct, data_path: list[str], labels: list[str]):
        nonlocal per_camera_props, stats

        print(bpy.types.Scene.bl_rna.properties.get("render"))

        return 

        section_label = ' > '.join(labels)
        if not section_label in stats:
            stats[section_label] = 0

        derived_pointer_properties = []

        def _process_property(prop: bpy.types.Property):
            if prop.identifier in {'rna_type', 'name'}:
                return

            if prop.type == 'POINTER' and prop.is_readonly:
                derived_pointer_properties.append(prop)
            elif not prop.is_readonly:
                path_split = data_path + [prop.identifier]
                path = '.'.join(path_split)
                label = f"{section_label}: {prop.name}"
                md5_hash = hashlib.md5(
                    bytes(path, encoding='utf-8'),
                    usedforsecurity=False
                ).hexdigest()

                per_camera_props[md5_hash] = (label, path, path_split)
                stats[section_label] += 1

                test_data_func = _TEST_DATA_CALLBACKS.get(prop.type, None)

                if test_data_func:
                    test_data = test_data_func(prop, test_camera_count)
                    if test_data:
                        per_camera_props_test[prop.identifier] = test_data
                    else:
                        pass  # TODO: Log?
                else:
                    print(prop.type, prop.identifier)

        struct_prop = struct.bl_rna.properties.get(data_path[-1])
        _process_property(struct_prop)

        for prop in derived_pointer_properties:
            prop: bpy.types.PointerProperty

            print(prop.fixed_type.bl_rna.properties)

        # structs_section_label = ' > '.join(labels)

        # if not structs_section_label in stats:
        #     stats[structs_section_label] = 0

        # attr = getattr(struct, data_path[-1], None)

        # pointer_props = []

        # if attr is None or type(attr) in struct_blacklist:
        #     return
        # elif hasattr(attr, "bl_rna"):
        #     attr: bpy.types.Struct

        #     for prop in attr.bl_rna.properties:
        #         _process_property(prop)
        # else:
        #     #assert hasattr(struct, "bl_rna")
        #     prop = struct.bl_rna.properties.get(data_path[-1])
        #     print(prop)
        #     #_process_property(prop)

        # for prop in pointer_props:
        #     _eval_scene_data_path_members_grouped(
        #         struct=attr,
        #         data_path=data_path + [prop.identifier],
        #         labels=labels + [prop.name]
        #     )

    for section_label, attributes in scene_attributes.items():
        for name in attributes:
            _eval_scene_data_path_members_grouped(struct=scene, data_path=[name], labels=[section_label])

    return per_camera_props, stats, per_camera_props_test


def write_module(per_camera_props: PerCameraPropsType, stats: StatsType):
    gen_script_rel_path = os.path.relpath(CURR_FILE, start=MCR_DATA_PATH_FILE.parent).replace('\\', '/')

    module_code = GEN_FILE_HEADER + f"""
# Generated using file://./{gen_script_rel_path}
# Blender {bpy.app.version_string}

# Generator stats:

"""

    total = 0
    for structs_section_label, count in stats.items():
        module_code += f"# {structs_section_label}: {count} prop{'s'[:count^1]}\n"
        total += count

    module_code += f"""
# Total: {total} properties
    """.rstrip()

    module_code += """

from __future__ import annotations

class PerCameraDataPaths:
    DATA_PATHS = {
""".rstrip()

    with open(str(MCR_DATA_PATH_FILE.resolve()), 'w') as file:
        file.write(module_code)

        for md5_hash, [label, data_path, path_split] in per_camera_props.items():
            item_format = f"""
        "{md5_hash}": (
            "{label}",
            "{data_path}",
            {path_split}
        ),
""".rstrip()

            file.write(item_format)

        file.write("\n    }")


def write_tests_data_file(per_camera_props_test: PerCameraPropsTestType):
    gen_script_rel_path = os.path.relpath(CURR_FILE, start=TEST_DATA_PATH_FILE.parent).replace('\\', '/')

    with open(TEST_DATA_PATH_FILE, 'w') as file:
        file.write(
            GEN_FILE_HEADER + f"""

# Generated using file://./{gen_script_rel_path}

""" + """
DATA = {
""".rstrip()
        )

        for data_path, items in per_camera_props_test.items():
            file.write(f"""
    "{data_path}": {items},
""".rstrip()
            )

        file.write("\n}")


if __name__ == '__main__':

    a()

    # per_camera_props, stats, per_camera_props_test = evaluate_scene_properties_data(LEVEL0_SCENE_DATA_PATH_MAP, 3)
    # write_module(per_camera_props, stats)
    # write_tests_data_file(per_camera_props_test)
