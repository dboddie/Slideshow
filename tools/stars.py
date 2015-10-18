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

Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Yellow = (255, 255, 0)
Blue = (0, 0, 255)
Magenta = (255, 0, 255)
Cyan = (0, 255, 255)
White = (255, 255, 255)

colours = [Black, Red, Green, Yellow, Blue, Magenta, Cyan, White]

image = Image.new("RGB", (640, 256), 0)

y = 0

while y < 256:

    colour = colours[random.randrange(0, 7)]
    for i in range(4):
        x = random.randrange(0, 639)
        image.putpixel((x, y), colour)
    
    y += 1

image.save("Pictures/stars.png")
