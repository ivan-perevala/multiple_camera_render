# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import py_launch_blender as lb

import os
import sys


def test_build():
    with lb.EnvironmentVariables() as ev:
        ev.BLENDER_USER_CONFIG = os.path.abspath('tests/config/')
        ev.BLENDER_USER_EXTENSIONS = os.path.abspath('tests/extensions/')
        ev.BLENDER_USER_SCRIPTS = os.path.abspath('tests/scripts/')

        lb.launch_blender(
            background=True,
            command="extension"
        )

# def test_launch():
#     with lb.EnvironmentVariables() as ev:
#         ev.BLENDER_CUSTOM_SPLASH_BANNER = 'tests/banner.png'
#         ev.BLENDER_USER_CONFIG = os.path.abspath('tests/config/')
#         ev.BLENDER_USER_EXTENSIONS = os.path.abspath('tests/extensions/')
#         ev.BLENDER_USER_SCRIPTS = os.path.abspath('tests/scripts/')

#         if venv_path := os.environ.get('VIRTUAL_ENV', None):
#             ev.BLENDER_SYSTEM_PYTHON = venv_path

#         os.environ['PYTHONPATH'] = os.pathsep.join(sys.path)

#         proc = lb.launch_blender(
#             factory_startup=True,
#             python_exit_code=255,
#             python_use_system_env=True,
#             # python_expr=f"import pytest; pytest.main(['-v', '-s', 'src/bl_tests/test_render'])"
#         )

#         while proc.poll() is None:
#             pass

#         assert not proc.returncode
