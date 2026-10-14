#!/usr/bin/env python3
"""Build the readers' ENTRIES.md from selected.json and the errata dump (NOT committed; its hash is).

    python3 -I entries.py <errata.json> <out.md>   ->  also writes entries.json (ids, labels, groups)

The 57 selected entries in one order, shuffled with random.Random(1271), each shown in full as the
register shows it: document, section, status, original text, corrected text, the reporter's notes
and the verifier's note. The group (S/A) is not shown.
"""
import hashlib, json, os, random, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
from draw import split  # noqa: E402
d = {e["errata_id"]: e for e in json.load(open(sys.argv[1]))}
sel = json.load(open(os.path.join(H, "selected.json")))["cells"]
rows = [(eid, cell.split("-")[0], cell.split("-")[1]) for cell, ids in sel.items() for eid in ids]
rows.sort(key=lambda r: int(r[0]))
random.Random(1271).shuffle(rows)
out, meta = [], []
for i, (eid, g, st) in enumerate(rows, 1):
    e = d[eid]
    rep, ver = split(e)
    lab = f"E{i:02d}"
    meta.append({"label": lab, "eid": eid, "doc": e["doc-id"], "group": g, "status": st})
    out.append(f"## {lab} (erratum {eid}, {e['doc-id']}, section {e['section']})\n\n"
               f"**Status recorded by the verifier:** {st}\n\n"
               f"**Original text:**\n```\n{(e.get('orig_text') or '').strip()}\n```\n\n"
               f"**Corrected text proposed by the reporter:**\n```\n{(e.get('correct_text') or '').strip()}\n```\n\n"
               f"**Reporter's notes:**\n```\n{rep.strip()}\n```\n\n"
               f"**Verifier's note:**\n```\n{ver.strip()}\n```\n")
txt = ("# Entries\n\n" + str(len(rows)) + " erratum reports filed against published RFCs, "
       "each with the outcome its verifier recorded.\n\n" + "\n".join(out))
open(sys.argv[2], "w").write(txt)
json.dump({"seed": 1271, "sha256_entries_md": hashlib.sha256(txt.encode()).hexdigest(), "rows": meta},
          open(os.path.join(H, "entries.json"), "w"), indent=1)
print(len(rows), "entries", hashlib.sha256(txt.encode()).hexdigest())
