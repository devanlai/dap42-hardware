#!/usr/bin/env python
import os
import sys
import argparse
import zipfile

import sh

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

IMAGE = "devanlai/diptrace-export:debug"
EXP_ENTRY = "/tmp/bin/export-asc.sh"
IMP_ENTRY = "/tmp/bin/import-asc.sh"

docker = sh.Command("docker")
dch_to_asc = docker.run.bake("-i", "--rm",
                             "--entrypoint", EXP_ENTRY,
                             IMAGE)
asc_to_dch = docker.run.bake("-i", "--rm",
                             "--entrypoint", IMP_ENTRY,
                             IMAGE)
render_schematic = docker.run.bake("-i", "--rm", IMAGE)

mogrify = sh.Command("mogrify")

pngify = mogrify.bake("-define", "png:exclude-chunks=date,time", "-strip", "-format", "png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("schematics",
                        nargs="+",
                        help="Paths to .sch files to render")
    parser.add_argument("-o", "--output",
                        help="Directory to place renders",
                        default="renders")
    parser.add_argument("--verbose",
                        action="store_true")
    args = parser.parse_args()

    for path in args.schematics:
        with open(path, "rb") as raw_schematic:
            if args.verbose:
                sys.stderr.write("Converting {} to ascii\n".format(path))
            schematic_name = os.path.basename(path)
            if schematic_name.endswith(".dch"):
                schematic_name = schematic_name[:-4]
            output_dir = os.path.join(args.output, schematic_name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            ascii_schematic = StringIO()
            for line in dch_to_asc(_in=raw_schematic):
                if line.strip().startswith("(PageScale"):
                    left = line[:line.index("(")]
                    right = line[line.index(")")+1:]
                    line = left + "(PageScale 1.0)" + right
                elif line.strip().startswith("(Scale"):
                    left = line[:line.index("(")]
                    right = line[line.index(")")+1:]
                    line = left + "(Scale 100.00%)" + right
                ascii_schematic.write(line)
            ascii_schematic.seek(0)

            if args.verbose:
                sys.stderr.write("Importing and rendering\n")
            render_job = render_schematic(asc_to_dch(_in=ascii_schematic))
            render_job.wait()
            del ascii_schematic

            if args.verbose:
                sys.stderr.write("Retrieving renders\n")
            with zipfile.ZipFile(StringIO(render_job.stdout), 'r') as zipped_renders:
                for member in zipped_renders.infolist():
                    fname = os.path.basename(member.filename)
                    if fname:
                        new_name = fname.replace(".bmp",".png")
                        if args.verbose:
                            sys.stderr.write("Converting {} to {}\n".format(fname, new_name))
                        dest = os.path.join(output_dir, new_name)
                        with open(dest, "wb+") as pngfile:
                            pngify('-', _in=zipped_renders.read(member), _out=dest)
                        if args.verbose:
                            sys.stderr.write("Output " + dest)
                        
