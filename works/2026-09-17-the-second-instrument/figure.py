#!/usr/bin/env python3
"""figure.py -- two panels: the interval that collapses, and the forty rows that decided it.

Panel A is the night's number.  Panel B is the night's evidence: forty columns, one per hand-read
row, four rows -- the reader and the three declared rules -- so that the disagreement can be
counted off the page rather than taken from a table.  Written after score.py; every value read from
results.json and adjudication.json, none typed.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = json.load(open(HERE / "results.json"))
ADJ = json.load(open(HERE / "adjudication.json"))
A = R["against_the_reader"]
P = R["over_the_population"]

W, H = 1020, 700
X0, X1 = 250.0, 930.0          # panel A plot area
SCALE = 55.0                   # per cent full scale

DECLARED = ["R1_adjacent_subject", "R2_no_competing_nominal", "R3_active_governor"]
SHORT = {"R1_adjacent_subject": "R1  adjacent subject",
         "R2_no_competing_nominal": "R2  no competing nominal",
         "R3_active_governor": "R3  active governor"}

s = []
a = s.append


def x(pct):
    return X0 + (X1 - X0) * pct / SCALE


alt = ("Two panels. Above: for each of three party-term vocabularies, the reach Session 90 "
       "published and the reach left after each carrier is asked whether it acts. The three raw "
       "figures span 50.15 points; the corrected figures span 13.33. Below: forty columns, one per "
       "hand-read row, showing the reader's verdict and each of three declared rules, so the "
       "disagreement can be counted.")

a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" role="img" '
  'aria-label="%s">' % (W, H, alt))
a('''<style>
 .bg{fill:#f7f5f0}
 .grid{stroke:#d8d2c6;stroke-width:1}
 .raw{fill:#c9c2b2}
 .cor{fill:#2f5d50}
 .corb{fill:#7fa99b}
 .rule{stroke:#22201c;stroke-width:1.4}
 .hd{font:600 18px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c}
 .h2{font:600 13.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c}
 .sub{font:13px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#6b655a}
 .lab{font:13px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c;text-anchor:end}
 .small{font:11.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#6b655a}
 .num{font:600 12px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;fill:#22201c}
 .numl{font:11.5px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;fill:#6b655a}
 .tick{font:10.5px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;fill:#6b655a;text-anchor:middle}
 .cellY{fill:#2f5d50}
 .cellN{fill:#ece7dc}
 .cellE{fill:#b04a33}
 .cellbox{stroke:#d8d2c6;stroke-width:.7}
 .key{font:11.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c}
</style>''')
a('<rect class="bg" x="0" y="0" width="%d" height="%d"/>' % (W, H))

a('<text class="hd" x="34" y="40">Asking each carrier whether it acts</text>')
a('<text class="sub" x="34" y="62">660 binding agentless obligations in 63 UK Acts. '
  'Reach: the share with a term for a party within 36 words behind them &#8212; a ceiling on a '
  'bearer named, never naming.</text>')

# ---------------------------------------------------------------- panel A
a('<text class="h2" x="34" y="102">The interval, before and after</text>')
top = 120
rowh = 62
for i in range(0, 60, 10):
    a('<line class="grid" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (x(i), top - 8, x(i), top + 3 * rowh + 6))
    a('<text class="tick" x="%.1f" y="%d">%d%%</text>' % (x(i), top + 3 * rowh + 24, i))

order = ["base", "narrow", "wide"]
names = {"base": "BASE  the shared 26", "narrow": "NARROW  + 15 UK offices",
         "wide": "WIDE  + person"}
for i, l in enumerate(order):
    y = top + i * rowh
    raw = P[l]["session_90_published_reach_pct"]
    c3 = P[l]["by_rule"]["R3_active_governor"]["corrected_reach_pct"]
    c3b = P[l]["by_rule"]["R3b_active_governor_own_block"]["corrected_reach_pct"]
    a('<text class="lab" x="%.1f" y="%d">%s</text>' % (X0 - 14, y + 20, names[l]))
    a('<rect class="raw" x="%.1f" y="%d" width="%.1f" height="26"/>' % (x(0), y, x(raw) - x(0)))
    a('<rect class="corb" x="%.1f" y="%d" width="%.1f" height="26"/>' % (x(0), y, max(x(c3b) - x(0), .5)))
    a('<rect class="cor" x="%.1f" y="%d" width="%.1f" height="26"/>' % (x(0), y, max(x(c3) - x(0), .5)))
    a('<text class="num" x="%.1f" y="%d">%.2f%%</text>' % (x(raw) + 9, y + 19, raw))
    a('<text class="numl" x="%.1f" y="%d">%.2f / %.2f</text>' % (x(0) + 6, y + 48, c3, c3b))

sp_raw = ADJ["predictions"]["P4"]["numbers"]["uncorrected_span_session_90"]
sp_c = ADJ["predictions"]["P4"]["numbers"]["corrected_span_points"]
sp_cb = ADJ["predictions"]["P4"]["numbers"]["corrected_span_points_R3b"]
a('<text class="small" x="%.1f" y="%d">Raw span <tspan class="num">%.2f</tspan> points &#183; '
  'corrected span <tspan class="num">%.2f</tspan> (R3) and <tspan class="num">%.2f</tspan> (R3b) '
  '&#183; the falsification band this line has been arguing inside is 20.</text>'
  % (X0 - 216, top + 3 * rowh + 48, sp_raw, sp_c, sp_cb))

# ---------------------------------------------------------------- panel B
btop = 410
a('<text class="h2" x="34" y="%d">The forty rows the rules were scored on</text>' % (btop - 22))
a('<text class="small" x="34" y="%d">One column per hand-read row, sorted by the reader\'s verdict '
  'then by sample order. Filled = bearer / rule fires. Red = the rule contradicts the reader.</text>'
  % (btop - 5))

rows = sorted(A["rows"], key=lambda r: (not r["reader"], r["n"]))
cw, gap = 13.5, 2.0
gx = X0
lanes = [("the reader", None)] + [(SHORT[n], n) for n in DECLARED]
for li, (label, key) in enumerate(lanes):
    y = btop + li * 30
    a('<text class="lab" x="%.1f" y="%d">%s</text>' % (gx - 14, y + 15, label))
    for ci, r in enumerate(rows):
        cx = gx + ci * (cw + gap)
        if key is None:
            cls = "cellY" if r["reader"] else "cellN"
        else:
            fires = r["rules"][key]
            cls = "cellE" if fires != r["reader"] else ("cellY" if fires else "cellN")
        a('<rect class="%s cellbox" x="%.1f" y="%d" width="%.1f" height="20"/>' % (cls, cx, y, cw))
    if key is not None:
        v = A["by_rule"][key]
        a('<text class="numl" x="%.1f" y="%d">%d/40 agree &#183; %d fire</text>'
          % (gx + 40 * (cw + gap) + 8, y + 15, v["agreements"], v["fires"]))
    else:
        a('<text class="numl" x="%.1f" y="%d">%d yes / %d no</text>'
          % (gx + 40 * (cw + gap) + 8, y + 15, A["reader_yes"], A["reader_no"]))

a('<text class="small" x="34" y="%d">Largest rule-to-rule disagreement <tspan class="num">%d</tspan> '
  'rows &#183; largest rule-to-reader disagreement <tspan class="num">%d</tspan>. The three rules do '
  'not cluster against the reader; one of them is further from her than they are from each other.</text>'
  % (btop + 4 * 30 + 18, A["max_rule_to_rule_disagreement"], A["max_rule_to_reader_disagreement"]))
a('<text class="small" x="34" y="%d">Session 91 &#183; Error as Method &#183; every value read from '
  'results.json and adjudication.json, committed beside this figure.</text>' % (btop + 4 * 30 + 40))
a('</svg>')

(HERE / "figure.svg").write_text("\n".join(s) + "\n")
print("wrote figure.svg -- %d bytes" % len("\n".join(s)))
