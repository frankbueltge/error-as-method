"""Assemble index.html: the six iterations exactly as written, the PNGs they were judged from
(inlined), the following journal, and the two moulds' ledgers. Run after score.py."""
import json, re, base64, glob, html
from collections import Counter
src = open("data.js").read(); D = json.loads(src[src.index("=") + 1:].rstrip().rstrip(";"))
its = sorted(glob.glob("iterations/*.js"), key=lambda p: int(p.split("/")[1].split("-")[0]))
code = "\n".join(open(p).read() for p in its)
F = open("FOLLOWING.md").read(); R = json.load(open("results.json"))
def md(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(material, encountered|material, recognised R\d+|legibility|error)\*\*",
               lambda m: f'<b class="tag t-{m.group(1).split(",")[0].split()[0]}{"-rec" if "recognised" in m.group(1) else ""}">{m.group(1)}</b>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s, flags=re.S); s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s, flags=re.S)
    out = []
    for blk in s.strip().split("\n\n"):
        if blk.lstrip().startswith("- ") or "\n- " in blk:
            head, *items = re.split(r"\n?- ", blk)
            out.append((f"<p>{head}</p>" if head.strip() else "") + "<ul>" + "".join(f"<li>{' '.join(i.split())}</li>" for i in items) + "</ul>")
        else: out.append(f"<p>{' '.join(blk.split())}</p>")
    return "".join(out)
entries = {}
for e in re.split(r"\n## ", F)[1:]:
    head, body = e.split("\n", 1); entries[int(head.split(" ")[0])] = {"head": html.escape(head), "body": md(body)}
png = {n: "data:image/png;base64," + base64.b64encode(open(f"seen/{n}.png", "rb").read()).decode() for n in entries}
# after the stop: checks of the trained mould against the data (none of these moved the form)
c = Counter
checks = {
 "R1": f"{sum(r[3] == 10 for r in D)} events at exactly 10 km",
 "R2": f"{sum(r[3] == 5 for r in D)} at 5 km, {sum(r[3] == 33 for r in D)} at 33 km, {sum(r[3] == 35 for r in D)} at 35 km",
 "R3": f"{len(set(r[5] for r in D))} magnitude types",
 "R4": "moved the form, iterations 2 to 3",
 "R5": f"{sum(r[6] != 'earthquake' for r in D)} events not earthquakes ({', '.join(f'{k} {v}' for k, v in c(r[6] for r in D if r[6] != 'earthquake').most_common())})",
 "R6": "not checked", "R7": f"{sum(r[4] is not None and r[4] < 0 for r in D)} negative magnitudes",
 "R8": f"{sum(r[3] < 0 for r in D)} negative depths", "R9": "not checked",
 "R10": ", ".join(f"{k} {v}" for k, v in c(r[7] for r in D).most_common()),
 "R11": "not as written; the comb in Northern California bunches at 0.70–0.76 and 1.02–1.09, not at round values"}
P = open("PREDICTIONS.md").read()
R_items = re.findall(r"^- (R\d+) (.+?)(?=\n- R|\n\n)", P, re.M | re.S)
M_line = re.search(r"M1 one mark.*?is\.", P, re.S).group(0)
tpl = open("page.tpl.html").read()
page = (tpl.replace("/*DATA*/", "const D=" + json.dumps(D, separators=(",", ":")) + ";")
        .replace("/*CODE*/", code)
        .replace("/*ENTRIES*/", json.dumps(entries, ensure_ascii=False))
        .replace("/*PNG*/", json.dumps(png))
        .replace("{{HOUSE}}", "".join(f'<li class="{"kept" if v else "lost"}">{html.escape(k)} <span>{"kept" if v else "lost"}</span></li>' for k, v in R["house_features_iteration5"].items()))
        .replace("{{TRAINED}}", "".join(f'<li class="{"moved" if k == "R4" else ""}"><b>{k}</b> {html.escape(" ".join(v.split()))} <span>{html.escape(checks[k])}</span></li>' for k, v in R_items))
        .replace("{{N}}", f"{len(D):,}"))
open("index.html", "w").write(page); print("index.html", len(page))
