"""Session 160: figure.svg. Left: where each of the 210 describer placements fell, as a share of the way from the
family's rating to the people's (diverging phrases, arm P). Right: mean error against the correction factor."""
import json, collections
from pathlib import Path
HERE = Path(__file__).parent
r = json.loads((HERE / "results.json").read_text())
D = [k for k in r["rows"] if k["diverges"]]
c = collections.Counter()
for k in D:
    a, p = k["A_q"][2], k["people_q"][2]
    for v in k["P_p50s"]:
        c[round((v - a) / (p - a), 2)] += 1
mean_s = r["summary"]["HALFWAY_mean_s_P"]
def err(f):
    return sum(abs(k["A_q"][2] + f * (k["P_q"][2] - k["A_q"][2]) - k["people_q"][2]) for k in D) / len(D)
o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 380" font-family="system-ui,sans-serif" font-size="13">',
     '<rect width="900" height="380" fill="#fcfcfb"/>',
     '<text x="30" y="32" font-size="16" font-weight="650" fill="#0b0b0b">Where 210 placements fell</text>',
     '<text x="30" y="52" fill="#52514e">0 = on the machine\'s own rating · 1 = on the 96 people\'s median</text>']
X0, X1, BY, TOP = 60, 420, 320, 80
sx = lambda s: X0 + (s + 1) / 2.2 * (X1 - X0)
mx = max(c.values())
o.append(f'<line x1="{X0}" x2="{X1}" y1="{BY}" y2="{BY}" stroke="#dddbd5"/>')
for s, n in sorted(c.items()):
    h = n / mx * (BY - TOP); col = "#1baf7a" if s >= 0 else "#77756f"
    o.append(f'<rect x="{sx(s)-18:.1f}" y="{BY-h:.1f}" width="36" height="{h:.1f}" fill="{col}"/>')
    o.append(f'<text x="{sx(s):.1f}" y="{BY-h-6:.1f}" text-anchor="middle" fill="#0b0b0b">{n}</text>')
    o.append(f'<text x="{sx(s):.1f}" y="{BY+18}" text-anchor="middle" fill="#77756f">{s:g}</text>')
o.append(f'<line x1="{sx(mean_s):.1f}" x2="{sx(mean_s):.1f}" y1="{TOP-10}" y2="{BY}" stroke="#eb6834" stroke-dasharray="4 4" stroke-width="2"/>')
o.append(f'<text x="{sx(mean_s)+6:.1f}" y="{TOP}" fill="#eb6834">mean {mean_s:.2f}: no one stood here</text>')
o.append(f'<text x="{(X0+X1)/2}" y="{BY+40}" text-anchor="middle" fill="#52514e">share of the way from the machine to the people</text>')
L, R, T, B = 520, 860, 80, 320
ks = [i / 20 for i in range(0, 51)]; es = [err(k) for k in ks]; em = max(es) * 1.05
px = lambda k: L + k / 2.5 * (R - L); py = lambda e: B - e / em * (B - T)
o.append('<text x="500" y="32" font-size="16" font-weight="650" fill="#0b0b0b">Correcting from outside</text>')
o.append('<text x="500" y="52" fill="#52514e">rating + factor × (description − rating), mean points off (35 phrases)</text>')
o.append(f'<line x1="{L}" x2="{R}" y1="{B}" y2="{B}" stroke="#dddbd5"/>')
o.append('<polyline fill="none" stroke="#8a5cd6" stroke-width="2.5" points="' + " ".join(f"{px(k):.1f},{py(e):.1f}" for k, e in zip(ks, es)) + '"/>')
for k, lab in ((0, "own"), (1, "as said"), (2, "doubled")):
    e = err(k)
    o.append(f'<circle cx="{px(k):.1f}" cy="{py(e):.1f}" r="5" fill="#8a5cd6"/>')
    o.append(f'<text x="{px(k):.1f}" y="{py(e)-10:.1f}" text-anchor="middle" fill="#0b0b0b">{e:.2f}</text>')
    o.append(f'<text x="{px(k):.1f}" y="{B+18}" text-anchor="middle" fill="#77756f">{k} · {lab}</text>')
o.append(f'<text x="{(L+R)/2}" y="{B+40}" text-anchor="middle" fill="#52514e">correction factor</text>')
o.append('</svg>')
(HERE / "figure.svg").write_text("\n".join(o) + "\n")
print(dict(c), [round(err(k), 3) for k in (0, 1, 1.5, 2)])
