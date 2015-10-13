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

import random

import Image

Black = "\x00\x00\x00"
Red = "\xff\x00\x00"
Green = "\x00\xff\x00"
Yellow = "\xff\xff\x00"
Blue = "\x00\x00\xff"
Magenta = "\xff\x00\xff"
Cyan = "\x00\xff\xff"
White = "\xff\xff\xff"

colours = [Black, Red, Green, Yellow, Blue, Magenta, Cyan, White]

y = 0
rh = 16
rw = rh * 2
scanlines = []
row = 0

row_colours = [(Red, Black), (Yellow, Black), (Green, Black), (Cyan, Black),
               (White, Black), (Magenta, Green), (Red, Green), (Black, Green),
               (Blue, Green), (Red, Green), (Black, Green), (Black, Red),
               (Black, White), (Blue, White), (Magenta, White), (Red, White)]

tiles = [(2,0, 0,1, 1,1, 1,0, 0,1, 0,0, 0,1, 0,0, 0,1, 0,0, 0,1, 1,0, 0,2, 2,0, 0,1, 0,0, 0,1, 1,0, 0,2, 2,0),
         (0,0, 1,2, 1,1, 2,2, 1,1, 0,2, 1,1, 0,2, 1,1, 2,1, 1,0, 0,2, 2,0, 0,2, 1,1, 2,1, 1,0, 0,2, 2,2, 2,2),
         (0,0, 0,0, 1,1, 0,0, 1,1, 1,1, 1,1, 2,2, 1,1, 0,1, 1,1, 1,0, 0,0, 2,2, 1,1, 0,1, 1,1, 1,2, 2,2, 2,2),
         (0,2, 2,2, 1,1, 0,0, 1,1, 2,2, 1,1, 2,2, 1,1, 0,0, 0,2, 1,1, 0,0, 2,2, 1,1, 0,0, 0,2, 1,1, 0,2, 2,2),
         (2,0, 0,2, 0,1, 0,2, 1,0, 2,0, 0,1, 2,0, 0,1, 0,1, 1,1, 1,0, 0,0, 0,2, 1,0, 0,1, 1,1, 1,0, 0,2, 2,2),
         (0,0, 0,2, 2,0, 0,0, 0,2, 2,0, 0,2, 2,0, 1,0, 0,2, 2,0, 0,2, 2,0, 0,2, 2,2, 2,2, 2,1, 1,0, 0,2, 2,2),
         (0,1, 1,0, 0,1, 1,0, 0,0, 0,1, 1,0, 0,0, 1,1, 1,0, 0,0, 1,1, 1,1, 1,0, 0,2, 2,1, 1,0, 0,1, 1,0, 0,2),
         (1,1, 2,1, 1,2, 1,1, 0,1, 1,0, 0,1, 1,0, 1,1, 0,1, 1,0, 1,1, 1,0, 0,0, 0,1, 1,0, 0,1, 2,1, 0,1, 1,0),
         (1,1, 0,2, 2,0, 1,1, 0,1, 1,0, 0,1, 1,0, 1,1, 0,1, 1,0, 1,1, 1,0, 0,0, 0,1, 1,0, 1,2, 1,0, 0,1, 1,0),
         (1,0, 0,2, 2,0, 0,1, 0,0, 0,1, 1,0, 0,0, 1,1, 1,0, 0,0, 1,1, 1,1, 1,0, 0,0, 0,1, 1,0, 0,1, 1,0, 0,2),
         (2,1, 1,2, 2,1, 1,2, 2,1, 1,2, 2,1, 1,0, 1,0, 0,2, 2,0, 0,2, 2,0, 0,2, 2,2, 2,0, 0,1, 1,0, 0,2, 2,2),
         (1,2, 2,2, 2,2, 2,1, 1,2, 2,1, 1,0, 0,0, 0,1, 1,2, 2,1, 1,2, 2,1, 1,2, 2,1, 1,1, 1,0, 0,2, 2,2, 2,2),
         (1,0, 1,1, 0,1, 0,2, 2,0, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1),
         (0,1, 1,1, 1,0, 0,0, 0,2, 2,0, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1),
         (0,1, 1,1, 1,0, 0,1, 1,0, 0,2, 2,0, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1),
         (1,0, 1,1, 0,1, 0,1, 1,0, 0,2, 2,0, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1, 0,1)]

orientations = [
    r"///////////\/////\/\ ",
    r"//////////////////\/",
    r"///////\/\/\///\/\/\ ",
    r"//////////////////\/",
    r"//\///\\\///\\/////\ ",
    r"\\//\/\/\\/\/\///\\\ ",
    r"/\/\//\\\\////\//\\\ ",
    r"/\/\//\\/\\/\////\\\ ",
    r"/\/\\\//\//\//\\\///",
    r"//\\\\////\\\\/\\///",
    r"//\\/\////\/\/\\\///",
    r"//\\/\////\/\/\\\///",
    r"\//\\\//////////////",
    r"\\/\\\//////////////",
    r"//\/\\\/////////////",
    r"/\\\////////////////"
    ]

while y < 256:

    colour0, colour1 = row_colours[row]
    rgb_values = [(colour0, colour0), (colour1, colour1), (colour0, colour1)]
    tile_colours = tiles[row]

    ry = 0
    
    while ry < rh:
    
        scanline = ""
        x = 0
        
        # Maintain an index into the tile colour list.
        c = 0
        
        while x < 640:
        
            # Find the colour of this tile.
            colour = rgb_values[tile_colours[c]]
            
            # Find the length of the span - this applies to two adjacent tiles.
            orientation = orientations[row][c/2]
            tw = ry * (rw/rh) + 1
            
            if orientation == "\\":
                if c % 2 == 1:
                    tw = rw - tw
            elif c % 2 == 0:
                tw = rw - tw
            
            # Add the pixel values for the colour, alternating between the two
            # supplied values and starting with the second value on alternate
            # scanlines.
            p = (ry + x) % 2
            i = 0
            while i < min(640 - x, tw):
                scanline += colour[p]
                i += 1
                p = 1 - p
            
            x += tw
            c += 1
        
        scanlines.append(scanline)
        ry += 1
    
    y += rh
    row += 1

image = Image.fromstring("RGB", (640, 256), "".join(scanlines))

image.save("Pictures/triangles.png")
