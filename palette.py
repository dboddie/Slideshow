#!/usr/bin/env python

colours = {"black": (0, 0, 0),  "red":  (1, 0, 0), "green":   (0, 1, 0),
           "yellow": (1, 1, 0), "blue": (0, 0, 1), "magenta": (1, 0, 1),
           "cyan": (0, 1, 1), "white": (1, 1, 1)}

# 4 colour mode
# fe08: b3 b2 b1 b0 g3 g2  x  x
# fe09:  x  x g1 g0 r3 r2 r1 r0

modes = {
    #        Red          Green          Blue          Logical
    #     FE08  FE09    FE08  FE09    FE08  FE09       colours
    2: [((0xff, 0xff), (0xff, 0xef), (0xef, 0xff)),  #    0
        ((0xff, 0xfb), (0xfb, 0xff), (0xbf, 0xff))], #    1

    4: [((0xff, 0xfe), (0xff, 0xef), (0xef, 0xff)),  #    0
        ((0xff, 0xfd), (0xff, 0xdf), (0xdf, 0xff)),  #    1
        ((0xff, 0xfb), (0xfb, 0xff), (0xbf, 0xff)),  #    2
        ((0xff, 0xf7), (0xf7, 0xff), (0x7f, 0xff))]  #    3
    }


def get_entries(number_of_colours, colours):

    fe08 = fe09 = 0xff
    
    for i in range(len(colours)):
        r, g, b = colours[i]
        masks = modes[number_of_colours][i]
        for component, mask in zip((r, g, b), masks):
            if component:
                fe08 = fe08 & mask[0]
                fe09 = fe09 & mask[1]
    
    return fe08, fe09

def palette(number):

    fe08 = fe09 = 0xff
    
    for i in range(4):
        colour = raw_input("Colour %i: " % i)
        r, g, b = colours[colour]
        masks = modes[number][i]
        for component, mask in zip((r, g, b), masks):
            if component:
                fe08 = fe08 & mask[0]
                fe09 = fe09 & mask[1]
    
    print "fe08: $%x" % fe08
    print "fe09: $%x" % fe09


if __name__ == "__main__":

    palette(4)
