# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import argparse
import logging
from typing import ClassVar
import typing
import pathlib
import shutil

log = logging.getLogger(__name__)


class Options:
    __slots__ = (
        "valid",
        "blender_filepaths",
    )

    valid: bool
    """True if arguments are parsed correctly"""

    blender_filepaths: list[str]
    "Path to Blender executable to perform RNA dump, is recommended to use multiple versions, they would be merged"

    _verbosity_to_logger_map: ClassVar[dict[int, int]] = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.WARNING,
        3: logging.INFO,
        4: logging.DEBUG,
    }

    def __repr__(self):
        if not self.valid:
            return "Invalid options"

        ret = "Blender file paths:\n"
        ret += '\n'.join(self.blender_filepaths)
        return ret

    def __init__(self, args: list[str]):
        self.valid = False

        self.blender_filepaths = []

        parser = argparse.ArgumentParser(
            prog="Per Camera Data Path Generator",
            description=(
                "Generates data paths and unit test data source files for Multiple Camera Render addon"
            ),
            allow_abbrev=False,
        )

        verbosity_help = "; ".join(
            f"{_level} = {logging.getLevelName(_logging_level)}"
            for _level, _logging_level in self._verbosity_to_logger_map.items()
        )

        parser.add_argument(
            '-v', '--verbosity',
            type=int,
            choices=self._verbosity_to_logger_map.keys(),
            default=1,
            help=f"Verbosity level, which corresponds to: {verbosity_help}, defaults to 1"
        )

        parser.add_argument(
            '-B', '--blender',
            action='append',
            help=(
                "Paths to Blender executable to perform RNA dump, is recommended to use multiple versions, "
                "they would be merged"
            ),
            required=True,
            type=str
        )

        try:
            ns = parser.parse_args(args=args)
        except argparse.ArgumentTypeError as err:
            log.error(f"Unable to parse arguments: {err}")
            return

        verbosity = typing.cast(int, ns.verbosity)
        logging.basicConfig(level=self._verbosity_to_logger_map[verbosity])

        bl_paths = typing.cast(list[str], ns.blender)

        for item in bl_paths:
            bl_path = shutil.which("blender", path=pathlib.Path(item).absolute().resolve())

            if bl_path is None:
                log.error(f"Blender executable not found at \"{item}\", skipped")
                continue

            self.blender_filepaths.append(str(bl_path))

        self.valid = True
