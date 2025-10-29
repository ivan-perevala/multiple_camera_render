# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys
from pathlib import Path

_INTERN_DIR = Path(__file__).parent / "gpcd_intern"

if _INTERN_DIR not in sys.path:
    sys.path.append(_INTERN_DIR)

import gpcd_intern as intern

if __name__ == '__main__':
    intern.main(sys.argv[1:])
