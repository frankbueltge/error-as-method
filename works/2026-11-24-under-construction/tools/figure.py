"""figure.svg: per sign, the people's count in 100, the makers' median guess, and the share of the makers' pages carrying it."""
import json
r = json.load(open("results.json")); P5 = r["predictions"]["P5"]; mk = r["makers"]
signs = [("under_construction", "Under Construction"), ("marquee", "marquee"), ("blink", "blink"), ("music", "music"),
         ("counter", "hit counter"), ("guestbook", "guestbook"), ("webring", "webring"), ("welcome_to_my", "“Welcome to my”")]
def carry(arm, k): return 100 * sum(v["final"]["iconic"][k] for m, v in mk.items() if m[0] == arm) / 6
W, row, top, left, sc = 760, 46, 72, 150, 4.5
H = top + row * len(signs) + 40
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia,serif" font-size="13">',
     f'<rect width="{W}" height="{H}" fill="#f6f4ee"/>',
     '<text x="16" y="26" font-size="17" font-weight="bold" fill="#1d1d1b">An ordinary person’s GeoCities page: what makers guessed, what they made</text>',
     '<text x="16" y="44" fill="#6b6a63" font-size="12">per hundred · grey: 100 real pages, 1996–2000 · light: makers’ median guess · dark: share of makers’ own pages</text>','<text x="16" y="58" fill="#6b6a63" font-size="12">P: six makers from words alone · S: six makers after reading twenty real pages</text>']
for i, (k, lab) in enumerate(signs):
    y = top + i * row
    s.append(f'<text x="16" y="{y+22}" fill="#1d1d1b">{lab}</text>')
    bars = [(r["people"]["rates"][k], "#6b6a63", "people"), (P5["P_median_estimates"][k], "#e0a27e", "P guess"),
            (carry("P", k), "#d4380d", "P pages"), (P5["S_median_estimates"][k], "#e9c4ad", "S guess"), (carry("S", k), "#f08c5a", "S pages")]
    for j, (v, c, n) in enumerate(bars):
        yy = y + 2 + j * 8
        s.append(f'<rect x="{left}" y="{yy}" width="{v*sc:.1f}" height="6" fill="{c}"/>')
    s.append(f'<text x="{left + 100*sc + 10:.1f}" y="{y+22}" fill="#6b6a63" font-size="11">{r["people"]["rates"][k]} · {P5["P_median_estimates"][k]:g} · {carry("P",k):.0f} · {P5["S_median_estimates"][k]:g} · {carry("S",k):.0f}</text>')
s.append(f'<text x="16" y="{H-14}" fill="#6b6a63" font-size="11">Numbers: people · P guess · P pages · S guess · S pages. Source: Geocities Gallery, seed 186; tools/features.py.</text>')
s.append('</svg>')
open("figure.svg", "w").write("\n".join(s)); print("ok")
