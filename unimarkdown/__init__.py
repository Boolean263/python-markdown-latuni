# -*- coding: utf-8 -*-

VERSION = (0, 0, 1)
__version__ = '.'.join(map(str, VERSION))

__all__ = [
        'UniMarkdown',
        'makeExtension',
        ]

import re
from xml.etree.ElementTree import Comment, ElementTree, QName, ProcessingInstruction

import markdown
import unilatin

RE_WS = re.compile('\s+')

# Tags that should be formatted in a particular way
tags = {
        'bold': ('b', 'strong'),
        'ital': ('i', 'em'),
        'mono': ('code'),
        }

# Tags that should be ignored and whose content should be skipped
skip_tags = ('script', 'style')

header_tags = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6')
code_holder_tags = ('p', 'pre')
para_tags = ('p', 'div')

class UniMarkdown(markdown.extensions.Extension):

    def __init__(self, **kwargs):
        self.config = {
                "style": ["sans",
                            'Style to use for bold and italic text, '
                            'sans (default) or serif'],
                "textwidth": [72,
                            'Text wrap width (default:72)'],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """\
        Register this extension with Markdown.
        """
        md.registerExtension(self)
        self.md = md
        md.output_formats["unilatin"] = self.to_unilatin

    def to_unilatin(self, element):
        root = ElementTree(element).getroot()
        data = []
        write = data.append
        self._serialize(root, write)
        return "".join(data)

    def _serialize(self, elem, write):
        style = unilatin.STYLE_SERIF if self.config["style"] == "serif" else unilatin.STYLE_SANS
        bold = unilatin.FACE_BOLD   # shorthand
        ital = unilatin.FACE_ITAL   # shorthand
        mono = unilatin.STYLE_MONO  # shorthand

        tag = elem.tag
        text = elem.text or ""
        tail = elem.tail or ""
        if tag in (Comment, ProcessingInstruction) or tag.lower() in skip_tags:
            # Don't render these to text at all
            write(tail)
            return
        if tag.lower() in code_holder_tags and len(elem) == 1 and not text and elem[0].tag.lower() == 'code':
            # Code blocks of the two different types.
            # Whitespace matters here.
            write(unilatin.fullwidth(elem[0].text))
            write(tail+"\n")
            return

        # From here on out, HTML/Markdown treats any whitespace as being
        # a single space. Do the same here.
        text = RE_WS.sub(" ", text).lstrip()
        tail = RE_WS.sub(" ", tail).lstrip()

        if tag.lower() in header_tags:
            # For now just write the text with a newline after
            write(text+"\n")
            write(tail)
            return
        elif tag.lower() in para_tags:
            write(text)
            for e in elem:
                self._serialize(e, write)
            write("\n")
            write(tail)
            return
        elif tag.lower() in tags['bold']:
            s = []
            if text: s.append(text)
            for e in elem:
                self._serialize(e, s.append)
            for i in s:
                write(unilatin.format(style|bold, i))
            write(tail)
            return
        elif tag.lower() in tags['ital']:
            s = []
            if text: s.append(text)
            for e in elem:
                self._serialize(e, s.append)
            for i in s:
                write(unilatin.format(style|ital, i))
            write(tail)
            return
        elif tag.lower() in tags['mono']:
            s = []
            if text: s.append(text)
            for e in elem:
                self._serialize(e, s.append)
            for i in s:
                write(unilatin.format(unilatin.STYLE_MONO, i))
            write(tail)
            return
        else:
            # Tags we haven't handled above, including non-tags and QNames
            pass

        # If we get this far, the tag handler didn't explicitly handle
        # its output or its children.
        write(text)
        for e in elem:
            self._serialize(e, write)
        write(tail)

def makeExtension(*args, **kwargs):
    return UniMarkdown(*args, **kwargs)


# Self-test routine
if __name__ == '__main__':
    test_text = """
# This is a test of unimarkdown

This text *is italicized* to some degree.

This one **has bold in it**.

Heck, _why not **both?**_

        Here is a single line of "code".
        More code
        And more

Back to normal. `code command` normal

```
Code block
code block
code Block
```

Markdown considers
lines without blank lines
to be a single paragraph

Thank you.
"""

    print("Original:\n"+test_text)
    print("HTML formatted:")
    print(markdown.markdown(test_text))

    md = markdown.Markdown(
            extensions=[UniMarkdown()],
            output_format="unilatin")
    md.stripTopLevelTags = False
    out = md.convert(test_text)
    print("Unilatin formatted:\n"+out)

#
# Editor modelines - http://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# End:
#
# vi:set shiftwidth=4 tabstop=4 expandtab:
# indentSize=4:tabSize=4:noTabs=true:
