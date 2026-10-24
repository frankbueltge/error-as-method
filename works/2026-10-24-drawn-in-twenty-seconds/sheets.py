#!/usr/bin/env python3
"""Arm F's sheets: the six S drawings of each thing, S1..S6 left to right, no words."""
import json, os, shutil
from render import contact_sheet
HERE = os.path.dirname(os.path.abspath(__file__))
cats = [c["category"] for c in json.load(open(os.path.join(HERE, "plan.json")))["categories"]]
dr = json.load(open(os.path.join(HERE, "drawings.json")))
for i, c in enumerate(cats):
    p = os.path.join(HERE, "sheets", f"F-{i + 1:02d}.png")
    contact_sheet([dr[f"S{n}"][c] for n in range(1, 7)], p)
    shutil.copy(p, "/tmp/k/")
print("F sheets written")
