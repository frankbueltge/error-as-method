#!/usr/bin/env python3
"""Append sort decisions to sort.json. Lines on stdin: '<walkpos> <S|A|N> <short reason>'."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
order = json.load(open(os.path.join(H, "order.json")))["order"]
p = os.path.join(H, "sort.json")
s = json.load(open(p)) if os.path.exists(p) else {"rule": "PREDICTIONS.md, 'Sorting before coding'; report only, status and verifier note hidden", "sort": {}}
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    k, g, why = line.split(" ", 2)
    k = int(k); assert g in "SAN"
    eid = order[k][0]
    assert len(s["sort"]) == k, (len(s["sort"]), k)
    s["sort"][eid] = {"k": k, "group": g, "why": why}
json.dump(s, open(p, "w"), indent=0, ensure_ascii=False)
print(len(s["sort"]), "sorted")
