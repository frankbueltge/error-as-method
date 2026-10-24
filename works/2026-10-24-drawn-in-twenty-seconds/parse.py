#!/usr/bin/env python3
"""Parse rooms/<maker>.txt into drawings.json: {maker: {category: strokes}}, by the maker's own order.
A reply line that does not parse as a stroke list is recorded as unparsed, never repaired."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
cats = [c["category"] for c in json.load(open(os.path.join(HERE, "plan.json")))["categories"]]
orders = json.load(open(os.path.join(HERE, "orders.json")))
out, bad = {}, []
for maker, order in orders.items():
    p = os.path.join(HERE, "rooms", maker + ".txt")
    if not os.path.exists(p):
        continue
    text = open(p).read()
    got = {}
    for m in re.finditer(r"^\s*(\d{1,2})\s*:\s*(\[.*\])\s*$", text, re.M):
        k = int(m.group(1))
        try:
            strokes = json.loads(m.group(2))
            assert isinstance(strokes, list) and strokes
            for s in strokes:
                assert len(s) == 2 and len(s[0]) == len(s[1]) and len(s[0]) >= 1
            got[cats[order[k - 1]]] = strokes
        except Exception as e:
            bad.append((maker, k, str(e)[:60]))
    out[maker] = got
json.dump(out, open(os.path.join(HERE, "drawings.json"), "w"), separators=(",", ":"))
for m, g in out.items():
    print(m, len(g))
print("unparsed:", bad)
