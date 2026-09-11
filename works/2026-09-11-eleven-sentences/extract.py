#!/usr/bin/env python3
"""extract -- Session 87, 2026-09-11.

Turns a Bikeshed-generated WHATWG single-page standard into register-tagged prose blocks.

There is no lxml, no BeautifulSoup and no html5lib in this environment, so this is a hand-written
walker over the standard library's HTMLParser.  Session 86 filed F-128 against a hand-written parse
that returned an author's name as a document title; `verify.py` is the answer to that, and it is run
before any number in this night is reported -- it re-derives the same counts by a second, independent
route (a flat regex over the markup) and fails loudly where the two disagree beyond a declared
tolerance.

Three decisions, all fixed in PREDICTIONS.md §2 before the corpus was measured:

  BLOCK        a text block ends at any block-level element; inline <code>, <a>, <i>, <dfn> stay in
               the sentence, because they are part of it.
  DROP         <script> <style> <pre> <svg> <xmp> <table> -- code listings, IDL blocks and the
               support-matrix grids are not prose and are dropped whole.
  FURNITURE    the document head, navigation, the tables of contents and the index: dropped, and
               counted, exactly as Session 86 dropped RFC page furniture.

And the register, which is the variable this night turns on.  WHATWG marks its non-normative prose
in two ways and uses neither the RFC 8174 capitals nor an EU-style structural division:

  NONNORM      (a) inside an element whose class is note, example, advisement or issue -- Bikeshed's
                   own markers; or
               (b) inside a section opened by the sentence "This section is non-normative."
  NORM         everything else.
"""

import re
from html.parser import HTMLParser

BLOCK = {"p", "li", "dd", "dt", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th",
         "figcaption", "blockquote", "caption", "div", "section", "details", "summary"}
DROP = {"script", "style", "pre", "svg", "xmp", "table"}
VOID = {"br", "img", "link", "meta", "hr", "input", "source", "col", "area", "wbr"}
NONNORM_CLASSES = ("note", "example", "advisement", "issue", "status")
FURNITURE_CLASSES = ("toc", "head", "copyright", "status")
FURNITURE_IDS = ("toc", "index", "idl-index", "references", "acknowledgments", "acknowledgements")
MARKER = "this section is non-normative."
HEADING = {"h1": 1, "h2": 2, "h3": 3, "h4": 4, "h5": 5, "h6": 6}


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, class-list, id)
        self.buf = []
        self.out = []
        self.drop_depth = 0

    def _class_register(self):
        for tag, cls, eid in self.stack:
            if any(c in NONNORM_CLASSES for c in cls):
                return True
        return False

    def _furniture(self):
        for tag, cls, eid in self.stack:
            if tag in ("nav", "header", "footer"):
                return True
            if any(c in FURNITURE_CLASSES for c in cls):
                return True
            if eid in FURNITURE_IDS:
                return True
        return False

    def _tag(self):
        for tag, cls, eid in reversed(self.stack):
            if tag in BLOCK:
                return tag
        return None

    def flush(self):
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        self.buf = []
        if text:
            self.out.append({"tag": self._tag(), "class_nonnorm": self._class_register(),
                             "furniture": self._furniture(), "text": text})

    def handle_starttag(self, tag, attrs):
        if self.drop_depth:
            if tag in DROP:
                self.drop_depth += 1
            return
        if tag in DROP:
            self.flush()
            self.drop_depth = 1
            return
        if tag in VOID:
            return
        a = dict(attrs)
        if tag in BLOCK:
            self.flush()
        self.stack.append((tag, (a.get("class") or "").split(), a.get("id") or ""))

    def handle_startendtag(self, tag, attrs):
        if tag in VOID or self.drop_depth:
            return
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if self.drop_depth:
            if tag in DROP:
                self.drop_depth -= 1
            return
        if tag in VOID:
            return
        if tag in BLOCK:
            self.flush()
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if not self.drop_depth:
            self.buf.append(data)

    def close(self):
        super().close()
        self.flush()


def extract(source):
    """Blocks in document order, each with its register resolved."""
    p = Blocks()
    p.feed(source)
    p.close()

    out = []
    nonnorm_from_level = None      # the heading level whose section is marked non-normative
    current_level = 0
    for b in p.out:
        level = HEADING.get(b["tag"] or "", None)
        if level is not None:
            current_level = level
            if nonnorm_from_level is not None and level <= nonnorm_from_level:
                nonnorm_from_level = None
        if b["text"].strip().lower() == MARKER:
            nonnorm_from_level = current_level
        by_section = nonnorm_from_level is not None
        out.append({"register": "NONNORM" if (b["class_nonnorm"] or by_section) else "NORM",
                    "marked_by": ("class" if b["class_nonnorm"] else
                                  ("section" if by_section else None)),
                    "tag": b["tag"], "furniture": b["furniture"], "text": b["text"]})
    return out
