# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging

from . options import Options
from . rna_dump import bl_rna_dump_run

log = logging.getLogger(__name__)


def main(args: list[str]):
    options = Options(args=args)

    log.debug("Run with options:")
    log.debug(options)

    result = bl_rna_dump_run(options)
