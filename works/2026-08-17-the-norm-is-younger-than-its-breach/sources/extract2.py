#!/usr/bin/env python3
"""Kerning-aware successor to sources/extract.py of 2026-08-16.

The 2026-08-16 extractor discarded the numbers inside TJ arrays, so its output was
unspaced. In these files inter-word space is carried by exactly those numbers: a
negative adjustment beyond a threshold is a space the typesetter took out of the
string. This one keeps them and re-inserts the space.
"""
import re, sys, zlib

TJ = re.compile(rb"\[(.*?)\]\s*TJ", re.S)
TJ_SIMPLE = re.compile(rb"(\((?:\\.|[^\\()])*\))\s*Tj", re.S)
PIECE = re.compile(rb"(\((?:\\.|[^\\()])*\))|(-?\d+\.?\d*)", re.S)
TD = re.compile(rb"(T\*|TD|Td|ET)")


def unescape(b):
    out = bytearray()
    i = 0
    while i < len(b):
        c = b[i]
        if c == 0x5C and i + 1 < len(b):
            nxt = b[i + 1]
            mapping = {0x6E: 10, 0x72: 13, 0x74: 9, 0x28: 40, 0x29: 41, 0x5C: 92}
            if nxt in mapping:
                out.append(mapping[nxt]); i += 2; continue
            if 0x30 <= nxt <= 0x37:
                m = re.match(rb"[0-7]{1,3}", b[i + 1:i + 4])
                out.append(int(m.group(0), 8) & 0xFF); i += 1 + len(m.group(0)); continue
            i += 2; continue
        out.append(c); i += 1
    return bytes(out)


def render_tj(inner, threshold=120):
    parts = []
    for m in PIECE.finditer(inner):
        if m.group(1) is not None:
            parts.append(unescape(m.group(1)[1:-1]).decode("latin-1"))
        else:
            if abs(float(m.group(2))) >= threshold and float(m.group(2)) < 0:
                parts.append(" ")
    return "".join(parts)


def extract(path, threshold=120):
    data = open(path, "rb").read()
    pages = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", data, re.S):
        try:
            content = zlib.decompress(m.group(1))
        except zlib.error:
            continue
        if b"TJ" not in content and b"Tj" not in content:
            continue
        buf = []
        pos = 0
        tokens = []
        for mm in re.finditer(rb"\[(.*?)\]\s*TJ|(\((?:\\.|[^\\()])*\))\s*Tj|(T\*|TD|Td)", content, re.S):
            tokens.append(mm)
        for mm in tokens:
            if mm.group(1) is not None:
                buf.append(render_tj(mm.group(1), threshold))
            elif mm.group(2) is not None:
                buf.append(unescape(mm.group(2)[1:-1]).decode("latin-1"))
            else:
                buf.append("\n")
        pages.append("".join(buf))
    return pages


if __name__ == "__main__":
    pages = extract(sys.argv[1])
    txt = "\n\n=== PAGE BREAK ===\n\n".join(pages)
    open(sys.argv[2], "w", encoding="utf-8").write(txt)
    print(len(pages), "streams,", len(txt), "chars")
