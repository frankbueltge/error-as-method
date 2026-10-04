"""Score Q1-Q5 from FOLLOWING.md as committed (the cause tags) and the house-mould features judged
on iteration 5. Writes results.json."""
import json, re
F = open("FOLLOWING.md").read()
entries = re.split(r"\n## ", F)[1:]
changes = []
for e in entries:
    n = int(e.split(" ", 1)[0])
    if "What changes for" not in e: continue
    block = e.split("What changes for", 1)[1]
    for b in re.findall(r"\n- (.*?)(?=\n- |\n\n|\Z)", block, re.S):
        tags = re.findall(r"\*\*(material, encountered|material, recognised R\d+|legibility|error)\*\*", b)
        assert len(tags) == 1, (n, b[:80], tags)
        changes.append({"after_iteration": n, "tag": tags[0], "text": " ".join(b.split())})
mat = [c for c in changes if c["tag"].startswith("material")]
rec = [c for c in mat if "recognised" in c["tag"]]
# House-mould features in iteration 5, judged by reading iterations/5-regions.js (see work.md):
house = {"M1 one mark per record": False, "M2 the mark is a square": True, "M3 grid in time order": False,
         "M4 colour from one field (magnitude)": True, "M5 touch to read a record": True,
         "M6 legend with counts": False, "M7 serif on paper": True, "M8 one-sentence lede": True}
surv = sum(house.values())
R = {
 "changes": changes, "n_changes": len(changes), "n_material": len(mat), "n_recognised": len(rec),
 "house_features_iteration5": house, "house_surviving": surv,
 "Q1": {"rule": ">= 4 of 8 house features survive", "value": surv, "holds": surv >= 4,
        "strict_note": "M4 counted as surviving (same field, ramp instead of bands); without it 4, still holds"},
 "Q2": {"rule": "more than half of material changes recognised", "value": f"{len(rec)}/{len(mat)}", "holds": len(rec) * 2 > len(mat),
        "sensitivity": "the two bullets after iteration 2 are one decision; merged, 2/4 and Q2 fails"},
 "Q3": {"rule": "at least one iteration abandoned", "value": "iteration 4 (labelling)", "holds": True},
 "Q4": {"rule": "material changes fewer than half of all", "value": f"{len(mat)}/{len(changes)}", "holds": len(mat) * 2 < len(changes)},
 "Q5": {"rule": "stop before the cap of six by judgement", "value": "stopped after 5", "holds": True},
}
json.dump(R, open("results.json", "w"), indent=1, ensure_ascii=False)
for q in ["Q1", "Q2", "Q3", "Q4", "Q5"]: print(q, R[q]["value"], "holds" if R[q]["holds"] else "FALSIFIED")
