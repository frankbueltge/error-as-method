#!/usr/bin/env python3
"""
evidence.py -- Session 54. Writes sources/evidence-*.txt: the exact rows of the
consortium's own data files on which the two withdrawal claims rest, so a reader
can check them without downloading 68 MB of archives.

Offline; reads ./cache/, which harvest.py fills and .gitignore keeps out of the
repository. Also cuts NamesList.txt down to the annotations the work quotes --
the full file is 2 MB and is a retrievable public file, not something this
repository should carry a copy of.
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
SRC = os.path.join(HERE, "sources")


def rows(version, lo, hi):
    out = []
    with open(os.path.join(CACHE, "UnicodeData-%s.txt" % version), encoding="utf-8",
              errors="replace") as f:
        for line in f:
            m = re.match(r"^([0-9A-Fa-f]{4,6});", line)
            if m and lo <= int(m.group(1), 16) <= hi:
                out.append(line.rstrip("\n"))
    return out


def block(title, version, filename, lo, hi, limit=6):
    r = rows(version, lo, hi)
    head = ["", "-" * 76, "%s" % title,
            "  file    : %s (directory %s of unicode.org/Public/)" % (filename, version),
            "  range   : U+%04X..U+%04X" % (lo, hi),
            "  rows    : %d" % len(r), "-" * 76]
    if not r:
        return head + ["  (no rows -- these code points are unassigned in this version)"]
    if len(r) <= limit * 2:
        return head + ["  " + x for x in r]
    return (head + ["  " + x for x in r[:limit]]
            + ["  ... %d rows omitted ..." % (len(r) - 2 * limit)]
            + ["  " + x for x in r[-limit:]])


def main():
    L = ["EVIDENCE FOR THE TWO WITHDRAWALS",
         "Session 54, 2026-08-13. Rows copied verbatim from the UnicodeData.txt files",
         "published by the Unicode Consortium at https://www.unicode.org/Public/ .",
         "Their SHA-256 hashes are in MANIFEST.json. Nothing here is retyped: every line",
         "below was cut out of the downloaded file by this script.",
         ""]

    L += ["", "=" * 76,
          "1. THE HANGUL SYLLABLES AT U+3400..U+4DFF -- assigned, withdrawn, reoccupied",
          "=" * 76]
    L += block("As shipped in Unicode 1.1.5 (July 1995): 6,656 named Hangul syllables",
               "1.1-Update", "UnicodeData-1.1.5.txt", 0x3400, 0x4DFF)
    L += block("The same range one release later, in Unicode 2.0.0 (July 1996)",
               "2.0-Update", "UnicodeData-2.0.14.txt", 0x3400, 0x4DFF)
    L += block("Where the syllables went in 2.0.0 -- a different address, 11,172 of them",
               "2.0-Update", "UnicodeData-2.0.14.txt", 0xAC00, 0xD7A3)
    L += block("Who lives at U+3400 today", "18.0.0", "UnicodeData.txt (18.0.0)",
               0x3400, 0x3401)

    L += ["", "=" * 76,
          "2. TIBETAN AT U+1000..U+104C -- assigned, withdrawn, reoccupied",
          "=" * 76]
    L += block("Unicode 1.0.1 (reconstructed file; code points and names stated accurate)",
               "1.0.1", "UnicodeData-1.0.1.txt", 0x1000, 0x1005)
    L += block("The same range in Unicode 1.1.5", "1.1-Update", "UnicodeData-1.1.5.txt",
               0x1000, 0x1005)
    L += block("Who lives there today", "18.0.0", "UnicodeData.txt (18.0.0)", 0x1000, 0x1005)

    L += ["", "=" * 76,
          "3. THE ONLY TWO NAME CHANGES AFTER THE 1996 FREEZE, AND WHAT THEY WERE",
          "=" * 76,
          "Unicode 4.0.0 shipped two character names with a trailing space; 4.0.1 removed",
          "it. Under the Name Stability policy the Name property value may not change, so",
          "the repair is of the data file's typography, not of the name. Quoted with the",
          "line ends marked | so the space is visible."]
    for v, fn in (("4.0-Update", "UnicodeData-4.0.0.txt"),
                  ("4.0-Update1", "UnicodeData-4.0.1.txt"),
                  ("18.0.0", "UnicodeData.txt (18.0.0)")):
        L.append("")
        L.append("  %s" % fn)
        for lo, hi in ((0x02AE, 0x02AE), (0x0615, 0x0615)):
            for r in rows(v, lo, hi):
                L.append("    " + ";".join(r.split(";")[:2]) + "|")

    with open(os.path.join(SRC, "evidence-withdrawals.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("wrote sources/evidence-withdrawals.txt (%d lines)" % len(L))

    # NamesList.txt -> only the annotated characters the work quotes.
    full = os.path.join(SRC, "NamesList.txt")
    if os.path.exists(full):
        want = {"027F", "0709", "0CDE", "0E9D", "0E9F", "0EA3", "0EA5",
                "0F0B", "0F0C", "1BBD", "A015"}
        out, keep, cur = [], False, None
        for raw in open(full, encoding="utf-8", errors="replace"):
            m = re.match(r"^([0-9A-F]{4,6})\t", raw)
            if m:
                cur = m.group(1)
                keep = cur in want
            if keep:
                out.append(raw.rstrip("\n"))
        header = [
            "NamesList.txt -- extract, Session 54.",
            "Source: https://www.unicode.org/Public/UCD/latest/ucd/NamesList.txt",
            "SHA-256 of the full file is in MANIFEST.json. The full file is 2 MB and is a",
            "public retrievable file; only the characters this work quotes are kept here.",
            "These are the eleven characters whose chart annotation says, in the standard's",
            "own words, that the character's name is a mistake or a misnomer.",
            "",
        ]
        with open(os.path.join(SRC, "NamesList-misnomers.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(header + out) + "\n")
        os.replace(full, os.path.join(CACHE, "NamesList.txt"))
        print("wrote sources/NamesList-misnomers.txt (%d lines); moved the 2 MB full "
              "file to cache/ so measure.py can still read it" % len(out))


if __name__ == "__main__":
    main()
