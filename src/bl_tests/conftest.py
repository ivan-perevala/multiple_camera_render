# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import importlib
import pathlib

import bpy  # pyright: ignore [reportMissingModuleSource]
from bpy.types import Context, Object  # pyright: ignore [reportMissingModuleSource]


def pytest_addoption(parser):
    parser.addoption(
        "--repo",
        action="store",
        default="user_default",
        help="Override for repository name (default: user_default)",
    )

    parser.addoption(
        "--main-tmpdir",
        action="store",
        default="",
        help="Temporary directory which was used by caller test",
    )

    parser.addoption(
        "--with-select-camera",
        action="store_true",
        default=False,
        help="Test with select camera feature",
    )


@pytest.fixture
def repo(request):
    return request.config.getoption("--repo")


@pytest.fixture
def main_tmpdir(request):
    return pathlib.Path(request.config.getoption("--main-tmpdir"))


@pytest.fixture
def with_select_camera(request):
    return request.config.getoption("--with-select-camera")


@pytest.fixture
def multiple_camera_render_module(repo):
    try:
        return importlib.import_module(f"bl_ext.{repo}.multiple_camera_render")
    except ModuleNotFoundError:
        return None


CAMERA_NAMES = (
    "Camera",
    "Camera.001",
    "Camera.002",
)


def update_depsgraph(context: Context):
    dg = context.evaluated_depsgraph_get()
    dg.update()


def get_camera(index: int) -> Object:
    context = bpy.context
    return context.scene.objects[CAMERA_NAMES[index]]


def set_camera_and_update_depsgraph(index: int):
    context = bpy.context
    scene = context.scene
    scene.camera = get_camera(index)

    update_depsgraph(context)


def set_active_object(ob: Object):
    context = bpy.context
    context.view_layer.objects.active = ob
    update_depsgraph(context)
