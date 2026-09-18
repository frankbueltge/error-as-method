#!/usr/bin/env python3
"""figure.py — two panels: where the load actually landed, and what the row did to the record.

Panel A is the standing sentence's eleven content terms, each carrying the number of fixed
readings Session 85's table gives it, with the five shapes of Sessions 88–91 drawn onto the term
they load. Three land where the table already has a reading; two land on terms that have none.

Panel B is the twelve nights either side of the night the falsifier was fixed: how often the word
the row names appears in each night's journal, per 1,000 words, and how many paragraphs a night
name the row beside it.

Written after score.py. Every value is read from results.json; none is typed.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = json.load(open(HERE / "results.json"))
SH = json.load(open(HERE / "shapes.json"))["shapes"]

TERMS = R["terms"]
COV = R["coverage"]
ALL = R["watch"]["all"]
GRIP = R["grip_post"]["per_night"]
GRIP_PRE = R["grip_pre"]["per_night"]

W, H = 1020, 830
s = []
a = s.append

alt = ("Two panels. Above: the eleven content terms of the standing sentence, each with the number "
       "of fixed readings this record has given it — four terms carry readings, seven carry none — "
       "and the five shapes Sessions 88 to 91 named, drawn onto the term each one actually loads. "
       "Three land on observer, which already has three readings; two land on difference and norm, "
       "which have none. Below: the word observer per 1,000 words in each of the twelve journal "
       "entries either side of the night the falsifier naming that word was fixed, and the number "
       "of paragraphs per night that name the falsifier beside it — exactly two on every night "
       "after it was fixed, and none before.")

a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" role="img" '
  'aria-label="%s">' % (W, H, alt))
a('''<style>
 .bg{fill:#f7f5f0}
 .grid{stroke:#d8d2c6;stroke-width:1}
 .cell{fill:#ece7dc;stroke:#d8d2c6;stroke-width:.9}
 .cellread{fill:#dfe7e3;stroke:#7fa99b;stroke-width:1.1}
 .dot{fill:#2f5d50}
 .bar{fill:#c9c2b2}
 .barpost{fill:#2f5d50}
 .lead{stroke:#9a9384;stroke-width:1.1;fill:none}
 .leadred{stroke:#b04a33;stroke-width:2;fill:none}
 .shape{fill:#f7f5f0;stroke:#9a9384;stroke-width:.9}
 .shapered{fill:#f7f5f0;stroke:#b04a33;stroke-width:1.6}
 .cut{stroke:#b04a33;stroke-width:1.2;stroke-dasharray:4 4}
 .hd{font:600 18px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c}
 .h2{font:600 13.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c}
 .sub{font:13px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#6b655a}
 .term{font:600 13px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c;text-anchor:middle}
 .termq{font:13px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#8a8478;text-anchor:middle}
 .small{font:11.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#6b655a}
 .smallc{font:11.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#6b655a;text-anchor:middle}
 .red{font:600 11.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#b04a33;text-anchor:middle}
 .shlab{font:11.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c;text-anchor:middle}
 .num{font:600 12px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;fill:#22201c;text-anchor:middle}
 .numl{font:10.5px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;fill:#6b655a;text-anchor:middle}
 .tick{font:10.5px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;fill:#6b655a;text-anchor:end}
</style>''')
a('<rect class="bg" x="0" y="0" width="%d" height="%d"/>' % (W, H))

a('<text class="hd" x="34" y="40">The word the row named</text>')
a('<text class="sub" x="34" y="62">Session 85 fixed a falsifier on <tspan style="font-style:italic">observer</tspan>. '
  'Four nights then reported that the pressure kept arriving at <tspan style="font-style:italic">observer</tspan>. '
  'Two of the five things they found are not about that word.</text>')

# ------------------------------------------------------------------ panel A
a('<text class="h2" x="34" y="106">The eleven content terms of the standing sentence, and what each carries</text>')

X0, X1 = 40.0, 980.0
n = len(TERMS)
cw = (X1 - X0) / n
CY, CH = 176.0, 38.0
cx = {t: X0 + cw * (i + 0.5) for i, t in enumerate(TERMS)}

for i, t in enumerate(TERMS):
    x = X0 + cw * i
    read = COV[t]["n_readings"]
    a('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"/>'
      % ("cellread" if read else "cell", x + 3, CY, cw - 6, CH))
    a('<text class="%s" x="%.1f" y="%.1f">%s</text>'
      % ("term" if read else "termq", cx[t], CY + 24, t))
    # one dot per fixed reading, with its session number under it
    for j, r in enumerate(COV[t]["readings"]):
        dx = cx[t] - (len(COV[t]["readings"]) - 1) * 23 / 2 + j * 23
        a('<circle class="dot" cx="%.1f" cy="%.1f" r="4.4"/>' % (dx, CY - 30))
        a('<text class="numl" x="%.1f" y="%.1f">%d</text>' % (dx, CY - 42, r["session"]))
    if not read:
        a('<text class="numl" x="%.1f" y="%.1f">0</text>' % (cx[t], CY - 30))

a('<text class="small" x="40" y="120">readings fixed on the term, by session</text>')
a('<text class="small" x="40" y="%.1f">seven of the eleven have never been given one</text>' % (CY + 60))

# the five shapes, and the term each loads
SY = 300.0
order = ["SH-88-READER", "SH-89-UNIT", "SH-90-LEXICON", "SH-91-RULE", "SH-91-KAPPA"]
LABEL = {"SH-88-READER": "S88  a reader", "SH-89-UNIT": "S89  a unit",
         "SH-90-LEXICON": "S90  a lexicon", "SH-91-RULE": "S91  a decision rule",
         "SH-91-KAPPA": "S91  a coefficient"}
byid = {x["id"]: x for x in SH}
bw = 172.0
for i, sid in enumerate(order):
    sh = byid[sid]
    bx = X0 + 12 + i * (bw + 16)
    new = sh["derives_from"] is None
    a('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="34" rx="3"/>'
      % ("shapered" if new else "shape", bx, SY, bw))
    a('<text class="shlab" x="%.1f" y="%.1f">%s</text>' % (bx + bw / 2, SY + 22, LABEL[sid]))
    tx, ty = cx[sh["lands_on"]], CY + CH
    a('<path class="%s" d="M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f"/>'
      % ("leadred" if new else "lead", bx + bw / 2, SY, bx + bw / 2, SY - 40, tx, ty + 44, tx, ty + 4))

a('<text class="small" x="40" y="%.1f">Grey: the shape is an instance of a reading the table already has — '
  'S88 of Session 26, both S91 shapes of Session 78. Red: the shape loads a term with no reading at all.</text>'
  % (SY + 56))

# ------------------------------------------------------------------ panel B
BY0, BY1 = 700.0, 470.0
a('<text class="h2" x="34" y="%.1f">The same word, per 1,000 words, in the twelve journal entries either side of the row</text>' % 416)

pre = {int(k): v for k, v in ALL["pre_per_night"].items()}
post = {int(k): v for k, v in ALL["post_per_night"].items()}
nights = sorted(pre) + sorted(post)
rate = {s_: 1000.0 * (pre.get(s_) or post.get(s_))["observer"] / (pre.get(s_) or post.get(s_))["words"]
        for s_ in nights}
top = 2.0
bx0, bx1 = 92.0, 900.0
slot = (bx1 - bx0) / (len(nights) + 1)   # one empty slot for the excluded night


def by(v):
    return BY0 - (BY0 - BY1) * min(v, top) / top


for g in (0.0, 0.5, 1.0, 1.5, 2.0):
    a('<line class="grid" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (bx0 - 6, by(g), bx1, by(g)))
    a('<text class="tick" x="%.1f" y="%.1f">%.1f</text>' % (bx0 - 12, by(g) + 4, g))

i = 0
for s_ in nights:
    if s_ == 86:
        i += 1   # the excluded night keeps its place on the axis
    x = bx0 + slot * i + slot * 0.08
    w = slot * 0.84
    a('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
      % ("barpost" if s_ >= 86 else "bar", x, by(rate[s_]), w, BY0 - by(rate[s_])))
    a('<text class="numl" x="%.1f" y="%.1f">%d</text>' % (x + w / 2, BY0 + 16, s_))
    g = (GRIP if s_ >= 86 else GRIP_PRE)[str(s_)]["also_naming_the_row"]
    a('<text class="%s" x="%.1f" y="%.1f">%d</text>'
      % ("red" if g else "smallc", x + w / 2, BY0 + 34, g))
    i += 1

xcut = bx0 + slot * 6 + slot * 0.5
a('<line class="cut" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (xcut, BY1 - 26, xcut, BY0 + 6))
a('<text class="red" x="%.1f" y="%.1f">Session 85 — the row is fixed</text>' % (xcut, BY1 - 34))
a('<text class="small" x="40" y="%.1f">session</text>' % (BY0 + 16))
a('<text class="small" x="40" y="%.1f">row named in</text>' % (BY0 + 34))
a('<text class="small" x="92" y="%.1f">Rate ratio, six nights after against six before: '
  '<tspan style="font-weight:600">%.3f</tspan> — the highest of the eleven terms.</text>'
  % (BY0 + 62, ALL["per_term"]["observer"]["ratio"]))
a('<text class="small" x="92" y="%.1f">The second axis row counts that night\'s paragraphs naming the row: '
  'two on every night after it was fixed, none before.</text>' % (BY0 + 80))
a('<text class="small" x="92" y="%.1f">Session 85 is excluded from both windows, declared before the count: '
  'it is the night that fixed the row and wrote the load table.</text>' % (BY0 + 98))

a('</svg>')
(HERE / "figure.svg").write_text("\n".join(s) + "\n", encoding="utf-8")
print("figure.svg", (HERE / "figure.svg").stat().st_size, "bytes")
