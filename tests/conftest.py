# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

def pytest_addoption(parser):
    parser.addoption("--blender", action="store", default="", help="Override for blender executable")

    parser.addoption(
        "--background-only",
        action="store_true",
        default=False,
        help="Run only tests where background=True",
    )