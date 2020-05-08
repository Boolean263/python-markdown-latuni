#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse

import markdown
from mdx_latuni import LatUni

##
## Main Program
##
def main():
    parser = argparse.ArgumentParser(description="Convert markdown to latuni")
    parser.add_argument("--sans",
            action="store_const", const="sans", dest="style",
            help="Use sans-serif variant for bold/italic (default)")
    parser.add_argument("--serif",
            action="store_const", const="serif", dest="style",
            help="Use serif variant for bold/italic")
    parser.add_argument("-x", "--extension", metavar="EXTENSION",
            type=str, action="append", dest="extensions",
            help="Load Markdown extension EXTENSION")
    parser.add_argument("-c", "--extension_configs", metavar="CONFIG_FILE",
            type=str, dest="configfile",
            help="Read extension configurations from CONFIG_FILE")
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
    args.style = args.style or "sans"

    text = args.infile.read()
    extensions = args.extensions or []
    extensions.extend([LatUni(style=args.style), 'smarty'])

    extension_configs = {}
    if args.configfile:
        with codecs.open(
            args.configfile, mode="r"
        ) as fp:
            try:
                extension_configs = yaml_load(fp)
            except Exception as e:
                message = "Failed parsing extension config file: %s" % \
                          args.configfile
                e.args = (message,) + e.args[1:]
                raise

    if 'latuni' not in extension_configs:
        extension_configs['latuni'] = {
                'style': args.style,
                }
    if 'smarty' not in extension_configs:
        extension_configs['smarty'] = {
                'substitutions': {
                    'left-single-quote': '‘',
                    'right-single-quote': '’',
                    'left-double-quote': '“',
                    'right-double-quote': '”',
                    'left-angle-quote': '«',
                    'right-angle-quote': '»',
                    'ndash': '–',
                    'mdash': '—',
                    }
                }

    md = markdown.Markdown(
            extensions=extensions,
            extension_configs=extension_configs,
            output_format="latuni")
    md.stripTopLevelTags = False
    out = md.convert(text)

    # the markdown module trims trailing whitespace
    args.outfile.write(out+"\n")

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
