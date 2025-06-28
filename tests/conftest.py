# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
import shutil
import os
import pathlib
import subprocess


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
def blender_version(blender):
    if not blender:
        pytest.skip("Blender executable not found")

    version_output = subprocess.check_output([blender, "--version"], text=True)
    first_line = version_output[:version_output.find('\n')]
    version_str = first_line.split(' ')[1].split('.')

    version = int(version_str[0]), int(version_str[1])

    return version


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


@pytest.fixture
def test_scripts_dir():
    curr_dir = pathlib.Path(os.path.dirname(__file__))
    return curr_dir / pathlib.Path("test_scripts")


def run_blender(bl_tests_dir: str, cli: list[str]):

    proc = subprocess.Popen(
        cli,
        env=os.environ,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        cwd=bl_tests_dir,
    )

    while proc.poll() is None:
        pass

    assert proc.stderr is not None
    assert proc.stderr.readable()

    errors = proc.stderr.read()

    assert not errors

    assert proc.returncode == 0
