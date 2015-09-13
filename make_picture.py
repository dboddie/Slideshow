#!/usr/bin/env python

import os, sys

import Image, ImageOps
from palette import get_entries

bitmap = {0: 0x00, 1: 0x01, 2: 0x10, 3: 0x11}
rgb_values = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0),
              (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)]
max_rows = 256
start_row = 0

def find_colour(r, g, b):

    r = r / 85
    g = g / 85
    b = b / 85
    
    if r == g == b:
        if r <= 1:
            colour = 0
        else:
            colour = 7

    elif r == g:
        if r > b:
            colour = 3
        else:
            colour = 4

    elif g == b:
        if g > r:
            colour = 6
        else:
            colour = 1

    elif b == r:
        if b > g:
            colour = 5
        else:
            colour = 2

    else:
        if b > r and b > g:
            colour = 4
        elif r > g and r > b:
            colour = 1
        elif g > b and g > r:
            colour = 2
        else:
            colour = 0
    
    return colour


if __name__ == "__main__":

    if len(sys.argv) >= 2 and sys.argv[1] == "-r":
        argv = sys.argv[:1] + sys.argv[2:]
        rotate = True
    else:
        argv = sys.argv[:]
        rotate = False
    
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s [-r] <image file> ...\n" % sys.argv[0])
        sys.exit(1)
    
    if not os.path.exists("data"):
        os.mkdir("data")
    
    for file_name in argv[1:]:
    
        im = Image.open(file_name)
        if rotate:
            im = im.rotate(270)
        if im.mode == "P":
            im = im.convert("RGB")
        
        if im.size[0] > 320:
            if im.size[0] > im.size[1]:
                height = int((320 * im.size[1])/im.size[0])
                im = im.resize((320, height), Image.CUBIC)
            elif im.size[1] > im.size[0]:
                width = int((256 * im.size[0])/im.size[1])
                im = im.resize((width, 256), Image.CUBIC)
        
        data = im.tostring()
        rows = []
        palette = []
        
        print "Converting image..."
        
        y = start_row
        while y < min(start_row + max_rows, im.size[1]):
        
            row = []
            colours = {}
            x = 0
            while x < im.size[0]:
            
                i = ((y * im.size[0]) + x) * 3
                r, g, b = map(ord, data[i:i+3])
                colour = find_colour(r, g, b)
                
                row.append(colour)
                colours[colour] = colours.get(colour, 0) + 1
                
                x += 1
            
            rows.append(row)
            palette.append(colours)
            y += 1
        
        while len(rows) % 8 != 0:
            rows.append([0] * im.size[0])
            palette.append({0: 320})
        
        # Simplify the palette on each row.
        print "Simplifying palette..."
        
        row = start_row
        old_entries = []
        while row < min(start_row + max_rows, len(rows)):
        
            # Sort the palette entries in ascending order of frequency.
            order = map(lambda (k, v): (v, k), palette[row - start_row].items())
            order.sort()
            
            # Only keep the four most frequent.
            entries = map(lambda (v, k): k, order[-4:])
            
            if old_entries:
            
                unused = []
                for entry in old_entries:
                    if entry not in entries:
                        unused.append(entry)
                
                for entry in entries:
                    if entry not in old_entries:
                        if unused:
                            old_entries[old_entries.index(unused.pop(0))] = entry
                        elif len(old_entries) < 4:
                            old_entries.append(entry)
                
                entries = filter(lambda x: x is not None, old_entries)
                
                # If there are spare slots, add an entry for black if it is not
                # already present.
                if 0 not in entries and len(entries) < 4:
                    entries.append(0)
            
            else:
                entries.sort()
            
            palette[row - start_row] = entries
            old_entries = entries[:]
            row += 1
        
        name = os.path.split(file_name)[1]
        output_file = os.path.join("data", "picture-data-" + os.path.splitext(name)[0] + ".oph")
        print "Writing", output_file
        
        f = open(output_file, "w")
        fe08_values = []
        fe09_values = []
        
        for entries in palette:
        
            fe08, fe09 = get_entries(4, map(lambda x: rgb_values[x], entries))
            fe08_values.append(fe08)
            fe09_values.append(fe09)
        
        while len(fe08_values) < max_rows:
            fe08_values.append(0xff)
            fe09_values.append(0xff)
        
        f.write("palette_fe08:\n")
        for fe08 in fe08_values:
            f.write(".byte $%02x\n" % fe08)
        
        f.write("\n")
        
        f.write("palette_fe09:\n")
        for fe09 in fe09_values:
            f.write(".byte $%02x\n" % fe09)
        
        f.write("\n")
        
        f.write("screen_data:\n")
        
        by = start_row
        while by < min(start_row + max_rows, len(rows)):
        
            if im.size[0] < 320:
                bx = 0
                padding = []
                while bx < 160 - im.size[0]/2:
                    values = []
                    y = by
                    while y < by + 8:
                        try:
                            # Find the logical colour for black.
                            i = palette[y - start_row].index(0)
                        except ValueError:
                            i = 0
                        value = bitmap[i] | (bitmap[i] << 1) | (bitmap[i] << 2) | (bitmap[i] << 3)
                        values.append("$%02x" % value)
                        y += 1
                    
                    padding.append(".byte " + ",".join(values) + "\n")
                    bx += 4
                
                f.write("".join(padding))
            
            bx = 0
            while bx < im.size[0]:
            
                f.write(".byte ")
                values = []
                y = by
                while y < by + 8:
                
                    value = 0
                    data = rows[y - start_row][bx:bx + 4]
                    shift = 0
                    
                    while data:
                        v = data.pop()
                        try:
                            # Find the logical colour for this physical colour.
                            i = palette[y - start_row].index(v)
                        except ValueError:
                            i = 0
                        value |= (bitmap[i] << shift)
                        shift += 1
                    
                    values.append("$%02x" % value)
                    y += 1
                
                f.write(",".join(values) + "\n")
                
                bx += 4
            
            if im.size[0] < 320:
                f.write("".join(padding))
            
            by += 8
        
        f.close()
    
    sys.exit()
