"""PLOT, an instrument. Draws the values of one column in the order they stand in the file, as a line.

usage: python3 instrument.py data.csv --column VALUE
Writes reading.svg (the picture) and reading.json (count, minimum, maximum) into the current folder.
Empty or non-numeric cells are skipped and counted."""
import argparse, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read, num, svg, write, esc
a = argparse.ArgumentParser(); a.add_argument("csv"); a.add_argument("--column", required=True); a = a.parse_args()
raw = read(a.csv, a.column); v = [num(s) for s in raw]; x = [t for t in v if t is not None]
if len(x) < 2: sys.exit("fewer than two numbers in the column")
lo, hi = min(x), max(x); span = (hi - lo) or 1; n = len(x)
step = max(1, n // 2000); pts = []
for i in range(0, n, step):
    pts.append("%.1f,%.1f" % (40 + 920 * i / max(1, n - 1), 500 - 400 * (x[i] - lo) / span))
body = ('<polyline fill="none" stroke="#1b1b1b" stroke-width="1" points="%s"/>' % " ".join(pts) +
        '<text x="40" y="530" font-size="13" fill="#555">first value</text>'
        '<text x="960" y="530" font-size="13" fill="#555" text-anchor="end">last value (n = %d)</text>' % n +
        '<text x="964" y="104" font-size="13" fill="#555">%s</text><text x="964" y="500" font-size="13" fill="#555">%s</text>' % (esc("%g" % hi), esc("%g" % lo)))
write("PLOT", svg("PLOT · " + a.column, "%d values in file order; %d cells skipped" % (n, len(raw) - n), body),
      {"column": a.column, "n": n, "skipped": len(raw) - n, "min": lo, "max": hi})
