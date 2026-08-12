#!/usr/bin/env python3
"""Draw figure.svg from results.json. No randomness, no seed; every mark is a datum.

The drawing is one time axis, 2012-08 to 2026-07, with the two channels of the same
institution stacked on it:

  above the axis  every retroactive edit to a historical row — a published fact about a
                  period that had already ended, rewritten. One stroke per event; the
                  vertical position is the identifier's rank in the namespace, so a
                  column is one release and a row is one place on earth.
  below the axis  every withdrawal of an identifier. One stroke per event.

Nothing is aggregated away: the two bands hold 593 and 2 marks respectively, and the
figure's only argument is that you can count the lower band by eye.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))

W, H = 1180, 620
L, RGT = 74, 26
AXIS = 430          # y of the time axis
TOP = 74            # y of the top of the upper band
LOW = AXIS + 96     # y of the lower band's baseline

INK = "#1b1b1b"
FAINT = "#9a9a9a"
HOT = "#b3261e"


def year_frac(datestr):
    y, m, d = (int(x) for x in datestr.split("-"))
    return y + (m - 1) / 12 + (d - 1) / 365


dates = [p["date"] for p in R["id_count_series"]]
T0, T1 = year_frac(min(dates)), year_frac(max(dates))


def X(datestr):
    return L + (year_frac(datestr) - T0) / (T1 - T0) * (W - L - RGT)


# identifier rank: alphabetical over every identifier that ever existed, so the vertical
# position of a mark is stable and means something (Africa/... at the top, Pacific/... low)
names = sorted({p["id"] for p in R["retro_hist_points"]} |
               {p["id"] for p in R["removal_points"]})
rank = {n: i for i, n in enumerate(names)}
BAND = AXIS - 34 - TOP


def Y(name):
    return TOP + rank[name] / max(1, len(names) - 1) * BAND


out = []
a = out.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
  f'viewBox="0 0 {W} {H}" font-family="Iowan Old Style, Palatino, Georgia, serif">')
a(f'<rect width="{W}" height="{H}" fill="#faf8f4"/>')

# year gridlines
for yr in range(2013, 2027):
    x = X(f"{yr}-01-01")
    a(f'<line x1="{x:.1f}" y1="{TOP - 16}" x2="{x:.1f}" y2="{LOW + 20}" '
      f'stroke="{FAINT}" stroke-width="0.4" stroke-dasharray="1 4"/>')
    a(f'<text x="{x:.1f}" y="{LOW + 40}" font-size="11" fill="{FAINT}" '
      f'text-anchor="middle">{yr}</text>')

# upper band: one stroke per retroactive edit of a historical row
for p in R["retro_hist_points"]:
    x, y = X(p["date"]), Y(p["id"])
    a(f'<line x1="{x:.1f}" y1="{y - 2.6:.1f}" x2="{x:.1f}" y2="{y + 2.6:.1f}" '
      f'stroke="{INK}" stroke-width="1.5" stroke-opacity="0.72"/>')

# the axis
a(f'<line x1="{L}" y1="{AXIS}" x2="{W - RGT}" y2="{AXIS}" stroke="{INK}" '
  f'stroke-width="1"/>')

# release ticks on the axis
for r in R["id_count_series"]:
    x = X(r["date"])
    a(f'<line x1="{x:.1f}" y1="{AXIS - 3}" x2="{x:.1f}" y2="{AXIS + 3}" '
      f'stroke="{INK}" stroke-width="0.7"/>')

# lower band: the withdrawals
for p in R["removal_points"]:
    x = X(p["date"])
    a(f'<line x1="{x:.1f}" y1="{AXIS + 12}" x2="{x:.1f}" y2="{LOW}" '
      f'stroke="{HOT}" stroke-width="1.8"/>')
    a(f'<circle cx="{x:.1f}" cy="{LOW}" r="3" fill="{HOT}"/>')
    a(f'<text x="{x + 7:.1f}" y="{LOW - 26:.1f}" font-size="12.5" fill="{HOT}">'
      f'{p["id"]}</text>')
    a(f'<text x="{x + 7:.1f}" y="{LOW - 11:.1f}" font-size="11" fill="{HOT}" '
      f'fill-opacity="0.8">withdrawn in {p["tag"]}</text>')

# labels
a(f'<text x="{L}" y="{TOP - 34}" font-size="15.5" fill="{INK}">'
  f'{R["n_retro_hist_events"]} rewrites of a historical row '
  f'&#183; {R["n_retro_hist_ids"]} of {R["identifiers_ever"]} identifiers '
  f'&#183; {R["n_transitions_with_retro_hist"]} of {R["n_transitions"]} releases</text>')
a(f'<text x="{L}" y="{TOP - 18}" font-size="11.5" fill="{FAINT}">'
  f'a published fact about a period that had already ended, changed. '
  f'vertical position = the identifier, alphabetically.</text>')
a(f'<text x="{L}" y="{LOW + 66}" font-size="15.5" fill="{HOT}">'
  f'{R["n_removals"]} withdrawals of an identifier, in fourteen years</text>')
a(f'<text x="{L}" y="{LOW + 82}" font-size="11.5" fill="{FAINT}">'
  f'both were unused misnomers in the backward-compatibility file; '
  f'neither corrected a fact about the world.</text>')
a(f'<text x="{L}" y="{H - 16}" font-size="11" fill="{FAINT}">'
  f'IANA time zone database, releases {R["window"][0]}&#8211;{R["window"][2]}. '
  f'Same institution, same releases, same files. '
  f'Measured from data/ by measure.py; every mark is one event in edits.json.</text>')
a('</svg>')

path = os.path.join(HERE, "figure.svg")
open(path, "w").write("\n".join(out))
print(f"wrote {path}  ({len(R['retro_hist_points'])} + {len(R['removal_points'])} marks)")
