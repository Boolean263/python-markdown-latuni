# python-markdown-latuni: Convert markdown to formatted "plain text"

The Unicode specification allows a lot of glyphs that would normally require special fonts to now be available in "plain text" files. Chess pieces, mathematical symbols, etc.

Unicode even contains variants for the basic Latin alphabet in 𝐛𝐨𝐥𝐝, 𝑖𝑡𝑎𝑙𝑖𝑐, 𝒃𝒐𝒍𝒅 𝒊𝒕𝒂𝒍𝒊𝒄, 𝚖𝚘𝚗𝚘𝚜𝚙𝚊𝚌𝚎, and 𝕞𝕠𝕣𝕖. My other python module, [LatUni](https://github.com/Boolean263/latuni), flagrantly abuses this fact to allow you to add text formatting to "plain text" files. This module, `python-markdown-latuni`, takes this abuse one step further and lets you generate unicode-formatted "plain text" from markdown, via the python [Markdown](https://pypi.org/project/Markdown/) module.

Disclaimer: This is a novelty, and probably breaks some accessibility rules or something. There is also probably some software which won't be able to handle text formatted in this way. (A lot of unicode-aware software still has trouble handling actually meaningful use cases like R-to-L text.)

## Installation

As much as anything else, this was to help me learn python package/module distribution. If I've done it right, you should be able to do the standard `python3 setup.py install` (or `python3 setup.py develop` if you want to hack around with me on this mess).

## Standalone Script

Once you install this module, you'll have a script in your path called `md2latuni`. It reads markdown text from the given input file (or standard input by default) and writes the unicode-formatted output to the given output file (or standard output). It automatically loads the `smarty` markdown extension to give the right unicode glyphs for single and double quotees. You can add other markdown extensions to the list as well; see `md2latuni --help`.

## Markdown Plugin

Usage is like any standard Markdown plugin:

    md = markdown.Markdown(
            extensions=[LatUni(style="sans")],
            output_format="latuni")
    md.stripTopLevelTags = False
    out = md.convert(text)

The style "sans" is default; "serif" is also available. This just tells latuni which variant of bold and italic text it should be using.

## Future Plans

* Text-wrapping
* Distinguishing headers
* Handling bullets
* Handling hyperlinks
* Handling blockquotes

## Have Fun

Because that's all this is for.
