#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import unicodedata

import markdown
import unilatin

##
## Main Program
##
def main():
    parser = argparse.ArgumentParser(description="Convert markdown to unilatin")
    parser.add_argument("--sans",
            action="store_const", const=unilatin.STYLE_SANS, dest="style",
            help="Use sans-serif variant for bold/italic (default)")
    parser.add_argument("--serif",
            action="store_const", const=unilatin.STYLE_SERIF, dest="style",
            help="Use serif variant for bold/italic")
    parser.add_argument("infile", metavar="INFILE",
            nargs="?",
            type=argparse.FileType(mode="rt", encoding="UTF-8"),
            default=sys.stdin,
            help="Read text from INFILE (default:stdin)")
    parser.add_argument("outfile", metavar="OUTFILE",
            nargs="?",
            type=argparse.FileType(mode="wt", encoding="UTF-8"),
            default=sys.stdout,
            help="Write formatted text to OUTFILE (default:stdout)")

    args = parser.parse_args()
    args.style = args.style or unilatin.STYLE_SANS

    text = args.infile.read()
    text = unicodedata.normalize('NFKD', text);
    flags = args.style|unilatin.FACE_BOLD
    args.outfile.write(unilatin.format(flags, text))

if __name__ == '__main__':
    sys.exit(main() or 0)

# Editor modelines - http://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# coding: utf-8
# End:
#
# vi:set shiftwidth=4 tabstop=4 expandtab fileencoding=utf-8:
# :indentSize=4:tabSize=4:noTabs=true:coding=utf-8:
