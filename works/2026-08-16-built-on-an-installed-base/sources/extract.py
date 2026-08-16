#!/usr/bin/env python3
"""
extract.py -- turn the two PDFs in this directory into the .txt beside them, using
nothing but the standard library, so that what this night read is reproducible from
the bytes in MANIFEST.json.

Why it is hand-rolled. This host's cryptography module is broken, and every PDF
library worth using imports it at load time; pdfminer.six and pypdf both died on
`ModuleNotFoundError: _cffi_backend` before reaching a page. So: inflate the content
streams and pull the text-showing operators out directly.

It has one known defect and the defect is left in on purpose. Inter-word spacing in
these files is carried by the kerning numbers inside TJ arrays, which this extractor
discards, so the output is unspaced: 'itwrestleswiththeinertia'. That is fine for
locating and reading a passage and useless for quoting one. Every quotation in
work.md was therefore re-read against the rendered PDF rather than cut from this
output. Written down because a text extractor that silently drops spaces is exactly
the class of instrument this line keeps catching itself trusting.
"""

import os
import re
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT_OP = re.compile(rb"\[(.*?)\]\s*TJ|\((?:\\.|[^\\()])*\)\s*Tj", re.S)
STR = re.compile(rb"\((?:\\.|[^\\()])*\)")


def extract(path):
    data = open(path, "rb").read()
    chunks = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        try:
            page = zlib.decompress(m.group(1))
        except zlib.error:
            continue                      # not a Flate stream (images, fonts)
        lines = []
        for op in TEXT_OP.finditer(page):
            if op.group(1) is not None:
                lines.append(b"".join(s[1:-1] for s in STR.findall(op.group(1))))
            else:
                lines.append(STR.search(op.group(0)).group(0)[1:-1])
        if lines:
            chunks.append(b"\n".join(lines))
    raw = b"\n".join(chunks)
    for a, b in ((rb"\\(", b"("), (rb"\\)", b")"), (rb"\\\\", b"\\")):
        raw = raw.replace(a, b)
    return raw.decode("latin-1")


if __name__ == "__main__":
    for fn in sorted(os.listdir(HERE)):
        if fn.endswith(".pdf"):
            src = os.path.join(HERE, fn)
            dst = src[:-4] + ".txt"
            t = extract(src)
            open(dst, "w", encoding="utf-8").write(t)
            print(f"{fn} -> {os.path.basename(dst)} ({len(t)} chars, unspaced)")
