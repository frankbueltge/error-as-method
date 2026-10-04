"""Build index.html from page.tpl.html, verdicts.jsonl, NORMS.md and results.json."""
import json, re
P = lambda i: " · ".join([["line", "strip", "spiral", "decades"][i // 6], ["raw", "seasonal", "tidal"][(i // 2) % 3], ["linear", "rank"][i % 2]]) if i < 24 else "from the norms"
R = json.load(open("results.json")); age = {v["order"]: v["age"] for v in R["per_verdict"]}
V = [json.loads(l) for l in open("verdicts.jsonl")]
revs = [{"revises": v["revises"], "seen": v["seen"]} for v in V if "revises" in v]
prim = [dict(order=v["order"], variant=v["variant"], verdict=v["verdict"], decisive=v["decisive"], age=age[v["order"]], seen=v["seen"],
             params=P(v["variant"]), revised=any(r["revises"] == v["order"] for r in revs)) for v in V if "revises" not in v]
minted = {n: v["order"] for v in V if "revises" not in v for n in v.get("minted", [])}
norms = []
for m in re.finditer(r"- \*\*(N[0-9.]+)\*\*(?: \*\([^)]*\)\*)?\s+(.+?)(?=\n- \*\*|\n\n|\Z)", open("NORMS.md").read(), re.S):
    norms.append({"id": m.group(1), "at": 0 if m.group(1).startswith("N0") else minted[m.group(1)], "text": " ".join(m.group(2).split())})
grid_works = sum(1 for v in prim if v["variant"] < 24 and v["verdict"] == "works")
data = {"verdicts": prim, "revisions": revs, "norms": norms, "fails": R["fails_by_age"], "works": grid_works}
html = open("page.tpl.html").read().replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
open("index.html", "w").write(html); print(len(prim), "verdicts,", len(norms), "norms,", len(html), "bytes")
