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

Black = "\x00\x00\x00"
Red = "\xff\x00\x00"
Green = "\x00\xff\x00"
Yellow = "\xff\xff\x00"
Blue = "\x00\x00\xff"
Magenta = "\xff\x00\xff"
Cyan = "\x00\xff\xff"
White = "\xff\xff\xff"

colours = [Black, Red, Green, Yellow, Blue, Magenta, Cyan, White]

class Solid:

    def __init__(self, background, foreground):
    
        self.background = background
        self.foreground = foreground
    
    def colour(self, colour_entry, row, x, height):
    
        if colour_entry == 0:
            return self.background
        elif colour_entry == 1:
            return self.foreground
        else:
            p = (row + x) % 2
            if p == 0:
                return self.background
            else:
                return self.foreground

class Gradient:

    def __init__(self, background0, foreground0,
                       background1 = None, foreground1 = None):
    
        self.background0 = background0
        self.foreground0 = foreground0
        
        if not background1:
            background1 = background0
        if not foreground1:
            foreground1 = foreground0
        
        self.background1 = background1
        self.foreground1 = foreground1
    
    def colour(self, colour_entry, row, x, height):
    
        if colour_entry == 0:
            colours0 = (self.background0, self.background0)
            colours1 = (self.background1, self.background1)
        elif colour_entry == 1:
            colours0 = (self.foreground0, self.foreground0)
            colours1 = (self.foreground1, self.foreground1)
        else:
            colours0 = (self.background0, self.foreground0)
            colours1 = (self.background1, self.foreground1)
        
        colours = (colours0, colours1)
        
        if row < height/4:
            c = 0
        elif row < (3*height)/4:
            c = row % 2
        else:
            c = 1
        
        p = (row + x) % 2
        return colours[c][p]

y = 0
rh = 16
rw = rh * 2
scanlines = []
row = 0

row_palettes = [
    Gradient(Red, Black, Yellow),
    Solid(Yellow, Black),
    Gradient(Yellow, Black, Green),
    Solid(Cyan, Black),
    Solid(White, Black),
    Solid(Magenta, Green),
    Gradient(Red, Green, Black, Cyan),
    Gradient(Black, Cyan, Black, Green),
    Gradient(Black, Green, Blue),
    Gradient(Blue, Green, Red),
    Solid(Black, Green),
    Gradient(Black, Red, Black, Blue),
    Gradient(Blue, Cyan, Magenta, White),
    Gradient(Magenta, White, Black),
    Gradient(Black, White, Red),
    Gradient(Red, White, Black, Cyan)
    ]

tiles = [(2,0, 0,1, 1,1, 1,0, 0,1, 0,0, 0,1, 0,0, 0,1, 0,0, 0,1, 1,0, 0,2, 2,0, 0,1, 0,0, 0,1, 1,0, 0,2, 2,0),
         (0,0, 1,2, 1,1, 2,2, 1,1, 0,2, 1,1, 0,2, 1,1, 2,1, 1,0, 0,2, 2,0, 0,2, 1,1, 2,1, 1,0, 0,2, 2,2, 2,2),
         (0,0, 0,0, 1,1, 0,0, 1,1, 1,1, 1,1, 2,2, 1,1, 0,1, 1,1, 1,0, 0,0, 2,2, 1,1, 0,1, 1,1, 1,2, 2,2, 2,2),
         (0,2, 2,2, 1,1, 0,0, 1,1, 2,2, 1,1, 2,2, 1,1, 0,0, 0,2, 1,1, 0,0, 2,2, 1,1, 0,0, 0,2, 1,1, 0,2, 2,2),
         (2,0, 0,2, 0,1, 0,2, 1,0, 2,0, 0,1, 2,0, 0,1, 0,1, 1,1, 1,0, 0,0, 0,2, 1,0, 0,1, 1,1, 1,0, 0,2, 2,2),
         (0,0, 0,2, 2,0, 0,0, 0,2, 2,0, 0,2, 2,0, 1,0, 0,2, 2,0, 0,2, 2,0, 0,2, 2,0, 0,0, 0,1, 1,0, 0,2, 2,2),
         (0,1, 1,0, 0,1, 1,0, 0,0, 0,1, 1,0, 0,0, 1,1, 1,0, 0,0, 1,1, 1,1, 1,0, 0,2, 2,1, 1,0, 0,1, 1,0, 0,2),
         (1,1, 2,1, 1,2, 1,1, 0,1, 1,0, 0,1, 1,0, 1,1, 0,1, 1,0, 1,1, 1,0, 0,0, 0,1, 1,0, 0,1, 2,1, 0,1, 1,0),
         (1,1, 0,2, 2,0, 1,1, 0,1, 1,0, 0,1, 1,0, 1,1, 0,1, 1,0, 1,1, 1,0, 0,0, 0,1, 1,0, 1,2, 1,0, 0,1, 1,0),
         (1,0, 0,2, 2,0, 0,1, 0,0, 0,1, 1,0, 0,0, 1,1, 1,0, 0,0, 1,1, 1,1, 1,0, 0,0, 0,1, 1,0, 0,1, 1,0, 0,2),
         (2,1, 1,2, 2,1, 1,2, 2,1, 1,2, 2,1, 1,2, 1,0, 0,2, 2,0, 0,2, 2,0, 0,2, 2,2, 2,0, 0,1, 1,0, 0,2, 2,2),
         (1,2, 2,2, 2,2, 2,1, 1,2, 2,1, 1,1, 1,2, 0,1, 1,2, 2,1, 1,2, 2,1, 1,2, 2,1, 1,1, 1,0, 0,1, 1,1, 1,2),
         (2,0, 1,0, 1,1, 0,1, 0,2, 2,0, 0,2, 2,0, 0,1, 1,1, 1,0, 0,1, 1,1, 1,0, 0,1, 1,1, 0,0, 1,1, 1,1, 1,0),
         (2,0, 0,1, 1,1, 1,0, 0,0, 0,2, 2,0, 0,2, 0,0, 0,1, 1,0, 1,1, 0,1, 1,1, 0,0, 1,1, 0,0, 0,1, 1,0, 0,0),
         (2,0, 0,1, 1,1, 1,0, 0,1, 1,0, 0,2, 2,0, 0,1, 1,0, 0,0, 1,1, 1,0, 1,1, 0,0, 1,1, 0,0, 0,0, 0,1, 1,0),
         (2,0, 1,0, 1,1, 0,1, 0,1, 1,0, 0,2, 2,0, 0,1, 1,1, 1,0, 0,1, 1,1, 1,0, 0,1, 1,1, 1,0, 1,1, 1,1, 1,0)]

orientations = [
    r"/(/]]/]/]//\//]//\/\ ",
    r"/(////////////////\/",
    r"///////\/\/\///\/)/\ ",
    r"//////////////////\/",
    r"//\///\\\)/]\\/)///\ ",
    r"\\//\/\/\\/\/\///\\\ ",
    r"/\/\//\\\\////\//\\\ ",
    r"/\/\//\\/\\/\////\\\ ",
    r"/\/\\\//\//\//\\\///",
    r"//\\\\////\\\\/\\///",
    r"//\\/\////\/\/\\\///",
    r"//\\/\\\//\/\/\\\///",
    r"/\//\\\\(\)(/)]\////",
    r"\\\/\\\\////)\/\/\\\ ",
    r"///\()\\////[//\//\\ ",
    r"\/\\[]//[\\[/]]\[//]"
    ]

while y < 256:

    palette = row_palettes[row]
    tile_colours = tiles[row]

    ry = 0
    
    while ry < rh:
    
        scanline = ""
        x = 0
        
        # Maintain an index into the tile colour list.
        c = 0
        
        while x < 640:
        
            # Find the colour entry of this tile (0=background, 1=foreground,
            # 2=dither).
            colour_entry = tile_colours[c]
            
            # Find the length of the span - this applies to two adjacent tiles.
            orientation = orientations[row][c/2]
            
            if orientation in r"\/":
            
                tw = ry * (rw/rh) + 1
                
                if orientation == "\\":
                    if c % 2 == 1:
                        tw = rw - tw
                elif c % 2 == 0:
                    tw = rw - tw
            
            elif orientation == "|":
            
                tw = rw/2
            
            elif orientation == "-":
            
                if ry < rh/2:
                    if c % 2 == 0:
                        tw = rw
                    else:
                        tw = 0
                else:
                    if c % 2 == 0:
                        tw = 0
                    else:
                        tw = rw
            
            elif orientation in "()":
            
                tw = rw - int(((rw**2) - (rw**2 * ((rh - (ry+1))**2)/(rh**2)))**0.5)
                
                if orientation == "(":
                    if c % 2 == 1:
                        tw = rw - tw
                else:
                    if c % 2 == 0:
                        tw = rw - tw
            
            elif orientation in "[]":
            
                tw = rw - int(((rw**2) - (rw**2 * (ry**2)/(rh**2)))**0.5)
                
                if orientation == "[":
                    if c % 2 == 1:
                        tw = rw - tw
                else:
                    if c % 2 == 0:
                        tw = rw - tw
            
            # Add the pixel values for the colour, alternating between the two
            # supplied values and starting with the second value on alternate
            # scanlines.
            i = 0
            while i < min(640 - x, tw):
                scanline += palette.colour(colour_entry, ry, x + i, rh)
                i += 1
            
            x += tw
            c += 1
        
        scanlines.append(scanline)
        ry += 1
    
    y += rh
    row += 1

image = Image.fromstring("RGB", (640, 256), "".join(scanlines))

image.save("Pictures/triangles.png")
