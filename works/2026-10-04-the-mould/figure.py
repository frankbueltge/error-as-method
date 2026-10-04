"""figure.svg: the ten changes between the six forms, one block per change, coloured by the cause
recorded at the time (from results.json)."""
import json, html
R = json.load(open("results.json"))
titles = ["the mould", "by magnitude, by network", "one row per network", "the floor, as a map", "named by busiest (dropped)", "named by region"]
col = {"material, encountered": "#3b6e8f", "legibility": "#6b8f3b", "error": "#c8553d"}
W, H, x0, cw = 900, 330, 40, 140
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia,serif">', f'<rect width="{W}" height="{H}" fill="#f4f1ea"/>',
     '<text x="40" y="34" font-size="19" fill="#1d1b18">The Mould: ten changes between six forms, by the cause recorded at the time</text>']
for i, t in enumerate(titles):
    x = x0 + i * cw
    o.append(f'<circle cx="{x+8}" cy="70" r="7" fill="{"#f4f1ea" if i == 4 else "#1d1b18"}" stroke="#1d1b18" stroke-width="1.5"/>')
    o.append(f'<text x="{x}" y="98" font-size="12" fill="#1d1b18">{i}</text><text x="{x+14}" y="98" font-size="11" fill="#6f6a60">{html.escape(t)}</text>')
    if i < 5: o.append(f'<line x1="{x+18}" y1="70" x2="{x+cw-2}" y2="70" stroke="#1d1b18" stroke-width="1"/>')
    for k, c in enumerate([c for c in R["changes"] if c["after_iteration"] == i]):
        tag = c["tag"]; fill = "#c9a66b" if "recognised" in tag else col[tag]
        o.append(f'<rect x="{x+20}" y="{118+k*36}" width="{cw-30}" height="28" fill="{fill}"/>')
        o.append(f'<text x="{x+26}" y="{136+k*36}" font-size="11" font-family="monospace" fill="{"#1d1b18" if "recognised" in tag else "#fff"}">{html.escape(tag.replace("material, ", ""))}</text>')
leg = [("material, encountered (not a prior belief)", "#3b6e8f"), ("material, recognised (prior R4)", "#c9a66b"), ("legibility", "#6b8f3b"), ("error (mine)", "#c8553d")]
for k, (t, c) in enumerate(leg):
    o.append(f'<rect x="{[40,330,580,700][k]}" y="262" width="12" height="12" fill="{c}"/><text x="{[58,348,598,718][k]}" y="273" font-size="12" fill="#1d1b18">{html.escape(t)}</text>')
o.append(f'<text x="40" y="306" font-size="12" fill="#6f6a60">Material moved the form 5 times of 10: twice by encounter, three times by recognition. The decisive turn, to a map, was recognition.</text>')
o.append('<text x="40" y="322" font-size="12" fill="#6f6a60">Data: USGS ComCat, 10,870 events, 3 Sep to 3 Oct 2026. Form 4 was abandoned.</text></svg>')
open("figure.svg", "w").write("\n".join(o)); print("figure.svg")
