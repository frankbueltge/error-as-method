"""Session 163, experiment 43 (Unheard): figure.svg, written by hand as SVG (no plotting library).
Left: the machine's own ratings and its account of the people against the decibel figure.
Right: the people. Run: python3 figure.py"""
import json, statistics as st
from pathlib import Path
HERE = Path(__file__).parent
R = [l for l in (HERE / "face-data.js").read_text().split("=", 1)[1].rstrip(";\n").splitlines()]
rows = json.loads("".join(R))
W, H = 900, 380
def panel(ox, title, layers):
    L, T, PW, PH = ox + 46, 40, 380, 280
    x = lambda v: L + (v - 35) / 45 * PW
    y = lambda v: T + (10 - v) / 10 * PH
    s = [f'<text x="{L}" y="24" font-size="14" font-weight="600" fill="#0b0b0b">{title}</text>']
    for v in range(0, 11, 2):
        s.append(f'<line x1="{L}" x2="{L+PW}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#e6e4de"/>'
                 f'<text x="{L-8}" y="{y(v)+4:.1f}" text-anchor="end" font-size="11" fill="#77756f">{v}</text>')
    for v in range(40, 81, 10):
        s.append(f'<text x="{x(v):.1f}" y="{T+PH+16}" text-anchor="middle" font-size="11" fill="#77756f">{v} dB</text>')
    for kind, colour in layers:
        for r in rows:
            v = {"fam": r["fam"], "desc": st.median(r["D"]), "ppl": r["people"]}[kind]
            cx, cy = x(r["Lmax"]), y(v)
            if kind == "fam":
                s.append(f'<rect x="{cx-4:.1f}" y="{cy-4:.1f}" width="8" height="8" fill="{colour}" transform="rotate(45 {cx:.1f} {cy:.1f})"/>')
            elif kind == "desc":
                s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="none" stroke="{colour}" stroke-width="1.8"/>')
            else:
                fill = colour if r["src"] == "small drone" else "none"
                s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="{fill}" stroke="{colour}" stroke-width="1.6"/>')
    return "\n".join(s)
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="system-ui, sans-serif">',
       f'<rect width="{W}" height="{H}" fill="#fcfcfb"/>',
       panel(0, "The machine, and its account of 36 listeners", [("fam", "#2a78d6"), ("desc", "#1baf7a")]),
       panel(450, "The 36 listeners (filled: small drones)", [("ppl", "#eb6834")]),
       f'<text x="20" y="{H-12}" font-size="11" fill="#52514e">Annoyance 0–10 against maximum level, 65 sounds; medians of six instances. Data: Kawai et al., Zenodo 22045972, CC BY 4.0.</text>',
       '</svg>']
(HERE / "figure.svg").write_text("\n".join(svg) + "\n")
print("figure.svg written")
