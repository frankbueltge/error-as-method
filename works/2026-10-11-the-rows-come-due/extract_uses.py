#!/usr/bin/env python3
"""S99.JOIN clause (b): every use of `error`/`errors`/`erroneous` in the journals of Sessions 100-119,
with the line before and after. Writes uses.json. Stdlib, no network, reads only committed files."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
WORD = re.compile(r"\b(errors?|erroneous)\b", re.I)
SESSION = re.compile(r"Session (\d+)")
rows = []
for name in sorted(os.listdir(os.path.join(ROOT, "journal"))):
    if not name.endswith(".md"):
        continue
    path = os.path.join(ROOT, "journal", name)
    lines = open(path, encoding="utf-8").read().split("\n")
    m = SESSION.search("\n".join(lines[:3]))
    if not m or not 100 <= int(m.group(1)) <= 119:
        continue
    s = int(m.group(1))
    for i, line in enumerate(lines):
        for hit in WORD.finditer(line):
            rows.append({"id": f"U{len(rows)+1:03d}", "session": s, "file": f"journal/{name}", "line": i + 1,
                         "word": hit.group(0),
                         "context": "\n".join(lines[max(0, i - 1): i + 2])})
json.dump({"_what": "Every use of error/errors/erroneous in journal entries of Sessions 100-119 (S99.JOIN clause b).",
           "n": len(rows), "uses": rows}, open(os.path.join(HERE, "uses.json"), "w"), indent=1, ensure_ascii=False)
print(len(rows), "uses in", len({r['file'] for r in rows}), "journals")
