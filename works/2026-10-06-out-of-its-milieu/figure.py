"""figure.svg: the sixteen claims, by instrument; ring = the practice's blind tag, fill = the check."""
import json
R = json.load(open("results.json"))
G, Hc, INK, MUTE = "#2f4a5e", "#9c2f22", "#1d1b18", "#6f685d"
rows = [("ear", "the ear (made for six bells)"), ("mould", "the mould (made for earthquakes)"), ("grid24", "grid24 (made for the length of day)")]
W, H = 760, 300
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Georgia, serif">',
     f'<rect width="{W}" height="{H}" fill="#f3efe7"/>',
     f'<text x="20" y="30" font-size="17" fill="{INK}">Out of Its Milieu: sixteen claims, guessed before the check</text>',
     f'<text x="20" y="50" font-size="12" fill="{MUTE}">ring: what the practice guessed · fill: what the check found · blue grid, red instrument · ✕ ring and fill disagree</text>']
for j, (k, lab) in enumerate(rows):
    y = 95 + j * 62
    s.append(f'<text x="20" y="{y + 5}" font-size="13" fill="{INK}">{lab}</text>')
    for i, c in enumerate([c for c in R["claims"] if c["instrument"] == k]):
        x = 290 + i * 56
        s.append(f'<circle cx="{x}" cy="{y}" r="17" fill="{G if c["verdict"] == "G" else Hc}" stroke="{G if c["blind"] == "G" else Hc}" stroke-width="5" stroke-opacity="0.45"/>')
        s.append(f'<text x="{x}" y="{y + 4}" font-size="11" fill="#fff" text-anchor="middle" font-family="monospace">{c["id"]}</text>')
        if not c["match"]: s.append(f'<text x="{x + 15}" y="{y - 14}" font-size="12" fill="{INK}">✕</text>')
s.append(f'<text x="20" y="{H - 34}" font-size="12" fill="{MUTE}">11 of 16 agree. All 6 claims guessed "instrument" were. The 5 misses were guessed "grid": the grid has each feature,</text>')
s.append(f'<text x="20" y="{H - 16}" font-size="12" fill="{MUTE}">smaller than claimed, or under a check that measured the wrong band. GB system frequency, August 2026, NESO.</text>')
s.append("</svg>")
open("figure.svg", "w").write("\n".join(s)); print("figure.svg")
