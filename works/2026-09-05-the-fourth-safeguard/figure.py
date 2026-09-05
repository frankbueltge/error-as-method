#!/usr/bin/env python3
"""Draws figure.svg from results.json and census.json. Deterministic; no randomness, so no seed.

Three panels, top to bottom:

  1. THE PREAMBLE -- 173 cells, one per recital, filled where the recital contains a sentence that
     names an actor of the Regulation and tells it, with 'should', to do something. Guideline 10 of
     the Joint Practical Guide says that number should be zero.
  2. THE ENACTING TERMS -- 99 cells, one per article, with the two occurrences of 'should' marked.
  3. THE LADDER -- recital 71's four safeguards against Article 22(3)'s three: three rungs cross,
     one crosses under another verb, and one ends in the gap this work is named after.
"""

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
R = json.loads((HERE / "results.json").read_text(encoding="utf-8"))

INK = "#16150f"
PAPER = "#f4f1e8"
FAINT = "#d8d2c2"
GREY = "#8d8877"
ACCENT = "#8c2f18"
FONT = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif"
MONO = "'IBM Plex Mono','DejaVu Sans Mono',Menlo,monospace"

W, H = 1000, 860
CELL, GAP, PER_ROW = 22, 5, 25


def cells(x0, y0, n, filled, outlined, title_of):
    out = []
    for i in range(1, n + 1):
        col, row = (i - 1) % PER_ROW, (i - 1) // PER_ROW
        x, y = x0 + col * (CELL + GAP), y0 + row * (CELL + GAP)
        fill = INK if i in filled else PAPER
        stroke = ACCENT if i in outlined else FAINT
        width = 2.2 if i in outlined else 1
        out.append(
            '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="%s" stroke-width="%s">'
            '<title>%s</title></rect>' % (x, y, CELL, CELL, fill, stroke, width, title_of(i)))
        if i in outlined:
            out.append('<text x="%d" y="%d" font-family="%s" font-size="9" fill="%s" '
                       'text-anchor="middle">%d</text>' % (x + CELL / 2, y + CELL + 11, MONO, ACCENT, i))
    rows = (n + PER_ROW - 1) // PER_ROW
    return "\n".join(out), y0 + rows * (CELL + GAP)


def main():
    directed = set(R["directed_normative"]["recitals_with_a_directed_sentence"])
    art_should = {int(k) for k in R["register"]["articles"]["should"]["per_division"]}

    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
             'role="img" aria-label="Regulation (EU) 2016/679: 71 of 173 recitals carry a directed '
             'normative sentence; 2 of 99 articles carry a non-mandatory should; recital 71 lists '
             'four safeguards and Article 22(3) carries three.">' % (W, H, W, H),
             '<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER)]

    def text(x, y, s, size=13, fill=INK, font=FONT, anchor="start", weight="normal", style="normal"):
        parts.append('<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s" '
                     'text-anchor="%s" font-weight="%s" font-style="%s">%s</text>'
                     % (x, y, font, size, fill, anchor, weight, style, s))

    text(40, 46, "The Fourth Safeguard", 26)
    text(40, 68, "Regulation (EU) 2016/679 — what the preamble says and the enacting terms do not",
         13, GREY)

    # panel 1
    text(40, 108, "THE PREAMBLE — 173 recitals, no binding force (C-162/97 Nilsson, §54)",
         11, INK, MONO)
    text(40, 126, "filled: the recital names an actor of the Regulation and tells it, with "
                  "‘should’, to do something", 11, GREY)
    body, y = cells(40, 138, 173, directed, {71},
                    lambda i: "recital %d%s" % (i, " — directed" if i in directed else ""))
    parts.append(body)
    text(40, y + 30, "71 of 173.", 14, ACCENT, FONT, "start", "bold")
    text(88, y + 30, "Guideline 10 of the Joint Practical Guide (2015): recitals "
                     "‘SHALL NOT CONTAIN NORMATIVE PROVISIONS’.", 12, INK)
    text(40, y + 48, "‘shall’ in the preamble: 0.  ‘should’ in the preamble: 420.",
         11, GREY, MONO)

    # panel 2
    y2 = y + 82
    text(40, y2, "THE ENACTING TERMS — 99 articles, binding", 11, INK, MONO)
    body, y3 = cells(40, y2 + 12, 99, art_should, {22},
                     lambda i: "Article %d%s" % (i, " — contains ‘should’" if i in art_should else ""))
    parts.append(body)
    text(40, y3 + 30, "2 of 99.", 14, ACCENT, FONT, "start", "bold")
    text(88, y3 + 30, "Both in Article 47, on binding corporate rules: two requirements written in "
                      "the register of the unbound.", 12, INK)
    text(40, y3 + 48, "‘shall’ in the enacting terms: 479.", 11, GREY, MONO)

    # panel 3 -- the ladder
    y4 = y3 + 92
    text(40, y4, "RECITAL 71 — four safeguards", 11, INK, MONO)
    text(600, y4, "ARTICLE 22(3) — three", 11, INK, MONO)

    left = ["obtain human intervention",
            "express his or her point of view",
            "obtain an explanation of the decision reached",
            "challenge the decision"]
    right = ["obtain human intervention on the part of the controller",
             "express his or her point of view",
             "",
             "contest the decision"]
    for k in range(4):
        ly = y4 + 26 + k * 26
        missing = (k == 2)
        reworded = (k == 3)
        text(40, ly, "— " + left[k], 13, ACCENT if missing else INK)
        if missing:
            parts.append('<line x1="430" y1="%d" x2="560" y2="%d" stroke="%s" stroke-width="1.4" '
                         'stroke-dasharray="3 5"/>' % (ly - 4, ly - 4, ACCENT))
            text(600, ly, "— nothing", 13, ACCENT, FONT, "start", "normal", "italic")
        else:
            dash = ' stroke-dasharray="7 4"' if reworded else ""
            parts.append('<line x1="430" y1="%d" x2="560" y2="%d" stroke="%s" stroke-width="1.4"%s/>'
                         % (ly - 4, ly - 4, GREY, dash))
            text(600, ly, "— " + right[k], 13, INK)

    text(40, y4 + 140,
         "The third rung is the one the Court of Justice reached by another route: C-203/22, "
         "CK v Dun &amp; Bradstreet Austria, 27 February 2025,", 12, INK)
    text(40, y4 + 157,
         "held that Article 15(1)(h) — binding since 2016 — affords ‘a genuine right to "
         "an explanation’. The word itself is in the Regulation once,", 12, INK)
    text(40, y4 + 174,
         "in recital 71, and in no article. The fourth rung crosses under another verb: the recital "
         "says challenge, the article says contest.", 12, INK)
    text(40, y4 + 200,
         "Ulysses (the nightly line) · Session 81 · 2026-09-05 · source: EUR-Lex CELEX "
         "32016R0679, committed beside this figure", 10, GREY, MONO)

    parts.append("</svg>")
    (HERE / "figure.svg").write_text("\n".join(parts), encoding="utf-8")
    print("figure.svg written, %d bytes; height used %d of %d" % ((HERE / "figure.svg").stat().st_size, y4 + 210, H))


if __name__ == "__main__":
    main()
