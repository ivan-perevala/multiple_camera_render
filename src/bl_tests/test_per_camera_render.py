# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

import bpy
import os
import pytest


def test_check_output(main_tmpdir):

    for name, width, height, color in (
        ('test_02_Camera.png', 64, 64, (1.0, 0.0, 0.0)),
        ('test_02_Camera.001.png', 256, 256, (0.0, 1.0, 0.0)),
        ('test_02_Camera.002.png', 256, 256, (0.0, 0.0, 1.0)),
    ):
        fp = main_tmpdir / name

        assert os.path.isfile(fp), f"Missing image file \"{name}\""

        ret = bpy.ops.image.open(filepath=os.path.join(main_tmpdir, name))

        assert ret == {'FINISHED'}, f"Unable to open image file \"{name}\""

        image = bpy.data.images[name]
        image_width, image_height = image.size

        assert image_width == width, f"Image \"{name}\" width failed: {image_width} != {width}"
        assert image_height == height, f"Image \"{name}\" height failed: {image_height} != {height}"

        for i in range(3):
            channel = color[i]
            image_channel = image.pixels[i]

            assert channel == pytest.approx(image_channel, rel=1e-3), (
                f"Image \"{name}\" channel {i} failed: {channel} != {image_channel}"
            )
