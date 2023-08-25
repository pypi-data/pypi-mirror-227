#!/usr/bin/env micropython
# interstate75-wrapper
# Copyright (C) 2023 Andrew Wilkinson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    from typing import Tuple
except ImportError:
    pass


class Pen:
    def __init__(self, r: int, g: int, b: int) -> None:
        self.r = r
        self.g = g
        self.b = b

    def as_tuple(self) -> Tuple[int, int, int]:
        return (self.r, self.g, self.b)


class RGB332Pen(Pen):
    def __init__(self, r: int, g: int, b: int) -> None:
        super().__init__(round((1 << 3) * (float(r) / (1 << 3))),
                         round((1 << 3) * (float(g) / (1 << 3))),
                         round((1 << 2) * (float(b) / (1 << 2))))


class RGB888Pen(Pen):
    def __init__(self, r: int, g: int, b: int) -> None:
        super().__init__(r, g, b)
