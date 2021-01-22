# -*- coding: utf-8 -*-

VERSION = (0, 0, 1)
__version__ = '.'.join(map(str, VERSION))

__all__ = [
        'LatUni',
        'makeExtension',
        ]

import re
from xml.etree.ElementTree import Comment, ElementTree, QName, ProcessingInstruction

import markdown
import latuni

RE_WS = re.compile('\s+')

# Tags that should be formatted in a particular way
tags = {
        'bold': ('b', 'strong'),
        'ital': ('i', 'em', 'cite'),
        'mono': ('code', 'samp', 'kbd', 'var'),
        'und': ('ins', 'u'),
        'stk': ('del', 'strike', 's'),
        }

# Tags that should be ignored and whose content should be skipped
skip_tags = ('script', 'style')

header_tags = ('h1', 'h2', 'h3', 'h4', 'h5', 'h6')
code_holder_tags = ('p', 'pre')
para_tags = ('p', 'div')

class LatUni(markdown.extensions.Extension):

    def __init__(self, **kwargs):
        self.config = {
                "style": ["sans",
                            'Style to use for bold and italic text, '
                            'sans (default) or serif'],
                # Not currently used:
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
        md.output_formats["latuni"] = self.to_latuni

    def to_latuni(self, element):
        root = ElementTree(element).getroot()
        data = []
        write = data.append
        self._serialize(root, write)
        return "".join(data)

    def _serialize(self, elem, write):
        style = latuni.STYLE_SERIF if self.getConfig("style") == "serif" else latuni.STYLE_SANS
        bold = latuni.FACE_BOLD   # shorthand
        ital = latuni.FACE_ITAL   # shorthand
        mono = latuni.STYLE_MONO  # shorthand
        textwidth = self.getConfig("textwidth")

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
            write(latuni.fullwidth(elem[0].text))
            write(tail+"\n")
            return

        # From here on out, HTML/Markdown treats any whitespace as being
        # a single space. Do the same here.
        text = RE_WS.sub(" ", text)
        tail = RE_WS.sub(" ", tail)

        if tag.lower() in header_tags:
            # For now just write the text with a newline after
            write(text+"\n\n")
            write(tail)
            return
        elif tag.lower() in para_tags:
            write(text)
            for e in elem:
                self._serialize(e, write)
            write("\n\n")
            write(tail)
            return
        elif tag.lower() in tags['bold']:
            s = []
            if text: s.append(text)
            for e in elem:
                self._serialize(e, s.append)
            for i in s:
                write(latuni.format(style|bold, i))
            write(tail)
            return
        elif tag.lower() in tags['ital']:
            s = []
            if text: s.append(text)
            for e in elem:
                self._serialize(e, s.append)
            for i in s:
                write(latuni.format(style|ital, i))
            write(tail)
            return
        elif tag.lower() in tags['mono']:
            s = []
            if text: s.append(text)
            for e in elem:
                self._serialize(e, s.append)
            for i in s:
                write(latuni.format(latuni.STYLE_MONO, i))
            write(tail)
            return
        elif tag.lower() in tags['und']:
            s = []
            if text: s.append(text)
            for e in elem:
                self._serialize(e, s.append)
            for i in s:
                write(latuni.format(latuni.FMT_UNDERLINE, i))
            write(tail)
            return
        elif tag.lower() in tags['stk']:
            s = []
            if text: s.append(text)
            for e in elem:
                self._serialize(e, s.append)
            for i in s:
                write(latuni.format(latuni.FMT_STRIKEOUT, i))
            write(tail)
            return
        elif tag.lower() == 'hr':
            write(text)
            write(chr(0x2500) * ((textwidth or 50)-2))
            write("\n")
        elif tag.lower() == 'hr':
            write(text+"\n\n")
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
    return LatUni(*args, **kwargs)


# Self-test routine
if __name__ == '__main__':
    test_text = """
# This is a test of LatUni

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

----

I don't think markdown has <ins>underline</ins> tags,
so let's <s>test them manually</s>. They aren't converted...

----

Thank you.
"""

    print("Original:\n"+test_text)
    print("HTML formatted:")
    print(markdown.markdown(test_text))

    md = markdown.Markdown(
            extensions=[LatUni()],
            output_format="latuni")
    md.stripTopLevelTags = False
    out = md.convert(test_text)
    print("LatUni formatted:\n"+out)

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
