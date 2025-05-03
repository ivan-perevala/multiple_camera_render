# SPDX-FileCopyrightText: 2025 Ivan Perevala <ivan95perevala@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

# type: ignore

import numpy as np

from bpy.types import Object


class ClockwiseIterator:
    "Clockwise iterator, loops from and to specified index of array."

    array: np.ndarray[Object]
    start_index: int
    _i: int
    _is_first_elem: bool

    def __init__(self, array, start_index):
        self.array = array
        self.start_index = start_index
        self._i = start_index
        self._is_first_elem = False

    def __iter__(self):
        self._i = self.start_index
        return self

    def __next__(self):
        if self._i == self.start_index:
            if self._is_first_elem:
                raise StopIteration
            else:
                self._is_first_elem = True

        item = self.array[self._i]
        self._i += 1

        if self._i == self.array.size:
            self._i = 0

        return item

    def __len__(self):
        return self.array.size

    def __reversed__(self):
        return CounterClockwiseIterator(self.array, self.start_index)


class CounterClockwiseIterator(ClockwiseIterator):
    "Reversed clockwise iterator."

    def __next__(self):
        if self._i == self.start_index:
            if self._is_first_elem:
                raise StopIteration
            else:
                self._is_first_elem = True

        item = self.array[self._i]

        if self._i == 0:
            self._i = self.array.size

        self._i -= 1

        return item
