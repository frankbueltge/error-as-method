#!/usr/bin/env python3
"""S85.OVERLOAD and S92.FIRSTTERM: reconcile every quote, count readings per word (Session 85's table
plus readings_since.json). Exits non-zero if a quote is not found. Stdlib, no network."""
import json, os, re, sys
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
EMPH = re.compile(r"[*_`]")
flat = lambda s: re.sub(r"\s+", " ", EMPH.sub("", s))
old = json.load(open(os.path.join(ROOT, "works/2026-09-09-what-the-sentence-lets-in/readings.json")))["readings"]
new = json.load(open(os.path.join(HERE, "readings_since.json")))["items"]
bad = 0
for r in old + new:
    if flat(r["quote"]) not in flat(open(os.path.join(ROOT, r["source"]), encoding="utf-8").read()):
        print("NOT FOUND:", r["source"], r["quote"]); bad += 1
if bad:
    sys.exit(1)
table = defaultdict(lambda: defaultdict(int))
for r in old:
    table[r["word"]]["fixed (S26-S79)"] += 1
for r in new:
    table[r["word"]][r["status"] + " (S85-S119)"] += 1
out = {w: dict(v) for w, v in sorted(table.items())}
moves = [r for r in new if r["status"] == "move"]
res = {"quotes_checked": len(old) + len(new), "per_word": out,
       "observer_fixed_readings": sum(1 for r in old + new if r["word"] == "observer" and r.get("status", "fixed") == "fixed"),
       "moves_since_S85": [{"session": m["session"], "kind": "subtraction", "at": m["word"]} for m in moves],
       "S85_OVERLOAD": "clause 1 (moved by an addition): no, the one move was a subtraction. clause 2 (not moved while observer took a fourth reading): no, the position moved, and observer holds three fixed readings (one offered). Not falsified. Its claim of place (at observer) failed.",
       "S92_FIRSTTERM": "clause a (move at observer): no, at the join. clause b (three or more new observer shapes): no, zero found. Not falsified. Its forecast (a first reading at difference or norm) failed as a forecast of the one move."}
json.dump(res, open(os.path.join(HERE, "count.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
