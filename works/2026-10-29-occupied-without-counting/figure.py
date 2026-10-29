"""Session 161: figure.svg. Top: arm F's 192 stated medians on the 0-100 line, stacked; the people's seven steps as
dashed marks. Bottom: the 32 people's medians on the same line. Reads face-data.js's source files via results.json."""
import json
from pathlib import Path
HERE = Path(__file__).parent
d = json.loads((HERE / "face-data.js").read_text().split("=", 1)[1].rstrip().rstrip(";"))
W, L, R, base = 760, 40, 720, 190
x = lambda v: L + (R - L) * v / 100
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 362" width="{W}" height="362" font-family="system-ui, sans-serif" font-size="12">',
       '<rect width="100%" height="100%" fill="#fcfcfb"/>',
       f'<text x="{L}" y="24" font-size="14" font-weight="600" fill="#0b0b0b">Six instances, asked for the people\'s median on a line from 0 to 100: 192 answers</text>']
for i in range(7):
    xi = x(100 * i / 6)
    out.append(f'<line x1="{xi:.1f}" x2="{xi:.1f}" y1="36" y2="{base+4}" stroke="#c9c6bd" stroke-dasharray="2 3"/>')
    out.append(f'<text x="{xi:.1f}" y="{base+20}" text-anchor="middle" fill="#77756f">{i+1}</text>')
out.append(f'<line x1="{L}" x2="{R}" y1="{base+4}" y2="{base+4}" stroke="#77756f"/>')
bins, tot = {}, {}
F = sorted(v for r in d["rows"] for v in r["F"])
for v in F: tot[round(v)] = tot.get(round(v), 0) + 1
step = min(5.0, (base - 44) / max(tot.values()))
for v in F:
    b = round(v); bins[b] = bins.get(b, 0) + 1
    out.append(f'<circle cx="{x(v):.1f}" cy="{base - 3 - (bins[b]-1)*step:.1f}" r="3" fill="none" stroke="#1baf7a" stroke-width="1.1"/>')
out.append(f'<text x="{L}" y="{base+44}" font-size="13" font-weight="600" fill="#0b0b0b">The 32 sentences\' medians among the 16 to 35 people who rated each</text>')
pb = {}
for r in d["rows"]:
    v = (r["pmed"] - 1) * 100 / 6; b = round(v); pb[b] = pb.get(b, 0) + 1
    out.append(f'<rect x="{x(v)-3.5:.1f}" y="{base+56+(pb[b]-1)*5.5:.1f}" width="7" height="4.5" fill="#eb6834"/>')
out.append(f'<text x="{L}" y="354" fill="#52514e">{round(d["onstep"]*100)} % of the instances\' answers lie within 2 points of a step (dashed); {round(d["mult5"]*100)} % are multiples of 5.</text>')
out.append('</svg>')
(HERE / "figure.svg").write_text("\n".join(out) + "\n")
