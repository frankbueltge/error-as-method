"""Draw figure.svg: the people's list for each of the 24 cues as one bar, the machine instances'
word inked, and the three tallies. stdlib only.

usage: python3 figure.py
"""
import json
from xml.sax.saxutils import escape

plan = json.load(open("plan.json"))
r = json.load(open("results.json"))
s = r["summary"]
W, X0, BW, RH, TOP = 900, 120, 740, 22, 128
H = TOP + 24 * RH + 52
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
     'font-family="Georgia, serif">',
     f'<rect width="{W}" height="{H}" fill="#f3f0e8"/>',
     '<text x="20" y="34" font-size="20" fill="#1c1a17">Three asked, the same word: people 1.7 of 24 '
     f'(expected), machines {s["S_unanimous"]} of 24</text>',
     '<text x="20" y="58" font-size="13" fill="#6f685d">With the people\'s first word struck: machines '
     f'{s["N_unanimous"]} of 24. Two words at once, which no norm prints: {s["P_unanimous"]} of 24 '
     f'({s["P_unforced_unanimous"]} of the 12 pairs that share no associate).</text>',
     '<text x="20" y="80" font-size="13" fill="#6f685d">Each bar: what about 150 people wrote for one cue, '
     'widest first; pale end, words one person wrote. Dark: the six instances\' most frequent word.</text>',
     f'<text x="20" y="102" font-size="13" fill="#6f685d">It is the people\'s widest on '
     f'{s["S_modal_is_people_top"]} of 24; four times no two people wrote it at all.</text>']
for i, k in enumerate(plan["keys"]["S"]):
    c = r["cells"][k["id"]]
    y = TOP + i * RH
    o.append(f'<text x="{X0 - 8}" y="{y + 15}" font-size="12" text-anchor="end" fill="#1c1a17" '
             f'letter-spacing="1">{k["cue"]}</text>')
    x, found = X0, False
    for j, (w, n) in enumerate(k["people"]):
        bw = BW * n / k["G"]
        mine = w == c["modal"]
        found |= mine
        fill = "#1c1a17" if mine else ("#d9d2c3" if j % 2 == 0 else "#c9c0ae")
        o.append(f'<rect x="{x:.1f}" y="{y + 2}" width="{bw:.1f}" height="{RH - 5}" fill="{fill}" '
                 'stroke="#f3f0e8" stroke-width="0.8"/>')
        if bw > 40:
            o.append(f'<text x="{x + 3:.1f}" y="{y + 14}" font-size="10.5" '
                     f'fill="{"#f3f0e8" if mine else "#6f685d"}">{escape(w.lower())}</text>')
        x += bw
    o.append(f'<rect x="{x:.1f}" y="{y + 2}" width="{X0 + BW - x:.1f}" height="{RH - 5}" fill="#ebe6dc"/>')
    if not found:
        raw = c["raw"][c["norm"].index(c["modal"])].lower()
        o.append(f'<text x="{X0 + BW - 4}" y="{y + 14}" font-size="10.5" text-anchor="end" '
                 f'fill="#9b3b2a">machines: {escape(raw)}, not in the people\'s list</text>')
o.append(f'<text x="20" y="{H - 16}" font-size="11" fill="#6f685d">USF Free Association Norms, '
         'Appendix A (Nelson, McEvoy &amp; Schreiber 1998), 24 cues. Machines: six fresh instances per cue, '
         'no tools. Session 153.</text>')
o.append("</svg>")
open("figure.svg", "w").write("\n".join(o) + "\n")
print("ok")
