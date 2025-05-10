# SPDX-FileCopyrightText: 2020-2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import shutil
import subprocess


if __name__ == '__main__':

    blender = shutil.which("blender")
    if not blender:
        raise RuntimeError("No Blender installation found, check PATH")

    cur_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(cur_dir)

    subprocess.Popen(
        [
            blender,
            os.path.join(cur_dir, "default.blend"),
            "--background",
            "--python",
            os.path.join(cur_dir, "blender_icons_geom.py"),
            "--",
            "--output-dir",
            os.path.join(root_dir, "src", "multiple_camera_render", "icons"),
        ],
        universal_newlines=True,
    )
