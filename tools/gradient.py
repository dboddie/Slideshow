#!/usr/bin/env python

"""
Copyright (C) 2015 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import Image

patterns = [
    "........",
    "........",
    "........",
    "........",
    "x.......",
    "....x...",
    "..x...x.",
    "x...x...",
    ".x.x...x",
    "..x.x.x.",
    ".x.x.x.x",
    "x.x.x.x.",
    ".x.x.x.x",
    "x.x.x.x.",
    ".xxx.x.x",
    "x.x.xxx.",
    ".xxx.xxx",
    "xx.xxx.x",
    "xxxx.xxx",
    ".xxxxxxx",
    ]

Black = "\x00\x00\x00"
Red = "\xff\x00\x00"
Green = "\x00\xff\x00"
Yellow = "\xff\xff\x00"
Blue = "\x00\x00\xff"
Magenta = "\xff\x00\xff"
Cyan = "\x00\xff\xff"
White = "\xff\xff\xff"

colours = [Black, Blue, Magenta, Red, Yellow, Green, Cyan, White,
           Cyan, Green, Yellow, Red, Magenta, Blue]

rows = []
y = 0

while y < 256:

    colour = (y / len(patterns)) % len(colours)
    pattern = patterns[y % len(patterns)]
    this_colour = colours[colour]
    next_colour = colours[(colour + 1) % len(colours)]
    pixels = pattern.replace(".", this_colour).replace("x", next_colour)
    
    rows.append(pixels * (640/len(pattern)))
    y += 1

data = "".join(map(lambda row: row[:len(row)/2], rows))
image = Image.fromstring("RGB", (320, 256), data)
image.save("Pictures/gradient1.png")

data = "".join(rows)
image = Image.fromstring("RGB", (640, 256), data)
image.save("Pictures/gradient0.png")
