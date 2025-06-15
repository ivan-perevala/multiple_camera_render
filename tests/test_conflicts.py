# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess
import os


def test_conflicts(blender, repo, bl_tests_dir):
    cli: list = [
        blender,
        "--background",

        "--addons",
        f"bl_ext.{repo}.multiple_camera_render,"
        f"bl_ext.{repo}.test_handler_conflict_one_level,"
        f"bl_ext.{repo}.test_handler_conflict_multilevel,"
        f"bl_ext.{repo}.test_handlers_conflict_from_lib",

        "--python-expr",
        f"import pytest; pytest.main(['-s', '-v', '--repo', '{repo}', \"{bl_tests_dir}/\"])",

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
