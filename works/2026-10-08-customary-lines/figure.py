"""figure.py -- figure.svg: the eighteen works as cells in four rows (R, D, B, C), coloured by the blind
coder's group, with the coder's 0-3 rating. Round 1 is one group by the coder's own sorting of r1-r6."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
res = json.load(open(os.path.join(HERE, "results.json")))
COL = {"lunation grid of phase discs": "#2f5f8a", "lunation spiral (moon clock)": "#c07a1a",
       "core sample strata": "#2d6b47", "silhouette landscape profile": "#8a2f5a"}
ROWS = [("R", "round 1, plain"), ("D", "told nothing more"), ("B", "shown the six"), ("C", "shown, told: none of them")]
W, H, cw, ch, x0, y0 = 830, 390, 98, 56, 200, 50
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Georgia,serif">',
     f'<rect width="{W}" height="{H}" fill="#f2efe8"/>',
     '<text x="20" y="28" font-size="17" fill="#1d1b18">Customary Lines: eighteen makers, one brief, one year of readers of "Moon"</text>']
for i, (a, label) in enumerate(ROWS):
    y = y0 + i * (ch + 14)
    s.append(f'<text x="20" y="{y + 24}" font-size="14" fill="#1d1b18">{a}</text>')
    s.append(f'<text x="40" y="{y + 24}" font-size="12" fill="#6a645a">{label}</text>')
    ms = sorted(m for m, r in res["rows"].items() if r["arm"] == a)
    for j, m in enumerate(ms):
        r = res["rows"][m]; x = x0 + j * (cw + 6)
        g = "lunation grid of phase discs" if a == "R" else r["M3_group"]
        fill = COL.get(g, "#d5cec0"); tc = "#ffffff" if g in COL else "#1d1b18"
        s.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{fill}" rx="2"/>')
        s.append(f'<text x="{x + 6}" y="{y + 16}" font-size="11" fill="{tc}">{m}</text>')
        if a != "R":
            s.append(f'<text x="{x + cw - 8}" y="{y + ch - 10}" font-size="18" text-anchor="end" fill="{tc}">{r["M2_rating"]}</text>')
        t = r["title"] if len(r["title"]) <= 16 else r["title"][:15] + "…"
        s.append(f'<text x="{x + 6}" y="{y + 31}" font-size="10" font-style="italic" fill="{tc}">{t.replace("&", "&amp;")}</text>')
ky = H - 42
for k, (g, c) in enumerate(list(COL.items()) + [("alone", "#d5cec0")]):
    x = 20 + k * 160
    s.append(f'<rect x="{x}" y="{ky}" width="14" height="10" fill="{c}"/><text x="{x + 20}" y="{ky + 9}" font-size="11" fill="#6a645a">{g.split(" (")[0]}</text>')
s.append(f'<text x="20" y="{H - 6}" font-size="10" fill="#6a645a">Colour: blind coder\'s group (pictures only). Number: "could this be one more of round 1?" 0-3. Round 1 sorted by the same coder into one group.</text>')
s.append('</svg>')
open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(s))
print("figure.svg written")
