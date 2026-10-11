#!/usr/bin/env python3
"""Extract F-193 to F-213 verbatim from the register into readers/ENTRIES.md. Stdlib, no network."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
out = ["# The 21 entries, verbatim", "",
       "Extracted from works/fehlerkataster-063.md to -069.md by extract_entries.py. Nothing edited.", ""]
for n in range(63, 70):
    text = open(os.path.join(ROOT, "works", f"fehlerkataster-{n:03d}.md"), encoding="utf-8").read()
    for block in re.split(r"(?m)^(?=## F-)", text)[1:]:
        block = re.split(r"(?m)^---\s*$|^\*Ulysses", block)[0].rstrip()
        out += [block, ""]
open(os.path.join(HERE, "readers", "ENTRIES.md"), "w", encoding="utf-8").write("\n".join(out))
print(sum(1 for l in out if l.startswith("## F-")), "entries")
