"""Counts the tagged changes in MAKING.md and the draw's candidates; writes results.json.
A change is a bullet under a 'What changes for N' heading. Its first tag in bold (M, R, H, L, E)
is its source; **SELECT** marks a selection. Run from this directory."""
import json, re
text = open("MAKING.md").read()
changes = []
for m in re.finditer(r"\*\*What changes for (\d+)[^\n]*\n((?:- .*\n(?:  .*\n)*)+)", text):
    for b in re.findall(r"^- (.*(?:\n  .*)*)", m.group(2), re.M):
        tags = re.findall(r"\*\*(M|R|H|L|E|SELECT)\*\*", b)
        src = next((t for t in tags if t != "SELECT"), None)
        if src is None: continue  # a statement that no change is made (entry 3's last bullet)
        changes.append({"for": int(m.group(1)), "source": src, "select": "SELECT" in tags, "text": " ".join(b.split())})
sel = [c for c in changes if c["select"]]
draw = json.load(open("draw-log.json")); run2 = json.load(open("draw-run2-log.json"))
uri = lambda f: (f or "").rstrip("/").rsplit("/", 1)[-1].upper()
ok = {"CSV", "JSON", "GEOJSON", "XLSX", "XLS", "TXT", "XML"}
r = {"changes": changes,
     "by_source": {k: sum(c["source"] == k for c in changes) for k in "MRHLE"},
     "selections": len(sel), "selections_by_source": {k: sum(c["source"] == k for c in sel) for k in "MRHLE"},
     "Q3_prior_share_of_selections": round(sum(c["source"] in "RH" for c in sel) / len(sel), 3),
     "draw": {"count_at_draw": draw["count_at_draw"], "first_index": draw["first_index"],
              "admitted_index": draw["candidates"][-1]["index"],
              "refused_by_rule": len(draw["candidates"]) - 1,
              "run1_refusals_before_reset": sum("refused" in l for l in open("draw-run1-stderr.txt")),
              "run2_refusals_that_carried_an_admitted_format": sum(any(uri(f) in ok for f in c["formats"]) for c in run2["candidates"]),
              "run2_candidates": len(run2["candidates"])}}
json.dump(r, open("results.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in r.items() if k != "changes"}, indent=1))
