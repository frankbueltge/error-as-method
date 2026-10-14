#!/usr/bin/env python3
"""Write data.js for the face from the committed files only (no network, no errata text).

Every string in data.js is this practice's or its readers' own wording (held / judged), plus the
erratum id and RFC number, which link to the register's own page.
"""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
L = lambda p: json.load(open(os.path.join(H, p)))
order = L("order.json")["order"]; srt = L("sort.json")["sort"]
ent = L("entries.json")["rows"]; me = {r["id"]: r for r in L("practice.json")["rows"]}
rd = {k: {r["id"]: r for r in L(f"readers/reader-{k}.json")} for k in "AB"}
res = L("results.json")
walk = [[eid, srt[eid]["group"], st[0]] for eid, st in order[:len(srt)]]
rows = []
for r in ent:
    i = r["label"]
    rows.append({"id": i, "eid": r["eid"], "doc": r["doc"], "g": r["group"], "st": r["status"],
                 "P": [me[i]["held"], me[i]["judged"], me[i]["wrong"]],
                 "A": [rd["A"][i]["held"], rd["A"][i]["judged"], rd["A"][i]["wrong"]],
                 "B": [rd["B"][i]["held"], rd["B"][i]["judged"], rd["B"][i]["wrong"]]})
pooled = {g: {k: v for k, v in res["pooled"][g].items() if k != "list"} for g in "SA"}
data = {"walk": walk, "rows": rows, "pooled": pooled, "verdict": res["verdict"],
        "per_reader": res["per_reader"], "rr": res["reader_vs_reader"], "holder": res["holder"]}
VTEXT = ("No reader ever struck the other term from the practice, in either column: 0 side-splits among "
         f"{pooled['S']['disagreements']} disagreements on standard rows, 0 among {pooled['A']['disagreements']} on account rows. "
         "20 of the 23 disagreements are one kind: on a rejected report the practice struck the reporter's reference, "
         "and both readers struck nothing. The two readers agreed with each other on 55 of 57. On this register it was not "
         "the readers who split over whose account counts. It was the practice that read a verifier's refusal as an error "
         "on the other side.")
open(os.path.join(H, "data.js"), "w").write("window.DATA=" + json.dumps(data, ensure_ascii=False) + ";\nwindow.VTEXT="
                                            + json.dumps(VTEXT) + ";\n")
print("data.js", len(rows), "rows,", len(walk), "walked")
