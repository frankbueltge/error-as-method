#!/usr/bin/env python3
"""Draw figure.svg from results.json. stdlib only, deterministic; no browser, no
external asset, no network.

Two panels, one argument.

  Upper — the book as a 286-page axis. Every occurrence of 'generative' is a tick on
  the top lane, every occurrence of 'unknowing' a tick on the lower one. The phrase
  this practice used for fifty-three days requires the two lanes to meet. They do not: the
  closest approach is bracketed and labelled.

  Lower — where the phrase actually accumulates. Three bars on one scale: the book
  (0), the review body (0), the review's title (3, being three printings of one
  title string), and this repository (74 across 31 files).

    python3 figure.py
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
res = json.load(open(os.path.join(HERE, "results.json")))
book = res["A_the_book"]
review = res["B_the_review"]
repo = res["C_this_repository"]

INK = "#1a1a1a"
FAINT = "#c9c4bb"
PAPER = "#f4f1ea"
GEN = "#5b6b7a"
UNK = "#c05a2e"

W = 900
L, R = 190, 60
plot_w = W - L - R


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- panel 1
# Re-derive character offsets from the same source probe.py measured, so the
# figure cannot drift from the numbers: the ticks are positions, and results.json
# stores contexts rather than every offset.
with open(os.path.join(HERE, "sources", "jones.txt")) as fh:
    n_text = re.sub(r"\s+", " ", fh.read())
total_chars = len(n_text)
gen_pos = [m.start() for m in re.finditer(r"\bgenerative\b", n_text, re.I)]
unk_pos = [m.start() for m in re.finditer(r"\bunknowing\b", n_text, re.I)]

assert len(gen_pos) == book["counts"]["generative"]
assert len(unk_pos) == book["counts"]["unknowing"]

TOP = 92
LANE_G, LANE_U = TOP, TOP + 52


def x_of(char):
    return L + (char / total_chars) * plot_w


parts = []
parts.append(
    '<text x="%d" y="34" font-family="Georgia,serif" font-size="17" fill="%s">'
    'Two words that never meet</text>' % (L, INK))
parts.append(
    '<text x="%d" y="56" font-family="Georgia,serif" font-size="12.5" fill="%s">'
    'Jones, %sGlitch Poetics%s (2022), %s pages, %s words &#183; every occurrence of each word'
    '</text>' % (L, "#5a544c", "&#8216;", "&#8217;",
                 book["pages"], "{:,}".format(book["words"])))

# lanes
for y, label, colour, positions in (
        (LANE_G, "generative", GEN, gen_pos),
        (LANE_U, "unknowing", UNK, unk_pos)):
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                 'stroke-width="1"/>' % (L, y, L + plot_w, y, FAINT))
    parts.append('<text x="%.1f" y="%.1f" text-anchor="end" font-family="Georgia,serif" '
                 'font-size="13" font-style="italic" fill="%s">%s</text>'
                 % (L - 12, y + 4, colour, label))
    parts.append('<text x="%.1f" y="%.1f" font-family="Georgia,serif" font-size="11.5" '
                 'fill="%s">%d</text>' % (L + plot_w + 8, y + 4, colour, len(positions)))
    for p in positions:
        parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                     'stroke-width="2"/>' % (x_of(p), y - 11, x_of(p), y + 11, colour))

# the closest approach
best = min(((abs(a - b), a, b) for a in gen_pos for b in unk_pos), key=lambda t: t[0])
gap, ga, ub = best
x1, x2 = sorted((x_of(ga), x_of(ub)))
BR = LANE_U + 34
parts.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f" fill="none" '
             'stroke="%s" stroke-width="1"/>'
             % (x1, BR - 8, x1, BR, x2, BR, x2, BR - 8, INK))
parts.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="Georgia,serif" '
             'font-size="12" fill="%s">closest approach: %s characters, about %s pages</text>'
             % ((x1 + x2) / 2, BR + 17, INK,
                "{:,}".format(book["min_char_gap_generative_to_unknowing"]),
                book["approx_pages_apart"]))

# page axis
AX = BR + 40
parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="1"/>'
             % (L, AX, L + plot_w, AX, FAINT))
for pg in (1, 50, 100, 150, 200, 250, 286):
    xx = L + ((pg - 1) / 285) * plot_w
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s"/>'
                 % (xx, AX, xx, AX + 5, FAINT))
    parts.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="Georgia,serif" '
                 'font-size="10.5" fill="%s">%d</text>' % (xx, AX + 17, "#8a837a", pg))
parts.append('<text x="%.1f" y="%.1f" text-anchor="end" font-family="Georgia,serif" '
             'font-size="10.5" font-style="italic" fill="%s">page</text>'
             % (L + plot_w, AX + 30, "#8a837a"))

# ---------------------------------------------------------------- panel 2
P2 = AX + 66
parts.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1"/>'
             % (L, P2 - 26, L + plot_w, P2 - 26, FAINT))
parts.append('<text x="%d" y="%.1f" font-family="Georgia,serif" font-size="17" fill="%s">'
             'Where %sgenerative unknowing%s actually occurs</text>'
             % (L, P2 - 2, INK, "&#8216;", "&#8217;"))

body_hits = review["unknowing_total"] - review["phrase_in_title_string"]
BARS = [
    ("the book, all 286 pages", 0, "0"),
    ("the review%s body prose" % "&#8217;s", 0,
     "0  (%d uses of %sunknowing%s, both of them verbs)" % (body_hits, "&#8216;", "&#8217;")),
    ("the review%s title" % "&#8217;s", review["phrase_in_title_string"],
     "%d  (one title string, printed %d times on the page)"
     % (review["phrase_in_title_string"], review["phrase_in_title_string"])),
    ("this repository", repo["total_occurrences"],
     "%d  across %d files, including a work titled with it"
     % (repo["total_occurrences"], repo["files_containing_phrase"])),
]
maxv = max(v for _, v, _ in BARS) or 1
BW = 300
for i, (label, val, note) in enumerate(BARS):
    y = P2 + 22 + i * 27
    parts.append('<text x="%.1f" y="%.1f" text-anchor="end" font-family="Georgia,serif" '
                 'font-size="12.5" fill="%s">%s</text>' % (L - 12, y + 4, INK, label))
    if val:
        parts.append('<rect x="%d" y="%.1f" width="%.1f" height="12" fill="%s"/>'
                     % (L, y - 6, (val / maxv) * BW, UNK if val > 5 else GEN))
    else:
        parts.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" '
                     'stroke-width="1.5"/>' % (L, y, L + 9, y, FAINT))
    tx = L + max((val / maxv) * BW, 9) + 10
    parts.append('<text x="%.1f" y="%.1f" font-family="Georgia,serif" font-size="11.5" '
                 'fill="%s">%s</text>' % (tx, y + 4, "#5a544c", note))

# the canvas is sized to the content rather than guessed at
H = int(P2 + 22 + (len(BARS) - 1) * 27 + 30)
parts.insert(0, '<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))

svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" '
       'height="%d" role="img" aria-label="%s">%s</svg>\n'
       % (W, H, W, H,
          esc("Upper panel: the 286 pages of Jones's Glitch Poetics with every occurrence "
              "of 'generative' and of 'unknowing' marked; the two never come within about "
              "42 pages of each other. Lower panel: the phrase 'generative unknowing' "
              "occurs zero times in the book, zero times in the review's body prose, "
              "three times as the review's title, and 74 times across 31 files of this "
              "repository."),
          "".join(parts)))

with open(os.path.join(HERE, "figure.svg"), "w") as fh:
    fh.write(svg)
print("wrote figure.svg  (%d bytes)" % len(svg))
print("closest approach: %s chars (~%s pages)"
      % ("{:,}".format(gap), book["approx_pages_apart"]))
