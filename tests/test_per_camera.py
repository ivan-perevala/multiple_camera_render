# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import pathlib

import pytest

from . conftest import run_blender


@pytest.mark.parametrize("case", (
    "test_per_camera_simple",
    "test_per_camera_all",
    "test_per_camera_clear",
    "test_per_camera_dump",
))
@pytest.mark.parametrize("with_select_camera", ("", "'--with-select-camera', "))
def test_per_camera_bl(blender, blender_version, repo, bl_tests_dir, case, with_select_camera):
    cli: list = [
        blender,

        os.path.abspath(f"tests/data/per_camera_clear.blend"),
        "--background",

        "--addons",
        f"bl_ext.{repo}.multiple_camera_render",

        "--python-expr",
        (
            f"import pytest; "
            "import sys; "
            "(pytest.main(["
            "'-s', '-v', "
            f"'--repo', '{repo}', "
            f"'-k', \"{case}\", "
            f"{with_select_camera}"
            f"\"{bl_tests_dir}/\""
            "]))"
        ),

        "--python-exit-code",
        "255",
    ]

    run_blender(blender_version, bl_tests_dir, cli)


def test_per_camera_save_active_camera(tmpdir, blender, blender_version, repo, bl_tests_dir, test_scripts_dir):

    test_blend_filepath = tmpdir / "test_save.blend"

    cli: list = [
        blender,

        os.path.abspath(f"tests/data/per_camera_clear.blend"),
        "--background",

        "--addons",
        f"bl_ext.{repo}.multiple_camera_render",

        "--python",
        test_scripts_dir / "_test_per_camera_prepare_save_case.py",

        "--python-exit-code",
        "255",

        "--",

        "test_blend_filepath",
        test_blend_filepath,

    ]

    run_blender(blender_version, bl_tests_dir, cli)

    cli: list = [
        blender,

        test_blend_filepath,
        "--background",

        "--addons",
        f"bl_ext.{repo}.multiple_camera_render",

        "--python-expr",
        f"import pytest; import sys; sys.exit(pytest.main(['-s', '-v', '--repo', '{repo}', '-k', \"test_per_camera_active_camera_saved\", \"{bl_tests_dir}/\"]))",

        "--python-exit-code",
        "255",
    ]

    run_blender(blender_version, bl_tests_dir, cli)


@pytest.mark.parametrize("with_select_camera", ("", "'--with-select-camera', "))
def test_per_camera_render(tmpdir, blender, blender_version, repo, bl_tests_dir, test_scripts_dir, with_select_camera):

    cli = [
        blender,
        os.path.abspath(f"tests/data/per_camera_render_3_cameras.blend"),
        "--background",

        "--quiet",  # NOTE: Only available in Blender 4.3+

        "--render-output",
        os.path.join(tmpdir, "test_##"),

        "--addons",
        f"bl_ext.{repo}.multiple_camera_render",

        "--python-exit-code",
        "255",

        "--python",
        test_scripts_dir / "_test_per_camera_prepare_render.py",

        "--",

        f"{with_select_camera}",

    ]

    if blender_version <= (4, 2):
        cli.remove("--quiet")  # --quiet is not available in Blender 4.2 and earlier

    run_blender(blender_version, bl_tests_dir, cli)

    cli = [
        blender,
        "--factory-startup",
        "--background",

        "--python-expr",
        (
            f"import pytest;"
            "import sys;"
            "sys.exit(pytest.main(["
            "'-s', '-v', "
            f"'--repo', '{repo}', "
            "'-k', \"test_per_camera_render\", "
            f"{with_select_camera}"
            f"'--main-tmpdir', \"{pathlib.Path(tmpdir).as_posix()}\", "
            f"\"{bl_tests_dir}/\""
            "]))"
        ),

        "--python-exit-code",
        "255",
    ]

    run_blender(blender_version, bl_tests_dir, cli)
