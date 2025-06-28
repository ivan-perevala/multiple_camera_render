# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
import os

import pytest


@pytest.mark.parametrize("case", (
    "test_per_camera_simple",
    "test_per_camera_all",
    "test_per_camera_clear",
    "test_per_camera_dump",
))
def test_per_camera(blender, repo, bl_tests_dir, case):
    cli: list = [
        blender,

        os.path.abspath(f"tests/data/per_camera_clear.blend"),
        "--background",

        "--addons",
        f"bl_ext.{repo}.multiple_camera_render",

        "--python-expr",
        f"import pytest; import sys; sys.exit(pytest.main(['-s', '-v', '--repo', '{repo}', '-k', \"{case}\", \"{bl_tests_dir}/\"]))",

        "--python-exit-code",
        "255",
    ]

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
