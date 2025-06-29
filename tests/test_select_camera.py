# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

import pytest

from . conftest import run_blender


@pytest.mark.parametrize("case", ("test_select_camera_active", "test_select_camera_inactive"))
def test_select_cameras(blender, blender_version, repo, bl_tests_dir, case):
    cli = [
        blender,
        os.path.abspath(f"tests/data/per_camera_clear.blend"),
        "--background",

        "--python-expr",
        (
            f"import pytest;"
            "import sys;"
            "sys.exit(pytest.main(["
            "'-s', '-v', "
            f"'--repo', '{repo}', "
            f"'-k', \"{case}\", "
            f"\"{bl_tests_dir}/\""
            "]))"
        ),

        "--python-exit-code",
        "255",
    ]

    run_blender(blender_version, bl_tests_dir, cli)
