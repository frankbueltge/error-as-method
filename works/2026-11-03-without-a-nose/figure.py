"""Session 168: figure.svg. Experiments 45, 46, 47: what the items were, how wide the family's own order was (SD of its
medians as a share of the scale's range, from each results.json), and how many of six shuffled-contact makers named the misfit
(experiment 45: 4, journal 2026-10-31; 46: 0, journal 2026-11-01; 47: 6, tonight). Run: python3 figure.py"""
import json
from pathlib import Path
H = Path(__file__).parent
rows = [("45 Paired", "pictures", "kawaii, 1-9", json.load(open(H / "../2026-10-31-paired/results.json"))["family_median_sd"], 8, 4),
        ("46 Clean Hands", "names", "disease risk, 1-7", json.load(open(H / "../2026-11-01-clean-hands/results.json"))["family_median_sd"], 6, 0),
        ("47 Without a Nose", "names", "smell, 1-9", json.load(open(H / "results.json"))["family_median_sd"], 8, 6)]
W, rowh, top = 640, 92, 70
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {top+rowh*3+40}" font-family="Georgia,serif" font-size="13">',
     f'<rect width="{W}" height="{top+rowh*3+40}" fill="#f6f3ec"/>',
     '<text x="20" y="28" font-size="17" fill="#1f1d1a">Who names a lie about a public: the eye, or the order already held?</text>',
     '<text x="20" y="50" fill="#6b665d">bar: spread of the family\'s own ratings · squares: shuffled-contact makers who named the misfit</text>']
for i, (name, perc, dom, sd, rng, named) in enumerate(rows):
    y = top + i * rowh + 20
    s.append(f'<text x="20" y="{y}" fill="#1f1d1a">{name}</text>')
    s.append(f'<text x="20" y="{y+18}" fill="#6b665d" font-size="12">{perc} · {dom}</text>')
    frac = sd / rng; bw = 180 * frac / 0.35
    s.append(f'<rect x="200" y="{y-12}" width="180" height="14" fill="none" stroke="#d8d2c4"/>')
    s.append(f'<rect x="200" y="{y-12}" width="{bw:.1f}" height="14" fill="#2c4a7a"/>')
    s.append(f'<text x="200" y="{y+20}" fill="#6b665d" font-size="11" font-family="monospace">SD {sd:.2f} on {rng} steps</text>')
    for k in range(6):
        fill = "#a3392b" if k < named else "none"
        s.append(f'<rect x="{420+k*30}" y="{y-14}" width="22" height="22" fill="{fill}" stroke="#a3392b"/>')
    s.append(f'<text x="420" y="{y+26}" fill="#6b665d" font-size="11" font-family="monospace">{named} of 6</text>')
s.append(f'<text x="20" y="{top+rowh*3+24}" fill="#6b665d" font-size="11">Names were enough where the family held a wide order (47). Still empty: pictures with a flat order.</text>')
s.append('</svg>')
(H / "figure.svg").write_text("\n".join(s))
