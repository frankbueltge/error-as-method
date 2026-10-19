"""facedata.py -- writes face-data.js for the face: every kept version (its html, its note, the maker's hand-back,
its bytes) and the blind coder's code and reason for each step, keyed back to lineage and step by coder/key.json."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, "plan.json")))
V = {(r["lineage"], r["v"]): r for r in map(json.loads, open(os.path.join(HERE, "versions.jsonl")))}
key = json.load(open(os.path.join(HERE, "coder", "key.json")))
ans = json.load(open(os.path.join(HERE, "coder", "answer.json")))["pairs"]
code = {(k["lineage"], k["to"]): ans[t] for t, k in key.items()}
rd = lambda *p: open(os.path.join(HERE, *p), encoding="utf-8").read()
out = []
for L in plan["lineages"]:
    vs = []
    for v in range(1, 5):
        note = rd("lineages", L["lineage"], "v%d" % v, "NOTE.md")
        title = (re.search(r"^#\s+(.+)$", note, re.M) or [None, ""])[1].strip()
        if L["arm"] in "PT" and v > 1:
            parts = re.split(r"^(## v%d\b.*)$" % v, note, flags=re.M)
            sect = (parts[1] + re.split(r"^## v\d", parts[2], flags=re.M)[0]) if len(parts) > 2 else note
        else:
            sect = note
        c = code.get((L["lineage"], v))
        vs.append({"v": v, "title": title, "bytes": V[(L["lineage"], v)]["bytes"], "note": sect.strip(),
                   "report": rd("reports", "%s-v%d.md" % (L["lineage"], v)).strip(),
                   "html": rd("lineages", L["lineage"], "v%d" % v, "index.html"),
                   "code": c["code"] if c else None, "reason": c["reason"] if c else None})
    out.append({"lineage": L["lineage"], "arm": L["arm"], "versions": vs})
open(os.path.join(HERE, "face-data.js"), "w", encoding="utf-8").write(
    "window.FACE = " + json.dumps(out, ensure_ascii=False) + ";\n")
print(sum(len(x["versions"]) for x in out), "versions;", os.path.getsize(os.path.join(HERE, "face-data.js")), "bytes")
