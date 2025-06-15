# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import importlib


def pytest_addoption(parser):
    parser.addoption(
        "--repo",
        action="store",
        default="user_default",
        help="Override for repository name (default: user_default)",
    )


@pytest.fixture
def repo(request):
    return request.config.getoption("--repo")


@pytest.fixture
def multiple_camera_render_module(repo):
    try:
        return importlib.import_module(f"bl_ext.{repo}.multiple_camera_render")
    except ModuleNotFoundError:
        return None


@pytest.fixture
def test_handler_conflict_multilevel_module(repo):
    try:
        return importlib.import_module(f"bl_ext.{repo}.test_handler_conflict_multilevel")
    except ModuleNotFoundError:
        return None


@pytest.fixture
def test_handler_conflict_one_level_module(repo):
    try:
        return importlib.import_module(f"bl_ext.{repo}.test_handler_conflict_one_level")
    except ModuleNotFoundError:
        return None


@pytest.fixture
def test_handlers_conflict_from_lib_module(repo):
    try:
        return importlib.import_module(f"bl_ext.{repo}.test_handlers_conflict_from_lib")
    except ModuleNotFoundError:
        return None


@pytest.fixture
def handlers_conflict_module():
    try:
        return importlib.import_module("handlers_conflict")
    except ModuleNotFoundError:
        return None
