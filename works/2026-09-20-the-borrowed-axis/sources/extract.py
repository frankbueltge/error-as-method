#!/usr/bin/env python3
"""
extract.py -- turn a PDF in this directory into the .txt beside it, using nothing but
the standard library, so that what this night read is reproducible from the bytes named
in MANIFEST.json rather than from a service.

Why hand-rolled. This host's `cryptography` module panics on import (checked tonight:
`pyo3_runtime.PanicException` from `cryptography.hazmat.bindings._rust`), and pypdf and
pdfminer.six both pull it in before they reach a page. Session 58 wrote the first version
of this file for the same reason (works/2026-08-16-built-on-an-installed-base/sources/
extract.py) and declared two defects in its own docstring: it dropped the kerning numbers
that carry inter-word spacing, so its output could not be quoted from, and it decoded
bytes as latin-1, so every ligature and curly quote came out as a control character.

Both are repaired here, and the repair is the reason this file is worth committing:

  * **Word gaps.** Inside a TJ array a kern more negative than -KERN_SPACE thousandths of
    an em is emitted as a space. That is the ordinary heuristic and it is a heuristic.
  * **Ligatures and quotes.** Subsetted fonts in this article map `fi`, `ffi`, `Th` and the
    Czech diacritics onto codes 0x02-0x08, and the same code means different letters in
    different fonts: 0x02 is `fi` in the roman and `Ě` in the Czech font of the same file.
    A single global table therefore cannot work. So the font resources are resolved per
    page, each font's /ToUnicode CMap is parsed, and every string is decoded through the
    map of the font in force at that point in the content stream. Where a font has no
    /ToUnicode -- the 2004 essay, which uses the standard fonts -- the bytes are decoded
    as cp1252, which is what such files actually carry.

It remains an approximation of a renderer: it does not do columns, and a heuristic decides
word gaps. No quotation in this night's work rests on it alone -- verify.py reconciles every
quote against the whitespace-stripped glyph sequence, which is the one thing this extractor
gets right without a heuristic: the order of the characters.

    python3 extract.py            # every .pdf beside this file
"""

import os
import re
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
KERN_SPACE = 180                       # thousandths of an em; below this, a word gap
OBJ = re.compile(rb"(\d+)\s+0\s+obj\b(.*?)\bendobj", re.S)
STREAM = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.S)
TOKEN = re.compile(rb"\[(.*?)\]\s*TJ|(\((?:\\.|[^\\()])*\))\s*Tj|/(\w+)\s+[\d.]+\s+Tf|(T\*|')", re.S)
PIECE = re.compile(rb"\((?:\\.|[^\\()])*\)|-?\d+(?:\.\d+)?")
SIMPLE = {b"n": b"\n", b"r": b"", b"t": b" ", b"b": b"", b"f": b"",
          b"(": b"(", b")": b")", b"\\": b"\\"}


def unescape(s):
    """PDF string escapes, by hand: re.sub cannot be used, because the replacement for a
    backslash is itself a template escape."""
    out, i = [], 0
    while i < len(s):
        c = s[i:i + 1]
        if c != b"\\":
            out.append(c)
            i += 1
            continue
        nxt = s[i + 1:i + 2]
        if nxt in SIMPLE:
            out.append(SIMPLE[nxt])
            i += 2
        elif nxt.isdigit():
            j = i + 1
            while j < len(s) and j < i + 4 and s[j:j + 1].isdigit():
                j += 1
            out.append(bytes([int(s[i + 1:j], 8) & 0xFF]))
            i = j
        else:
            i += 1
    return b"".join(out)


def objects(data):
    return {int(n): body for n, body in OBJ.findall(data)}


def stream_of(body):
    m = STREAM.search(body)
    if not m:
        return None
    try:
        return zlib.decompress(m.group(1))
    except zlib.error:
        return m.group(1)


def parse_tounicode(cmap):
    """Return {byte code: text}. Handles bfchar and bfrange, 1- and 2-byte source codes."""
    table = {}

    def txt(h):
        s = bytes.fromhex(h.decode("ascii")).decode("utf-16-be", "replace")
        return s.replace("�", "")

    for block in re.findall(rb"beginbfchar(.*?)endbfchar", cmap, re.S):
        for src, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block):
            table[int(src, 16)] = txt(dst)
    for block in re.findall(rb"beginbfrange(.*?)endbfrange", cmap, re.S):
        for lo, hi, dst in re.findall(rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block):
            base = int(dst, 16)
            for k, code in enumerate(range(int(lo, 16), int(hi, 16) + 1)):
                table[code] = chr(base + k)
    return table



# --- the file's own Unicode table is wrong, and the file says so twice -------------------
#
# In the 2016 article every subsetted Minion font puts its ligatures on codes 0x02-0x08 and
# then hands out a /ToUnicode CMap that maps those codes **to themselves**: <02> -> <02>.
# A reader that trusts /ToUnicode therefore drops `fi`, `fl`, `ff`, `ffi` and `Th` silently
# -- "scientific" arrives as "scienti c", "This" as " is" -- with no error anywhere, because
# the page still *renders* correctly: rendering uses the glyph outlines, which are intact.
# The second table in the same file, the /Encoding /Differences array, names those glyphs
# properly (/f_i, /T_h, /f_f_i). So where /ToUnicode maps a code to itself, or has nothing,
# the glyph name wins. Only the ligature and space names are resolved here; everything else
# is left to /ToUnicode, which is right about the rest.
GLYPH = {"space": " ", "uni00A0": "\u00a0"}


def from_glyph_name(name):
    if re.fullmatch(r"uni[0-9A-Fa-f]{4}", name):
        return chr(int(name[3:], 16))
    if name in GLYPH:
        return GLYPH[name]
    parts = name.split("_")
    if len(parts) > 1 and all(len(p) == 1 and p.isalpha() for p in parts):
        return "".join(parts)          # f_i, T_h, f_f_i -- a ligature named by its letters
    return None


def differences(objs, font_body):
    """{code: text} from the font's /Encoding /Differences array, ligatures only."""
    enc = re.search(rb"/Encoding\s+(\d+)\s+0\s+R|/Encoding\s*<<(.*?)>>", font_body, re.S)
    if not enc:
        return {}
    body = objs.get(int(enc.group(1)), b"") if enc.group(1) else enc.group(2)
    arr = re.search(rb"/Differences\s*\[(.*?)\]", body, re.S)
    if not arr:
        return {}
    out, code = {}, 0
    for tok in re.findall(rb"\d+|/[^\s/\]]+", arr.group(1)):
        if tok.isdigit():
            code = int(tok)
            continue
        text = from_glyph_name(tok[1:].decode("latin-1"))
        if text is not None:
            out[code] = text
        code += 1
    return out


def font_maps(objs, page_body):
    """{resource name: code->text} for the fonts a page declares."""
    out = {}
    m = re.search(rb"/Font\s*<<(.*?)>>", page_body, re.S)
    if not m:
        return out
    for name, num in re.findall(rb"/(\w+)\s+(\d+)\s+0\s+R", m.group(1)):
        font = objs.get(int(num), b"")
        table = {}
        tu = re.search(rb"/ToUnicode\s+(\d+)\s+0\s+R", font)
        if tu:
            cmap = stream_of(objs.get(int(tu.group(1)), b""))
            if cmap:
                table = parse_tounicode(cmap)
        for code, text in differences(objs, font).items():
            if table.get(code, "") in ("", chr(code)):
                table[code] = text
        if table:
            out[name.decode("ascii")] = table
    return out


def decode(raw, table):
    if table:
        return "".join(table.get(b, chr(b) if b >= 32 else "") for b in raw)
    return raw.decode("cp1252", "replace")


def page_text(content, maps):
    cur, buf = None, []
    for m in TOKEN.finditer(content):
        arr, tj, font, nl = m.groups()
        if font is not None:
            cur = maps.get(font.decode("ascii"))
        elif nl is not None:
            buf.append("\n")
        elif tj is not None:
            buf.append(decode(unescape(tj[1:-1]), cur))
        else:
            for piece in PIECE.findall(arr):
                if piece.startswith(b"("):
                    buf.append(decode(unescape(piece[1:-1]), cur))
                else:
                    try:
                        if float(piece) < -KERN_SPACE:
                            buf.append(" ")
                    except ValueError:
                        pass
    return "".join(buf)


def extract(path):
    data = open(path, "rb").read()
    objs = objects(data)
    pages = [(n, b) for n, b in objs.items() if re.search(rb"/Type\s*/Page[^s]", b)]
    if pages:
        out = []
        for _, body in sorted(pages, key=lambda kv: kv[0]):
            cref = re.search(rb"/Contents\s+(\d+)\s+0\s+R", body)
            if not cref:
                continue
            content = stream_of(objs.get(int(cref.group(1)), b""))
            if content:
                out.append(page_text(content, font_maps(objs, body)))
        return "\n".join(out)
    # no page tree we can follow: fall back to every Flate stream in file order
    out = []
    for m in STREAM.finditer(data):
        try:
            out.append(page_text(zlib.decompress(m.group(1)), {}))
        except zlib.error:
            continue
    return "\n".join(out)


if __name__ == "__main__":
    names = sys.argv[1:] or sorted(f for f in os.listdir(HERE) if f.lower().endswith(".pdf"))
    if not names:
        print("no PDF beside this file -- re-fetch the sources named in MANIFEST.json first")
    for fn in names:
        src = os.path.join(HERE, fn)
        text = extract(src)
        dst = src[:-4] + ".txt"
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"{fn} -> {os.path.basename(dst)}  {len(text)} chars, {len(text.split())} tokens")
