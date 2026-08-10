#!/usr/bin/env python3
"""The session ledger, read off the record instead of off a sentence.

Written on 2026-08-10 (session 44), after the restoration note in PROTOCOL.md, the
table in README.md and the instruction that started that night all said the next
session was 27 — a number that had been in use since 2026-07-14. None of the three
descends from `journal/`; all three descend from the header of one position paper.

So: derive it. This prints every session number the journal actually claims, the
gaps, the collisions, and the next free number. Run it during orientation and copy
from here, not from prose.

    python3 tools/sessions.py
"""
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOURNAL = os.path.join(ROOT, "journal")
# Both spellings the record uses, in headers and in the italic mode line beneath.
PAT = re.compile(r"\b(?:Session|Sitzung)\s*(\d{1,3})\b", re.I)


def ledger(path=JOURNAL):
    found = defaultdict(list)
    for fn in sorted(os.listdir(path)):
        if not fn.endswith(".md"):
            continue
        head = open(os.path.join(path, fn), encoding="utf-8").read(600)
        m = PAT.search(head)
        if m:
            found[int(m.group(1))].append(fn)
        else:
            found.setdefault(None, []).append(fn)
    return found


def main():
    found = ledger()
    unnumbered = found.pop(None, [])
    numbers = sorted(found)
    print(f"journal entries carrying a session number : {sum(len(v) for v in found.values())}")
    print(f"entries with no session number in the head: {len(unnumbered)}")
    for fn in unnumbered:
        print(f"    {fn}")
    print(f"lowest / highest session number           : {numbers[0]} / {numbers[-1]}")
    missing = [n for n in range(numbers[0], numbers[-1] + 1) if n not in found]
    print(f"gaps                                      : {missing or 'none'}")
    collisions = {n: v for n, v in found.items() if len(v) > 1}
    for n, v in sorted(collisions.items()):
        print(f"collision: session {n} claimed by {', '.join(v)}")
    print(f"NEXT FREE SESSION NUMBER                  : {numbers[-1] + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
