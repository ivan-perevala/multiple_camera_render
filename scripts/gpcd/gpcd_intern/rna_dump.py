# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from . options import Options


def bl_rna_dump_run(options: Options) -> bool:
    env = os.environ.copy()
    env['PYTHONPATH'] = str(Path(__file__).parent.parent.resolve())

    # print(str(Path(__file__).parent.parent.resolve()))

    for bl_path in options.blender_filepaths:
        args = [
            bl_path,
            '--background',
            '--factory-startup',
            '--python-use-system-env',
            '--python-expr',
            "import gpcd_runtime as gpcd; gpcd.dump()"
        ]

        proc = subprocess.Popen(
            args=args,
            env=env,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            # cwd=bl_path,
        )

        while proc.poll() is None:
            pass

        assert proc.stderr is not None
        assert proc.stderr.readable()

        errors = proc.stderr.read()

        assert not errors, errors

        assert proc.returncode == 0
