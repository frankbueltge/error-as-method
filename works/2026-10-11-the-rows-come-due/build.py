#!/usr/bin/env python3
"""Build index.html and figure.svg from the committed JSON. Stdlib, no network."""
import json, os, html
H = os.path.dirname(os.path.abspath(__file__))
J = lambda p: json.load(open(os.path.join(H, p), encoding="utf-8"))
me = J("census.json")["rows"]; A = J("readers/reader-A.json"); B = J("readers/reader-B.json")
splits = J("splits.json"); uses = J("uses.json")["uses"]
up = {r["id"]: r for r in J("uses-practice.json")["codes"]}; ur = {r["id"]: r for r in J("readers/reader-uses.json")}
entries = [{"id": m["id"], "me": {"h": m["held"], "j": m["judged"], "w": m["wrong"]},
            "A": {"h": a["held"], "j": a["judged"], "w": a["wrong"]},
            "B": {"h": b["held"], "j": b["judged"], "w": b["wrong"]},
            "split": [k for k in "AB" if splits[k].get(m["id"], {}).get("split")],
            "why": {k: splits[k][m["id"]]["why"] for k in "AB" if m["id"] in splits[k]}}
           for m, a, b in zip(me, A, B)]
U = [{"id": u["id"], "s": u["session"], "f": u["file"], "l": u["line"], "c": u["context"],
      "p": up[u["id"]]["code"], "r": ur[u["id"]]["code"], "rw": ur[u["id"]]["why"],
      "pn": up[u["id"]].get("note", "")} for u in uses]
data = json.dumps({"entries": entries, "uses": U}, ensure_ascii=False).replace("</", "<\\/")
page = open(os.path.join(H, "page.tpl.html"), encoding="utf-8").read().replace("/*DATA*/null", data)
open(os.path.join(H, "index.html"), "w", encoding="utf-8").write(page)

# figure: two bands. Top: 21 entries x 3 coders, cell = which side is wrong. Bottom: 109 uses, practice vs reader.
col = {"R": "#c0392b", "J": "#2c6e9e", "B": "#8e44ad", "X": "#9a9a9a",
       "N": "#2c6e9e", "T": "#c0392b", "C": "#d4a017", "O": "#cfcfcf"}
W, cw = 760, 30
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 330" font-family="Helvetica,Arial,sans-serif" font-size="11">',
     f'<rect width="{W}" height="330" fill="#fbfaf7"/>',
     '<text x="20" y="22" font-size="14" font-weight="bold">The rows come due — Session 120</text>',
     '<text x="20" y="40" fill="#444">F-193 to F-213: which term each coder says is wrong (red = held, blue = judged, violet = both, grey = neither). Ringed: a side-split.</text>']
for k, (lab, key) in enumerate([("practice", "me"), ("reader A", "A"), ("reader B", "B")]):
    y = 56 + k * 34
    s.append(f'<text x="20" y="{y+19}">{lab}</text>')
    for i, e in enumerate(entries):
        x = 90 + i * cw; w = e[key]["w"]
        ring = key in e["split"] or (key == "me" and e["split"])
        s.append(f'<rect x="{x}" y="{y}" width="{cw-4}" height="26" fill="{col[w]}"' + (' stroke="#000" stroke-width="2.5"' if ring else '') + '/>')
        s.append(f'<text x="{x+13}" y="{y+17}" text-anchor="middle" fill="#fff">{w}</text>')
for i, e in enumerate(entries):
    s.append(f'<text x="{90+i*cw+13}" y="168" text-anchor="middle" font-size="8" fill="#555">{e["id"][2:]}</text>')
s.append('<text x="20" y="200" fill="#444">The 109 uses of “error” in the journals of Sessions 100–119: practice (upper) and fresh reader (lower).</text>')
s.append('<text x="20" y="214" fill="#444">Red = T, an error named against a value nobody holds; blue = N, against a held reference; amber = concept; light = register, name, other.</text>')
for i, u in enumerate(U):
    x = 20 + i * 6.7
    for j, key in enumerate(["p", "r"]):
        c = u[key]; c2 = "#e8e8e8" if c == "R" else col[c]
        s.append(f'<rect x="{x:.1f}" y="{226+j*30}" width="5.6" height="26" fill="{c2}"/>')
s.append('<text x="20" y="306" fill="#222">Practice: 0 T. Reader: 2 T (U084, U106) — both passages leave the reference’s holder unnamed. Reader B split 2 of 3 disagreements: S113.SIDE fires.</text>')
s.append('</svg>')
open(os.path.join(H, "figure.svg"), "w").write("\n".join(s))
print("built")
