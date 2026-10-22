"""figure.svg: the four cells of experiment 35, and the four chips whose twins lost the crowd's name."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(HERE, "results.json")))
C = r["cells"]
W, H = 760, 420
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Georgia, serif">',
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
       '<text x="24" y="34" font-size="18" fill="#1d1d1b">Twin Chips: how often a maker gave the crowd\'s own name</text>']
bars = [("numbers, exact point", "N_on"), ("numbers, invisible twin", "N_off"), ("picture, exact point", "S_on"), ("picture, twin", "S_off")]
for i, (lab, k) in enumerate(bars):
    y = 64 + i * 34
    v = C[k]["exact_pct"]
    out.append(f'<text x="24" y="{y + 15}" font-size="13" fill="#1d1d1b">{lab}</text>')
    out.append(f'<rect x="210" y="{y + 2}" width="{v * 12:.1f}" height="18" fill="#1d1d1b"/>')
    out.append(f'<text x="{216 + v * 12:.1f}" y="{y + 15}" font-size="13" fill="#1d1d1b">{v}% ({C[k]["exact"]} of {C[k]["n"]})</text>')
loss = sorted(r["per_chip"], key=lambda c: c["N_on_exact"] - c["N_off_exact"], reverse=True)[:4]
for i, c in enumerate(loss):
    x = 24 + i * 184
    y = 220
    out.append(f'<rect x="{x}" y="{y}" width="80" height="80" fill="{c["on"]}"/>')
    out.append(f'<rect x="{x + 84}" y="{y}" width="80" height="80" fill="{c["off"]}"/>')
    out.append(f'<text x="{x}" y="{y + 100}" font-size="12" fill="#1d1d1b">crowd: {c["crowd_name"]}</text>')
    out.append(f'<text x="{x}" y="{y + 118}" font-size="11" fill="#1d1d1b">exact: {c["N_on_exact"]} of 3 · twin: {c["N_off_exact"]} of 3</text>')
    out.append(f'<text x="{x}" y="{y + 136}" font-size="11" fill="#6b6a66">twin read as: {c["N_off"][0]}</text>')
out.append('<text x="24" y="404" font-size="11" fill="#6b6a66">Six number-readers, six lookers, 24 chips each; crowd names from the xkcd colour survey (CC0). Experiment 35, Session 151.</text>')
out.append('</svg>')
open(os.path.join(HERE, "figure.svg"), "w").write("\n".join(out))
