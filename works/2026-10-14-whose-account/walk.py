#!/usr/bin/env python3
"""Print walk positions a..b of order.json showing the REPORT ONLY (no status, no verifier note).

    python3 -I walk.py <errata.json> a b
"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
from draw import split  # noqa: E402  (same directory)
d = {e["errata_id"]: e for e in json.load(open(sys.argv[1]))}
order = json.load(open(os.path.join(H, "order.json")))["order"]
a, b = int(sys.argv[2]), int(sys.argv[3])
for k in range(a, min(b, len(order))):
    e = d[order[k][0]]
    rep, _ = split(e)
    print(f"=== #{k} eid{e['errata_id']} {e['doc-id']} §{e['section']}")
    print("ORIG:", (e.get("orig_text") or "").strip()[:900])
    print("CORR:", (e.get("correct_text") or "").strip()[:900])
    print("NOTE:", rep.strip())
