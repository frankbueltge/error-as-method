"""figure.py -- figure.svg from looks.json and results.json: every look of every maker as a dot (changed
after it, or not), and the blind coder's defect count in each final work."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); J = lambda p: json.load(open(os.path.join(H, p)))
L, R = J("looks.json"), J("results.json"); D = R["P6"]["defects_by_maker"]
order = [m for a in "ROn" for m in sorted(L) if L[m]["arm"] == a.upper()]
W, rowh, top = 760, 30, 96
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {top + rowh * 12 + 70}" font-family="Georgia, serif" font-size="13">',
       f'<rect width="{W}" height="{top + rowh * 12 + 70}" fill="#f3efe7"/>',
       '<text x="20" y="32" font-size="20" fill="#211d18">Who Looks: every look, and what came after it</text>',
       '<text x="20" y="54" fill="#6d655a" font-size="12">One row per maker. Each dot is one look at its own picture: filled = it changed the work after that look; ring = it changed nothing and handed in.</text>',
       '<text x="20" y="72" fill="#6d655a" font-size="12">Right: visible defects a blind coder found in the work handed in.</text>',
       f'<text x="560" y="{top - 8}" fill="#6d655a" font-size="11">defects in the final</text>']
names = {"R": "eye required", "O": "eye offered", "N": "no eye"}
for i, m in enumerate(order):
    y = top + i * rowh + 14; r = L[m]
    out.append(f'<text x="20" y="{y + 4}" fill="#211d18">{m} · {names[r["arm"]]}</text>')
    if r["looks"]:
        for k, ch in enumerate(r["changed_after_look"]):
            x = 190 + k * 34
            out.append(f'<circle cx="{x}" cy="{y}" r="9" fill="{"#a8431f" if ch else "none"}" stroke="{"#a8431f" if ch else "#2d5b4f"}" stroke-width="2.5"/>')
    else:
        out.append(f'<text x="182" y="{y + 4}" fill="#6d655a" font-size="12" font-style="italic">no viewer</text>')
    d = D[m]
    out.append(f'<rect x="560" y="{y - 8}" width="{max(d * 30, 2)}" height="16" fill="#6d655a"/>')
    out.append(f'<text x="{566 + max(d * 30, 2)}" y="{y + 4}" fill="#211d18" font-size="12">{d}</text>')
    if i in (3, 7):
        out.append(f'<line x1="20" x2="{W - 20}" y1="{y + 15}" y2="{y + 15}" stroke="#d5cdbf"/>')
yb = top + rowh * 12 + 26
out.append(f'<text x="20" y="{yb}" fill="#211d18" font-size="12">Mean defects: with an eye {R["P6"]["mean_O_R"]:.2f} (offered {R["P6"]["mean_O"]:.2f}, required {R["P6"]["mean_R"]:.2f}); without {R["P6"]["mean_N"]:.2f}. Median looks {R["P3"]["median"]:.0f}.</text>')
out.append(f'<text x="20" y="{yb + 20}" fill="#6d655a" font-size="11">Wikidata meteorites with a mass (568, CC0). Ulysses (the nightly line), Session 117, 2026-10-08.</text>')
out.append('</svg>')
open(os.path.join(H, "figure.svg"), "w").write("\n".join(out))
