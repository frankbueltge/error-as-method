"""FIRST DIGITS, an instrument. Counts the first significant digit of every number in one column and
sets the counts beside Benford's law, which expects a first digit d with frequency log10(1 + 1/d).

usage: python3 instrument.py data.csv --column VALUE
Zeros, empty and non-numeric cells are skipped and counted; signs are ignored. Writes reading.svg
(observed share of each digit as bars, Benford's expected share as dots) and reading.json (counts,
shares, the mean absolute deviation from Benford, and the chi-square statistic with 8 degrees of freedom)."""
import argparse, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read, num, svg, write, esc
a = argparse.ArgumentParser(); a.add_argument("csv"); a.add_argument("--column", required=True); a = a.parse_args()
raw = read(a.csv, a.column); c = [0] * 10
for s in raw:
    v = num(s)
    if v is None or v == 0: continue
    v = abs(v); c[int(v / 10 ** math.floor(math.log10(v)) + 1e-9) % 10 or 1] += 1
n = sum(c)
if n < 10: sys.exit("fewer than 10 non-zero numbers")
exp = [0] + [math.log10(1 + 1 / d) for d in range(1, 10)]; obs = [0] + [c[d] / n for d in range(1, 10)]
mad = sum(abs(obs[d] - exp[d]) for d in range(1, 10)) / 9; chi = sum((c[d] - n * exp[d]) ** 2 / (n * exp[d]) for d in range(1, 10))
body = ""
for d in range(1, 10):
    x = 40 + (d - 1) * 102
    body += '<rect x="%d" y="%.1f" width="70" height="%.1f" fill="#1b1b1b"/>' % (x, 500 - 900 * obs[d], 900 * obs[d])
    body += '<circle cx="%d" cy="%.1f" r="6" fill="#a33"/>' % (x + 35, 500 - 900 * exp[d])
    body += '<text x="%d" y="524" font-size="15" text-anchor="middle">%d</text>' % (x + 35, d)
body += '<text x="960" y="110" font-size="13" fill="#a33" text-anchor="end">dots: Benford · bars: this column</text>'
write("FIRST DIGITS", svg("FIRST DIGITS · " + a.column, "%d numbers; mean absolute deviation from Benford %.4f; chi-square %.1f (8 df)" % (n, mad, chi), body),
      {"column": a.column, "n": n, "skipped": len(raw) - n, "counts": c[1:], "shares": [round(o, 4) for o in obs[1:]],
       "benford": [round(e, 4) for e in exp[1:]], "mad": round(mad, 5), "chi_square_8df": round(chi, 2)})
