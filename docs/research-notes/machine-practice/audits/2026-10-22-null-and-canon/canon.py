#!/usr/bin/env python3
"""Count canon.json. No fetching; the placements are hand-coded in canon.json."""
import json, collections, pathlib
c = json.loads((pathlib.Path(__file__).parent / "canon.json").read_text())
for exp, rooms in c["rooms"].items():
    n = collections.Counter(v[2] for v in rooms.values())
    print(f"{exp}: {len(rooms)} choices  SAME {n['SAME']}  KIN {n['KIN']}  NONE {n['NONE']}  "
          f"-> in the canon {n['SAME'] + n['KIN']} of {len(rooms)}")
