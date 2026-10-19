#!/usr/bin/env python3
"""Write face-data.js for index.html from the committed answers. Stdlib, no network.

    python3 -I build_face.py
"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
L = lambda p: json.load(open(os.path.join(H, p)))
res = L("results.json")
party134 = L("../2026-10-18-not-a-defect/party.json")["refused"]
codes134 = {r: {e["id"]: e for e in L(f"../2026-10-18-not-a-defect/readers/reader-{r}.json")} for r in ("A", "B")}
ans = {r: {e["id"]: e for e in L(f"readers/reader-{r}.json")} for r in ("D1", "D2", "O1", "O2")}
rows = []
for e in res["per_entry"]:
    i = e["id"]
    row = {"id": i, "issue": e["issue"], "status": e["status"], "cells": {}}
    for r in ("A", "B"):
        p = party134[r].get(i, "standard") if e["status"] == "NAD" else "standard"
        c = codes134[r][i]
        row["cells"]["134" + r] = [p, c["wrong"], c["held"], c["judged"]]
    for r in ans:
        c = ans[r][i]
        row["cells"][r] = [e[r + "_party"], c["wrong"], c["held"], c["judged"]]
    rows.append(row)
out = "window.FACE = " + json.dumps({"rows": rows}, separators=(",", ":")) + ";\n"
open(os.path.join(H, "face-data.js"), "w").write(out)
print(len(rows), "rows,", len(out), "bytes")
