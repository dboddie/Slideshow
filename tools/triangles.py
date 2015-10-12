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

colour0 = colours[random.randrange(0, 7)]
colour1 = colour0

while y < 256:

    # Choose a new second colour for the row.
    while True:
        new_colour = colours[random.randrange(0, 7)]
        if new_colour != colour1 and new_colour != colour0:
            colour0 = colour1
            colour1 = new_colour
            break
    
    rgb_values = [(colour0, colour0), (colour1, colour1), (colour0, colour1)]
    ry = 0
    possible = [0, 1, 2]
    tile_colours = []
    i = 0
    while i < 2 * (640/rw):
        if not tile_colours:
            tile_colours.append(random.choice(rgb_values))
        else:
            while True:
                colour = random.choice(rgb_values)
                if colour != tile_colours[-1]:
                    tile_colours.append(colour)
                    break
        i += 1
    
    while ry < rh:
    
        scanline = ""
        x = 0
        # Change the span length for each scanline.
        if row % 4 == 0 or row % 4 == 3:
            tw = ry * (rw/rh) + 1
        else:
            tw = rw - (ry * (rw/rh)) - 1
        
        # Maintain an index into the tile colour list.
        c = 0
        
        while x < 640:
        
            # Find the colour of this tile.
            colour = tile_colours[c]
            
            # Add the pixel values for the colour, alternating between the two
            # supplied values and starting with the second value on alternate
            # scanlines.
            p = ry % 2
            i = 0
            while i < min(640 - x, tw):
                scanline += colour[p]
                i += 1
                p = 1 - p
            
            x += tw
            
            # Mirror the triangles every two triangles.
            if c % 2 == 0:
                tw = rw - tw
            
            c += 1
        
        scanlines.append(scanline)
        ry += 1
    
    y += rh
    row += 1

image = Image.fromstring("RGB", (640, 256), "".join(scanlines))

image.save("Pictures/triangles.png")
