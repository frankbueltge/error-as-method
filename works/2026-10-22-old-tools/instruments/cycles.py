"""CYCLES, an instrument. Looks for regular recurrence in one column of values that stand at even steps.

usage: python3 instrument.py data.csv --column VALUE [--step "1 day"]
It removes the straight-line trend, then measures how strongly every period from 2 steps to half the
record recurs (a periodogram, Hann-windowed). Records longer than 4096 values are first averaged in
equal blocks down to at most 4096, and the block size is reported. Writes reading.svg (power against
period) and reading.json (the three strongest periods, in steps of the record) into the current folder.
It assumes the values are evenly spaced and in order; it does not check this."""
import argparse, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read, num, svg, write, esc
a = argparse.ArgumentParser(); a.add_argument("csv"); a.add_argument("--column", required=True)
a.add_argument("--step", default="step"); a = a.parse_args()
raw = read(a.csv, a.column); x = [t for t in (num(s) for s in raw) if t is not None]
block = max(1, math.ceil(len(x) / 4096))
if block > 1: x = [sum(x[i:i + block]) / len(x[i:i + block]) for i in range(0, len(x) - block + 1, block)]
n = len(x)
if n < 16: sys.exit("fewer than 16 values")
mt = (n - 1) / 2; mx = sum(x) / n
b = sum((i - mt) * (x[i] - mx) for i in range(n)) / sum((i - mt) ** 2 for i in range(n))
y = [(x[i] - mx - b * (i - mt)) * (0.5 - 0.5 * math.cos(2 * math.pi * i / (n - 1))) for i in range(n)]
P = []
for k in range(1, n // 2 + 1):
    w = 2 * math.pi * k / n; c = s = 0.0
    for i in range(n): c += y[i] * math.cos(w * i); s += y[i] * math.sin(w * i)
    P.append((n / k, c * c + s * s))
tot = sum(p for _, p in P) or 1
peaks = [(P[i][0], P[i][1] / tot) for i in range(len(P)) if (i == 0 or P[i][1] >= P[i-1][1]) and (i == len(P)-1 or P[i][1] >= P[i+1][1])]
peaks.sort(key=lambda t: -t[1]); top = peaks[:3]
pmax = max(p for _, p in P) or 1; lmin, lmax = math.log(2), math.log(n)
X = lambda per: 60 + 880 * (math.log(per) - lmin) / (lmax - lmin)
pts = " ".join("%.1f,%.1f" % (X(per), 500 - 400 * p / pmax) for per, p in sorted(P))
body = '<polyline fill="none" stroke="#1b1b1b" stroke-width="1" points="%s"/>' % pts
for j, (per, f) in enumerate(top):
    body += ('<line x1="%.1f" x2="%.1f" y1="96" y2="500" stroke="#a33" stroke-dasharray="3 3"/>'
             '<text x="%.1f" y="%d" font-size="13" fill="#a33">%s</text>') % (X(per), X(per), X(per) + 4, 110 + 16 * j,
             esc("%.4g × %d %s (%.0f%% of power)" % (per, block, a.step, 100 * f)))
body += ('<text x="60" y="530" font-size="13" fill="#555">period: 2 steps</text>'
         '<text x="940" y="530" font-size="13" fill="#555" text-anchor="end">%d steps (whole record)</text>' % n)
write("CYCLES", svg("CYCLES · " + a.column, "%d values%s; trend removed; the three strongest periods marked" %
      (n, (" (blocks of %d)" % block) if block > 1 else ""), body),
      {"column": a.column, "n": n, "block": block, "step": a.step,
       "strongest": [{"period_steps": per * block, "share_of_power": round(f, 4)} for per, f in top]})
