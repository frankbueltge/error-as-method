"""Build index.html, the face of *Withdrawn* (Session 104), from notices.json and coded.json.
Everything inline; nothing is fetched. Category per notice, in this order of precedence:
0 bare (corrected coder) · 1 withdrawn by administrators · 2 error, located · 3 error, not located
· 4 a reason that is not an error. 'other' (a third party named) is drawn as a dot."""
import json, html
n = {r["id"]: r for r in json.load(open("notices.json"))}
rows = []
for c in json.load(open("coded.json")):
    r = n[c["id"]]
    k = 0 if c["bare_corrected"] else 1 if c["admin"] else 2 if c["located"] else 3 if c["error"] else 4
    rows.append([r["updated"], c["id"], k, c["other"], r["comment"]])
rows.sort()
data = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
counts = [sum(1 for r in rows if r[2] == k) for k in range(5)]
tpl = open("page.tpl.html").read()
out = tpl.replace("/*DATA*/[]", data).replace("{{N}}", f"{len(rows):,}")
for k, v in enumerate(counts):
    out = out.replace("{{C%d}}" % k, f"{v:,}")
open("index.html", "w").write(out)
print(len(out), counts)
