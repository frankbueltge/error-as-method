"""figure.py (Session 146): figure.svg, the 28 pages by row and the five verdicts on each as columns:
the practice's 'works', W (no register), WT (register beside it), W1 (only the 18 changed pages), V (truth)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); R = json.load(open(os.path.join(H, "results.json"))); T = R["table"]
true_rows = ["c1", "c2", "c3", "c4"] + [m for m in T if T[m]["pixeldiff"] == 0]
lie_rows = [m for m in T if T[m]["pixeldiff"] > 0]
cols = [("practice", lambda k: T[k]["practice_works"] if k in T else "yes"), ("W", lambda k: T[k]["W"] if k in T else R["family"][k]["W"]),
        ("WT", lambda k: T[k]["WT"] if k in T else R["family"][k]["WT"]), ("W1", lambda k: T[k].get("W1") if k in T else None),
        ("V", lambda k: T[k]["V"] if k in T else R["family"][k]["V"])]
cw, rh, x0, y0 = 70, 17, 60, 84
def cell(x, y, v, truth=False):
    if v is None: return '<text x="%d" y="%d" class="m" text-anchor="middle">·</text>' % (x + cw / 2, y + 12)
    ok = str(v).lower().startswith("y")
    fill = "#2f6a46" if ok else "#a8432b"
    return '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity="%s"/>' % (x + 8, y + 2, cw - 16, rh - 4, fill, "0.9" if ok else "0.85")
rows = [("ten true pages: the family, and six mutants that read neither swapped column", true_rows), ("eighteen pages under swapped columns", lie_rows)]
h = y0 + sum(len(r) * rh + 34 for _, r in rows) + 40; w = max(x0 + cw * len(cols) + 20, 520)
s = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" font-family="Georgia, serif">' % (w, h, w, h),
     '<style>.t{font-size:13px;fill:#1b1916}.m{font-size:11px;fill:#6a645b}.h{font-size:12px;fill:#1b1916}</style>',
     '<rect width="100%%" height="100%%" fill="#f6f3ee"/>',
     '<text x="10" y="22" class="t">Five verdicts on 28 pages. Green: works (V: agrees with the register). Red: does not (V: false).</text>',
     '<text x="10" y="40" class="m">practice: this line, knowing every swap. W: a judge without the register. WT: the register beside it.</text>',
     '<text x="10" y="56" class="m">W1: shown only the eighteen. V: checked against the register.</text>']
for i, (n, _) in enumerate(cols): s.append('<text x="%d" y="%d" class="h" text-anchor="middle">%s</text>' % (x0 + i * cw + cw / 2, y0 - 8, n))
y = y0
for label, ks in rows:
    s.append('<text x="10" y="%d" class="m">%s</text>' % (y + 12, label)); y += 18
    for k in ks:
        s.append('<text x="%d" y="%d" class="m" text-anchor="end">%s</text>' % (x0 - 6, y + 12, k))
        for i, (_, f) in enumerate(cols): s.append(cell(x0 + i * cw, y, f(k)))
        y += rh
    y += 16
s.append('</svg>'); open(os.path.join(H, "figure.svg"), "w").write("\n".join(s)); print("figure.svg", w, h)
