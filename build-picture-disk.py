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

import glob, os, stat, struct, sys
import makedfs

version = "1.0"

def system(command):

    if os.system(command):
        sys.exit(1)

boot_text = [
    # Enter the display mode and create a text window
    "MODE 1:VDU 28,0,31,31,30",
    "VDU 23,1,0;0;0;0;",
    # Disable printer and ADC
    "*FX 163,128,1",
    # Disable VDU output
    "CLS:*FX 3,2"
    ]

if __name__ == "__main__":

    if len(sys.argv) < 3:
    
        sys.stderr.write("Usage: %s <Ophis picture data files> ... <new SSD file>\n" % sys.argv[0])
        sys.exit(1)
    
    out_file = sys.argv[-1]
    
    # Build the ROM image file.
    system("ophis sync.oph -o palette.rom")
    rom = open("palette.rom", "rb").read()
    rom += "\x00" * (16384 - len(rom))
    open("palette.rom", "wb").write(rom)
    print "Written palette.rom"
    
    # Collect the pictures in the data directory.
    picture_files = sys.argv[1:-1]
    
    picture_data = []
    i = 1
    for name in picture_files:
        picture_data.append((name, "PICT%i" % i, 0x2e00))
        boot_text.append("?&FE08=&FF:?&FE09=&FF")
        boot_text.append("*LOAD PICT%i" % i)
        boot_text.append("*SLIDE")
        i += 1
    
    boot_text.append("*FX 3")
    boot_text.append("VDU 26:CLS")
    boot_text.append("PRINT ?&1900")
    boot_text.append("")
    
    # Assemble the files.
    assemble = [("sync-ram.oph", "SLIDE", 0xe00)] + picture_data
    files = [("!BOOT", 0x0000, 0x0000, "\r".join(boot_text))]
    
    for name, output, addr in assemble:
        if name.endswith(".oph"):
            if not os.path.exists(output) or (
                os.stat(name)[stat.ST_MTIME] > os.stat(output)[stat.ST_MTIME]):
                system("ophis " + name + " -o " + output)
            code = open(output).read()
        else:
            code = open(name).read().replace("\n", "\r")
            addr = 0x0000
        
        files.append((output, addr, addr, code))
    
    
    # Write the files to a disk image.
    disk = makedfs.Disk()
    disk.new()
    
    catalogue = disk.catalogue()
    catalogue.boot_option = 3
    
    disk_files = []
    for name, load, exec_, data in files:
        disk_files.append(makedfs.File("$." + name, data, load, exec_, len(data)))
    
    catalogue.write("Palette", disk_files)
    
    disk.file.seek(0, 0)
    disk_data = disk.file.read()
    open(out_file, "w").write(disk_data)
    
    print
    print "Written", out_file


    # Remove the object files.
    for name, output, addr in assemble:
        if name.endswith(".oph") and os.path.exists(output):
            os.remove(output)
    
    # Exit
    #sys.exit()
