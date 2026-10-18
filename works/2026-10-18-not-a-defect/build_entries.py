#!/usr/bin/env python3
"""Write the entries file every coder reads, from draw.py's entries.json. Stdlib.

    python3 -I build_entries.py <entries.json> <ENTRIES.md>
"""
import json, sys
d = json.load(open(sys.argv[1]))
out = []
for i, e in enumerate(d, 1):
    oc = "NAD (not a defect)" if e["status"] == "NAD" else "accepted as a defect; resolution adopted in " + e["status"]
    out.append(f"## E{i:02d}\n\nIssue {e['id']}: {e['title']}\nSection: {e['section']}\nOutcome recorded: {oc}\n\n{e['text']}\n")
open(sys.argv[2], "w").write("\n---\n\n".join(out))
print(len(d), "entries")
