#!/usr/bin/env python3
"""figure.py -- two panels: which of the sentence's words are in the source, and why the
sentence's relation to that source cannot be a subset relation.

Panel A is the standing position written out word by word, each content term carrying the
number of times it occurs in the two texts by the author the sentence's centre was taken
from. Six of the eleven carry zero, and they are the six the sentence uses to say what error
is. Every number is read from readings.json and judged.json; none is typed here.

Panel B is the cross. Rheinberger separates his two kinds of object on one axis -- determined
against underdetermined -- and this practice separates its own on another: a norm imposed
against no norm imposed. Drawn as two axes rather than one, four quadrants appear, and the
one in the upper left is the case the standing sentence has no room for: a difference that
has been called an error and is still entirely unknown.
"""

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = json.load(open(HERE / "readings.json", encoding="utf-8"))
J = json.load(open(HERE / "judged.json", encoding="utf-8"))

ORDER = ["error", "special", "case", "epistemic", "thing",
         "difference", "onto", "observer", "already", "imposed", "norm"]
GENUINE = {t: J["verdicts"][t]["genuine"] for t in ORDER}
TOTAL = {t: sum(R["terms"][t]["counts"].values()) for t in ORDER}
ABSENT = [t for t in ORDER if GENUINE[t] == 0]

W, H = 1020, 1050
s = []
a = s.append

alt = ("Two panels. Above: the eleven content terms of this practice's standing position, each "
       "with the number of times it occurs in two texts by Hans-Joerg Rheinberger, the author "
       "its central term was taken from. Five terms occur -- epistemic, thing, difference, case, "
       "already -- and six do not: error, special, onto, observer, imposed, norm. The five that "
       "occur are the ones the sentence borrowed; the six that do not are the ones it uses to say "
       "what error is. Below: a cross with two axes. The horizontal axis is Rheinberger's, running "
       "from underdetermined to determined, with the epistemic thing at one end and the technical "
       "object at the other. The vertical axis is this practice's, running from no norm imposed to "
       "a norm imposed. Four quadrants result. A difference that has been called an error and is "
       "still entirely unknown sits in the upper left, and the standing sentence, which makes error "
       "a special case of the epistemic thing, has no room for it.")

a('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="100%%" role="img" '
  'aria-label="%s">' % (W, H, alt))
a('''<style>
 .bg{fill:#f7f5f0}
 .cell{fill:#ece7dc;stroke:#d8d2c6;stroke-width:.9}
 .cellnil{fill:#f7f5f0;stroke:#b04a33;stroke-width:1.6}
 .axis{stroke:#6b655a;stroke-width:1.4}
 .axisl{stroke:#9a9384;stroke-width:1;stroke-dasharray:3 4}
 .quad{fill:#ece7dc;stroke:#d8d2c6;stroke-width:.9}
 .quadhot{fill:#f4e7e2;stroke:#b04a33;stroke-width:1.4}
 .dot{fill:#2f5d50}
 .bar{fill:#2f5d50}
 .hd{font:600 19px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c}
 .h2{font:600 13.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c}
 .sub{font:13px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#6b655a}
 .term{font:600 13px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c;text-anchor:middle}
 .termnil{font:600 13px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#b04a33;text-anchor:middle}
 .glue{font:13px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#8a8478;text-anchor:middle}
 .small{font:11.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#6b655a}
 .smallc{font:11.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#6b655a;text-anchor:middle}
 .qlab{font:600 12.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#22201c;text-anchor:middle}
 .qtxt{font:11.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#6b655a;text-anchor:middle}
 .qred{font:600 11.5px Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif;fill:#b04a33;text-anchor:middle}
 .num{font:600 12px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;fill:#22201c;text-anchor:middle}
 .numnil{font:600 12px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;fill:#b04a33;text-anchor:middle}
 .axlab{font:11.5px SFMono-Regular,Menlo,DejaVu Sans Mono,Consolas,monospace;fill:#6b655a}
</style>''')
a('<rect class="bg" x="0" y="0" width="%d" height="%d"/>' % (W, H))


def wrap(text, width):
    lines, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            lines.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        lines.append(line)
    return lines


def para(x, y, text, width=128, lead=17, cls="small"):
    for k, ln in enumerate(wrap(text, width)):
        a('<text class="%s" x="%.1f" y="%.1f">%s</text>' % (cls, x, y + k * lead, ln))
    return y + lead * len(wrap(text, width))

a('<text class="hd" x="34" y="42">The borrowed axis</text>')
a('<text class="sub" x="34" y="65">Sixty-seven sessions after this practice took '
  '<tspan style="font-style:italic">epistemic thing</tspan> out of Rheinberger, it opened him. '
  'Six of the eleven words of its own sentence are not in him at all.</text>')

# ---------------------------------------------------------------- panel A
a('<text class="h2" x="34" y="112">Each content term of the standing position, and how often it '
  'occurs in the two texts read tonight</text>')

X0, X1, Y = 44.0, 976.0, 150.0
BW = (X1 - X0) / len(ORDER)
MAX = max(TOTAL.values())
for i, t in enumerate(ORDER):
    x = X0 + i * BW
    nil = GENUINE[t] == 0
    a('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="64" rx="3"/>'
      % ("cellnil" if nil else "cell", x + 3, Y, BW - 6))
    a('<text class="%s" x="%.1f" y="%.1f">%s</text>'
      % ("termnil" if nil else "term", x + BW / 2, Y + 25, t))
    a('<text class="%s" x="%.1f" y="%.1f">%d</text>'
      % ("numnil" if nil else "num", x + BW / 2, Y + 45, TOTAL[t]))
    if not nil:
        h = 42.0 * TOTAL[t] / MAX
        a('<rect class="bar" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
          % (x + BW / 2 - 13, Y + 140 - h, 26, h))
    else:
        a('<text class="qred" x="%.1f" y="%.1f">absent</text>' % (x + BW / 2, Y + 84))

a('<line class="axisl" x1="44" y1="%.1f" x2="976" y2="%.1f"/>' % (Y + 140, Y + 140))
para(44, Y + 168,
     "The five that occur are the five the sentence borrowed. The six that do not are the six it "
     "uses to say what error is. The counter, whose normalisation is declared loose in one "
     "direction only, found three of those six anyway - inside especially, inside contours, and "
     "across a word gap the extractor dropped - which is the declared looseness doing exactly "
     "what it was declared to do.")

# ---------------------------------------------------------------- panel B
TOP = 400.0
a('<text class="h2" x="34" y="%.1f">Two axes, not one</text>' % TOP)
para(34, TOP + 24,
     "Rheinberger sorts his objects by how far they are determined - the horizontal axis. This "
     "practice sorts differences by whether a norm has been imposed on them - the vertical one. "
     "Those are different questions, so they cross.")

CX0, CX1 = 180.0, 900.0
CY0, CY1 = TOP + 100, TOP + 500
MX, MY = (CX0 + CX1) / 2, (CY0 + CY1) / 2
QUADS = [
    (CX0, CY0, "an error nobody understands",
     "a failing test, a bug marked high severity and not diagnosed, "
     "an erratum judged and unexplained", True),
    (MX, CY0, "a known defect",
     "judged, and determined: the closed erratum, the reproduced bug, "
     "the instrument whose failure mode is documented", False),
    (CX0, MY, "the epistemic thing proper",
     "Rheinberger's own: “this difference remained mute experimentally: "
     "It did not lend itself further specification”", False),
    (MX, MY, "the technical object",
     "determined, and nobody is judging it: the liquid scintillation counter, "
     "the subroutine, the standard", False),
]
for x, y, label, txt, hot in QUADS:
    a('<rect class="%s" x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
      % ("quadhot" if hot else "quad", x + 2, y + 2, (CX1 - CX0) / 2 - 4, (CY1 - CY0) / 2 - 4))
    a('<text class="%s" x="%.1f" y="%.1f">%s</text>'
      % ("qred" if hot else "qlab", x + (CX1 - CX0) / 4, y + 34, label))
    words, line, lines = txt.split(), "", []
    for w in words:
        if len(line) + len(w) > 44:
            lines.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    lines.append(line)
    for k, ln in enumerate(lines):
        a('<text class="qtxt" x="%.1f" y="%.1f">%s</text>'
          % (x + (CX1 - CX0) / 4, y + 58 + 16 * k, ln))

a('<line class="axis" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (CX0, MY, CX1, MY))
a('<line class="axis" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (MX, CY0, MX, CY1))
a('<text class="axlab" x="%.1f" y="%.1f">&#8592; underdetermined</text>' % (CX0 + 10, MY - 12))
a('<text class="axlab" x="%.1f" y="%.1f" text-anchor="end">determined &#8594;</text>' % (CX1 - 10, MY - 12))
a('<text class="axlab" x="%.1f" y="%.1f" text-anchor="middle">&#8593; a norm imposed</text>'
  % (MX, CY0 - 12))
a('<text class="axlab" x="%.1f" y="%.1f" text-anchor="middle">&#8595; no norm imposed</text>'
  % (MX, CY1 + 22))
a('<text class="axlab" x="%.1f" y="%.1f" transform="rotate(-90 %.1f %.1f)" text-anchor="middle">'
  'this practice&#8217;s axis</text>' % (CX0 - 26, MY, CX0 - 26, MY))
a('<text class="axlab" x="%.1f" y="%.1f" transform="rotate(-90 %.1f %.1f)" text-anchor="middle">'
  'Rheinberger&#8217;s axis</text>' % (CX1 + 30, MY, CX1 + 30, MY))

y = para(34, CY1 + 58,
         "The standing sentence says error is a special case of the epistemic thing. A special "
         "case is a subset, and a subset needs one axis. On two axes the upper-left quadrant is "
         "a difference that is both at once - called an error, and still entirely unknown - and "
         "that is not a special case of anything.")
para(34, y + 8,
     "Counts: readings.json, produced by reconcile.py from the sources declared in "
     "sources/MANIFEST.json, and judged by hand in judged.json. Quadrant examples: quotes.json "
     "for Rheinberger's, this record for the others (Sessions 73, 74, 89).")

a('</svg>')
svg = "\n".join(s) + "\n"
(HERE / "figure.svg").write_text(svg, encoding="utf-8")
print("figure.svg  %d bytes, %d terms absent: %s" % (len(svg), len(ABSENT), ", ".join(ABSENT)))
