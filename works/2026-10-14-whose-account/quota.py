#!/usr/bin/env python3
"""Fill the four cells from sort.json in walk order; report counts and the selected ids.
Reads the hidden status from order.json. Writes selected.json.  python3 -I quota.py"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
order = json.load(open(os.path.join(H, "order.json")))["order"]
srt = json.load(open(os.path.join(H, "sort.json")))["sort"]
Q = 15
cells = {(g, s): [] for g in "SA" for s in ("Verified", "Rejected")}
walked = 0
for k, (eid, st) in enumerate(order):
    if eid not in srt:
        break
    walked = k + 1
    g = srt[eid]["group"]
    if g in "SA" and len(cells[(g, st)]) < Q:
        cells[(g, st)].append(eid)
    if all(len(v) >= Q for v in cells.values()):
        break
full = all(len(v) >= Q for v in cells.values())
json.dump({"walked": walked, "full": full, "cells": {f"{g}-{s}": v for (g, s), v in cells.items()}},
          open(os.path.join(H, "selected.json"), "w"), indent=1)
print("walked", walked, "full", full, {f"{g}-{s}": len(v) for (g, s), v in cells.items()})
