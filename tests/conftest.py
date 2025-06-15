# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import shutil
import os
import pathlib


def pytest_addoption(parser):
    parser.addoption("--blender", action="store", default="", help="Override for blender executable")

    parser.addoption(
        "--repo",
        action="store",
        default="user_default",
        help="Override for repository name (default: user_default)",
    )
    parser.addoption(
        "--background-only",
        action="store_true",
        default=False,
        help="Run only tests where background=True",
    )


@pytest.fixture
def blender(request):
    blender = request.config.getoption("--blender")

    if not blender:
        blender = shutil.which("blender")

    return blender


@pytest.fixture
def repo(request):
    return request.config.getoption("--repo")


@pytest.fixture
def background_only(request):
    return request.config.getoption("--background-only")


@pytest.fixture
def bl_tests_dir():
    curr_dir = pathlib.Path(os.path.dirname(__file__))
    return (curr_dir / pathlib.Path("../src/bl_tests/")).resolve().as_posix()
