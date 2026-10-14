#!/usr/bin/env python3
"""Draw tonight's walk order from the RFC errata dump. Stdlib, no network.

    python3 -I draw.py <errata.json>   ->  writes order.json (ids in walk order, with hidden status)

The pool and the order are fixed in PREDICTIONS.md: Technical, Verified or Rejected; a Rejected
entry must carry a verifier's note of at least 20 characters; report and note together at most
3,000 characters; sorted by id, then random.Random(127).shuffle.
"""
import json, os, random, sys
H = os.path.dirname(os.path.abspath(__file__))
MARK = "--VERIFIER NOTES--"

def split(e):
    n = e.get("notes") or ""
    i = n.find(MARK)
    return (n, "") if i < 0 else (n[:i], n[i + len(MARK):])

def pool(d):
    out = []
    for e in d:
        if e["errata_type_code"] != "Technical" or e["errata_status_code"] not in ("Verified", "Rejected"):
            continue
        rep, ver = split(e)
        if e["errata_status_code"] == "Rejected" and len(ver.strip()) < 20:
            continue
        if len((e.get("orig_text") or "") + (e.get("correct_text") or "") + (e.get("notes") or "")) > 3000:
            continue
        out.append(e)
    out.sort(key=lambda e: int(e["errata_id"]))
    random.Random(127).shuffle(out)
    return out

if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    p = pool(d)
    json.dump({"pool": len(p), "order": [[e["errata_id"], e["errata_status_code"]] for e in p]},
              open(os.path.join(H, "order.json"), "w"))
    print(len(d), "entries,", len(p), "in the pool")
