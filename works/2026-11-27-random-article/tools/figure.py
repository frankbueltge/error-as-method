"""figure.svg: for each kind, share of the 160 (x) against share of curators' stamps that say unusual (y);
right panel: the same by length band. Usage: figure.py <work dir>"""
import json, os, sys
W = sys.argv[1]
res = json.load(open(os.path.join(W, "results.json")))
K = {"P": "person", "X": "other", "S": "settlement", "D": "navigation page", "W": "creative work", "T": "sport",
     "B": "building or site", "O": "organism", "G": "natural feature"}
items = res["items"]
w, h = 820, 400
L, T, PW, PH = 70, 50, 420, 270
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="Georgia,serif" font-size="12">',
     '<style>text{fill:#1e2124}.m{fill:#5d6468}.ax{stroke:#8a8a8a;stroke-width:1}.g{stroke:#ddd6c8;stroke-width:1}'
     '@media (prefers-color-scheme:dark){text{fill:#e7e3dc}.m{fill:#9aa2a7}.g{stroke:#363d41}}</style>',
     f'<text x="{L}" y="24" font-size="15">What the curators stamped unusual (144 stamps, 12 curators)</text>']
def X(v): return L + v / 0.25 * PW
def Y(v): return T + PH - v * PH
for gy in [0, .25, .5, .75, 1]:
    o.append(f'<line class="g" x1="{L}" x2="{L+PW}" y1="{Y(gy):.1f}" y2="{Y(gy):.1f}"/><text class="m" x="{L-8}" y="{Y(gy)+4:.1f}" text-anchor="end">{int(gy*100)} %</text>')
for gx in [0, .05, .10, .15, .20, .25]:
    o.append(f'<text class="m" x="{X(gx):.1f}" y="{T+PH+16}" text-anchor="middle">{int(gx*100)} %</text>')
o.append(f'<line class="ax" x1="{L}" x2="{L+PW}" y1="{T+PH}" y2="{T+PH}"/><line class="ax" x1="{L}" x2="{L}" y1="{T}" y2="{T+PH}"/>')
o.append(f'<text class="m" x="{L+PW/2}" y="{T+PH+34}" text-anchor="middle">share of the kind among 160 articles drawn by chance</text>')
o.append(f'<text class="m" transform="translate(18,{T+PH/2}) rotate(-90)" text-anchor="middle">stamped unusual</text>')
for k, v in res["by_kind"].items():
    if not v["n"]: continue
    x, y = X(v["pool_share"]), Y(v["unusual"] / v["n"])
    r = 3 + v["n"] ** .5 * 1.3
    fill = "#b2321f" if k == "D" else "#5d6468"
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" fill-opacity=".75"/>')
    if v["unusual"] == 0:
        dy = {"G": 70, "O": 50, "W": 30, "S": 90}.get(k, 30)
        o.append(f'<line class="g" x1="{x:.1f}" x2="{x:.1f}" y1="{y-r:.1f}" y2="{y-dy+4:.1f}"/>')
        o.append(f'<text x="{x+3:.1f}" y="{y-dy:.1f}" font-size="11">{K[k]} 0/{v["n"]}</text>')
    else:
        o.append(f'<text x="{x+r+3:.1f}" y="{y+4:.1f}" font-size="11">{K[k]} {v["unusual"]}/{v["n"]}</text>')
# length panel
L2, PW2 = 560, 220
bands = [("under 100 words", lambda x: x < 100), ("100–299", lambda x: 100 <= x < 300), ("300–999", lambda x: 300 <= x < 1000), ("1,000 or more", lambda x: x >= 1000)]
o.append(f'<text x="{L2}" y="{T-8}" font-size="12">by length of the article</text>')
for i, (name, f) in enumerate(bands):
    s = [x for x in items if f(x["words"])]; u = sum(x["tag"] == "unusual" for x in s)
    y = T + 20 + i * 60; bw = PW2 * u / len(s)
    o.append(f'<text x="{L2}" y="{y}" font-size="11">{name}: {u} of {len(s)}</text>')
    o.append(f'<rect x="{L2}" y="{y+6}" width="{PW2}" height="12" fill="#ddd6c8" fill-opacity=".6"/><rect x="{L2}" y="{y+6}" width="{bw:.1f}" height="12" fill="#b2321f" fill-opacity=".8"/>')
o.append(f'<text class="m" x="{L2}" y="{T+270}" font-size="11">Navigation pages (red, left) are as common</text>')
o.append(f'<text class="m" x="{L2}" y="{T+285}" font-size="11">in the 160 as settlements; one was stamped</text>')
o.append(f'<text class="m" x="{L2}" y="{T+300}" font-size="11">unusual 14 times in 18, the other never.</text>')
o.append("</svg>")
open(os.path.join(W, "figure.svg"), "w").write("\n".join(o))
print("ok")
