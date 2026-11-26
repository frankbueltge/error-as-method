"""figure.svg: how far each eight's endings sit from the sixty's mix, against 100,000 random eights.

usage: python figure.py <work dir>
"""
import json, os, random, sys
from collections import Counter

E = ["resignation", "time", "checkmate", "draw"]

def main(wd):
    pool = json.load(open(os.path.join(wd, "people/drawn-400.json")))[:60]
    res = json.load(open(os.path.join(wd, "results.json")))
    sh = {e: 8 * sum(g["ending"] == e for g in pool) / 60 for e in E}
    def dev(p): return round(sum(abs(sum(pool[n - 1]["ending"] == e for n in p) - sh[e]) for e in E), 2)
    rng = random.Random(1882)
    c = Counter(dev(rng.sample(range(1, 61), 8)) for _ in range(100000))
    xs = sorted(c)
    W, H, L, B = 760, 360, 60, 290
    xmax = max(max(xs), 7.5)
    def X(v): return L + (W - L - 30) * v / xmax
    ymax = max(c.values())
    def Y(v): return B - 170 * v / ymax
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Georgia,serif" font-size="12">',
         '<rect width="100%" height="100%" fill="#f1eee8"/>',
         f'<text x="{L}" y="24" font-size="15" fill="#1f2326">How close each eight sits to the sixty\'s mix of endings</text>',
         f'<text x="{L}" y="42" fill="#5f676c">grey bars: 100,000 random eights from the sixty · dots: the eighteen selectors\' final eights, with how many sit at each value</text>']
    for v in xs:
        s.append(f'<rect x="{X(v) - 4:.1f}" y="{Y(c[v]):.1f}" width="8" height="{B - Y(c[v]):.1f}" fill="#bdb6a8"/>')
    s.append(f'<line x1="{L}" y1="{B}" x2="{W - 20}" y2="{B}" stroke="#5f676c"/>')
    for t in range(0, 8):
        s.append(f'<text x="{X(t):.1f}" y="{B + 16}" text-anchor="middle" fill="#5f676c">{t}</text>')
    s.append(f'<text x="{L}" y="{B + 34}" fill="#5f676c">games away from eight times the sixty\'s shares (resignation, time, mate, draw); 1.2 is the closest possible</text>')
    col = {"A": "#a8432a", "B": "#4f7a3a", "C": "#6a4c8a"}
    lab = {"A": "A · as it is", "B": "B · told the counts", "C": "C · most worth showing"}
    for i, a in enumerate("ABC"):
        y = 70 + i * 18
        ds = sorted(res["selectors"][s_]["ending_dev"] for s_ in res["selectors"] if s_[0] == a)
        for d, k in sorted(Counter(ds).items()):
            s.append(f'<circle cx="{X(d):.1f}" cy="{y}" r="5" fill="{col[a]}"/>')
            s.append(f'<text x="{X(d) + 8:.1f}" y="{y + 4}" fill="{col[a]}">{k}</text>')
        s.append(f'<text x="{W - 24}" y="{y + 4}" text-anchor="end" fill="{col[a]}">{lab[a]}</text>')
    s.append(f'<text x="{L}" y="{H - 8}" fill="#5f676c">Lichess open database, 1 Oct 2026, 60 games drawn by seed 188. Experiment 62, Session 188.</text>')
    s.append('</svg>')
    open(os.path.join(wd, "figure.svg"), "w").write("\n".join(s))

if __name__ == "__main__":
    main(sys.argv[1])
