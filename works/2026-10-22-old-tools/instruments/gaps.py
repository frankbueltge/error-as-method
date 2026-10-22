"""GAPS, an instrument. Finds where a record breaks its own cadence.

usage: python3 instrument.py data.csv --time TIMECOLUMN
It reads the time of every row (ISO 8601 dates or datetimes, or plain numbers), takes the most common
interval between neighbouring rows as the record's own cadence, and lists every place where that
interval is not kept: a gap (longer), a repeat (zero), a step back (negative), or an irregular step
(shorter). Rows whose time cannot be read are counted too. Writes reading.svg (the record as one line,
each break marked where it falls) and reading.json (the cadence, the counts and the largest breaks)."""
import argparse, sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import read, when, svg, write, esc
a = argparse.ArgumentParser(); a.add_argument("csv"); a.add_argument("--time", required=True); a = a.parse_args()
raw = read(a.csv, a.time); t = [when(s) for s in raw]; bad = sum(v is None for v in t)
t = [v for v in t if v is not None]
if len(t) < 3: sys.exit("fewer than three readable times")
d = [t[i + 1] - t[i] for i in range(len(t) - 1)]; cad = Counter(round(v, 6) for v in d).most_common(1)[0][0]
kinds = Counter(); br = []
for i, v in enumerate(d):
    if abs(v - cad) <= 1e-6 * max(1, abs(cad)): continue
    k = "gap" if v > cad else "repeat" if v == 0 else "step back" if v < 0 else "irregular"
    kinds[k] += 1; br.append((i, k, v))
lo, hi = min(t), max(t); span = (hi - lo) or 1
col = {"gap": "#a33", "repeat": "#36c", "step back": "#a3a", "irregular": "#888"}
body = '<line x1="40" x2="960" y1="300" y2="300" stroke="#1b1b1b"/>'
for i, k, v in br[:5000]:
    xx = 40 + 920 * (t[i] - lo) / span
    if k == "gap": body += '<rect x="%.1f" y="240" width="%.1f" height="120" fill="#a33" fill-opacity="0.55"/>' % (xx, max(1, 920 * v / span))
    else: body += '<line x1="%.1f" x2="%.1f" y1="250" y2="350" stroke="%s"/>' % (xx, xx, col[k])
def human(s):
    for u, q in (("days", 86400), ("hours", 3600), ("minutes", 60)):
        if abs(s) >= q: return "%.4g %s" % (s / q, u)
    return "%.4g s" % s
leg = "cadence %s · %s · unreadable times %d" % (human(cad), ", ".join("%s %d" % kv for kv in sorted(kinds.items())) or "no breaks", bad)
body += '<text x="40" y="420" font-size="15" fill="#1b1b1b">%s</text>' % esc(leg)
body += '<text x="40" y="530" font-size="13" fill="#555">first row</text><text x="960" y="530" font-size="13" fill="#555" text-anchor="end">last row (%d rows)</text>' % len(t)
big = sorted((b for b in br if b[1] == "gap"), key=lambda b: -b[2])[:5]
write("GAPS", svg("GAPS · " + a.time, "where the record does not keep its own most common interval", body),
      {"time_column": a.time, "rows": len(raw), "unreadable_times": bad, "cadence_seconds": cad, "cadence": human(cad),
       "breaks": dict(kinds), "largest_gaps": [{"after_row": i + 2, "length": human(v)} for i, k, v in big]})
