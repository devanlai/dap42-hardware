#!/usr/bin/env python
"""
Takes in a DipTrace ascii schematic and filters out any per-sheet
scaling factors that affect how the schematic is displayed
"""

import re
import sys

for line in sys.stdin:
    if line.strip().startswith("(PageScale"):
        left = line[:line.index("(")]
        right = line[line.index(")")+1:]
        line = left + "(PageScale 1.0)" + right
    elif line.strip().startswith("(Scale"):
        left = line[:line.index("(")]
        right = line[line.index(")")+1:]
        line = left + "(Scale 100.00%)" + right
    sys.stdout.write(line)
