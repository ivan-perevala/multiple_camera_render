# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import subprocess

import pytest


CAMERA_NAMES = (
    "Camera",
    "Camera.001",
    "Camera.002",
    "Camera.003",
    "Camera.004",
    "Camera.005",
    "Camera.006",
)


@pytest.mark.parametrize("filepath", (
    "cycles_7_cameras_clockwise.blend",
    "cycles_7_cameras_counterclockwise.blend",
))
@pytest.mark.parametrize("background", (False, True,))
@pytest.mark.parametrize("animation", (False, True))
@pytest.mark.parametrize("preview", (False, True))
@pytest.mark.parametrize("render_output", (("test_####", "test_{_frame:04}_{_camera}.png"),))
def test_render(tmpdir, blender, blender_version, filepath, background, animation, preview, render_output, background_only):
    if background_only and not background:
        pytest.skip("Skipping test because --background-only option is set")

    cli: list = [blender,]

    if background:
        cli.append("--background")

    cli.extend([
        os.path.abspath(f"tests/data/{filepath}"),
        "--quiet",  # NOTE: Only available in Blender 4.3+
        "--render-output",
        os.path.join(tmpdir, render_output[0]),
        "--python-expr",
        f"import bpy; bpy.ops.render.multiple_camera_render('INVOKE_DEFAULT', animation={animation}, preview={preview}, quit=True)",
        "--python-exit-code",
        "255",
    ])

    if blender_version <= (4, 2):
        cli.remove("--quiet")  # --quiet is not available in Blender 4.2 and earlier

    proc = subprocess.Popen(cli, env=os.environ)

    while proc.poll() is None:
        pass

    assert proc.returncode == 0

    _expected_files = set()
    rendered_files = set(os.listdir(tmpdir))

    if preview:
        assert not rendered_files
    else:
        if animation:
            for _frame in range(1, 11):
                for _camera in CAMERA_NAMES:
                    _expected_files.add(render_output[1].format(_frame=_frame, _camera=_camera))
        else:
            _expected_files = set((render_output[1].format(_frame=1, _camera=_) for _ in CAMERA_NAMES))

        assert rendered_files == _expected_files
