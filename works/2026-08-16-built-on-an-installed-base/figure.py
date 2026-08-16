#!/usr/bin/env python3
"""
figure.py -- Session 59. Draws figure.svg from results.json and register.json.
Deterministic: no randomness, no clock, same input same bytes.

One job. Each lane is a word this line's argument rests on. The rule runs from the
year the field named the word to the day this practice first wrote it, so the length
of the rule is the interval during which the word already existed and this practice
was not reading it. The marker at the right-hand end says what the practice did on
arrival: cited the owner, cited nobody, or -- in one lane -- cited the owner and then
later claimed the word as its own.

Four lanes have no marker. Those are words the field owns for claims this line has
reached anyway, in its own vocabulary, having never once written the field's word.
Their rules run off the right-hand edge, because the interval has not ended.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))
REG = json.load(open(os.path.join(HERE, "register.json"), encoding="utf-8"))
FIELD = {t["term"]: t["field"] for t in REG["terms"]}
NOTE = {t["term"]: t for t in REG["terms"]}

X0, X1 = 1982.0, 2028.0
# Layout note. The first draft put every annotation immediately right of its marker.
# Rendered, the right-hand labels ran off the page and the "never written here" note
# sat on top of the owner's name. Annotations now live in one right-aligned column and
# owner labels flip anchor near the right edge. Recorded because the fault was only
# visible once the thing was rendered and looked at.
L, RGT, TOP, LANE = 214, 60, 120, 54
ANNO = 1120 - 60           # right-aligned annotation column
ROWS = [r for r in RES["terms"]]
W, H = 1120, TOP + len(ROWS) * LANE + 108

INK, MUTE, RULE, PAPER = "#1b1b18", "#6f6a5e", "#b9b5ab", "#f4f1e8"
HOT = "#8c2f14"          # the uncredited and the miscredited
COOL = "#2f4858"         # the credited


def x(year):
    return L + (year - X0) / (X1 - X0) * (W - L - RGT)


def yr(datestr):
    p = str(datestr).split("-")
    y = float(p[0])
    if len(p) >= 2:
        y += (int(p[1]) - 1) / 12.0
    if len(p) >= 3:
        y += (int(p[2]) - 1) / 365.0
    return y


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace("'", "&#39;"))


o = []
a = o.append
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
  f'viewBox="0 0 {W} {H}" font-family="Iowan Old Style, Palatino Linotype, '
  f'Palatino, Georgia, serif">')
a(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
a(f'<text x="36" y="38" font-size="20" fill="{INK}">How old each word already was '
  f'when this practice first wrote it</text>')
a(f'<text x="36" y="60" font-size="12.5" fill="{MUTE}">'
  f'{RES["corpus"]["files"]} markdown files, {RES["corpus"]["earliest"]} to '
  f'{RES["corpus"]["latest"]} &#183; rule = the interval the word existed unread here '
  f'&#183; marker = what this practice did on arrival</text>')

# decade grid
for d in range(1990, 2030, 10):
    a(f'<line x1="{x(d):.1f}" y1="{TOP - 22}" x2="{x(d):.1f}" y2="{TOP + len(ROWS)*LANE - 18}" '
      f'stroke="{RULE}" stroke-width="0.6"/>')
    a(f'<text x="{x(d):.1f}" y="{TOP - 30}" font-size="11.5" fill="{MUTE}" '
      f'text-anchor="middle">{d}</text>')

for i, r in enumerate(ROWS):
    y = TOP + i * LANE
    f = FIELD[r["term"]]
    fu = r["first_use"]
    verdict = r["verdict"]
    hot = verdict in ("field-owned-uncredited", "credited-then-miscredited")
    col = HOT if hot else COOL

    a(f'<text x="{L - 14}" y="{y + 4}" font-size="14" fill="{INK}" '
      f'text-anchor="end">{esc(r["term"])}</text>')

    fy = yr(f.get("date") or f["year"]) if f.get("year") else None

    def anno(text, colour=MUTE):
        a(f'<text x="{ANNO}" y="{y + 19}" font-size="11" fill="{colour}" '
          f'text-anchor="end">{text}</text>')

    if fy is None:
        a(f'<text x="{L}" y="{y + 4}" font-size="11.5" fill="{MUTE}">'
          f'no field year established</text>')
        if fu:
            a(f'<circle cx="{x(yr(fu["date"])):.1f}" cy="{y}" r="4" fill="none" '
              f'stroke="{MUTE}" stroke-width="1.4"/>')
        anno("not adjudicated &#8212; carried as unknown, not as novel")
        continue

    a(f'<circle cx="{x(fy):.1f}" cy="{y}" r="3.2" fill="{MUTE}"/>')
    owner = (f.get("owner") or "").split(" and ")[0]
    if owner.startswith("read out of"):
        owner = "this line's own synthesis"
    if x(fy) > W * 0.60:
        a(f'<text x="{x(fy) - 8:.1f}" y="{y - 12}" font-size="11" fill="{MUTE}" '
          f'text-anchor="end">{esc(owner)}, {f["year"]}</text>')
    else:
        a(f'<text x="{x(fy):.1f}" y="{y - 12}" font-size="11" fill="{MUTE}">'
          f'{esc(owner)}, {f["year"]}</text>')

    if fu:
        fx = x(yr(fu["date"]))
        dash = ' stroke-dasharray="4 3"' if verdict == "sense-collision" else ""
        wdt = 3.4 if hot else 1.3
        a(f'<line x1="{x(fy):.1f}" y1="{y}" x2="{fx:.1f}" y2="{y}" stroke="{col}" '
          f'stroke-width="{wdt}"{dash}/>')
        age = r["years_old_when_first_written_here"]
        if verdict == "credited-then-miscredited":
            a(f'<rect x="{fx-5:.1f}" y="{y-5}" width="10" height="10" fill="{HOT}"/>')
            a(f'<line x1="{fx:.1f}" y1="{y}" x2="{fx+26:.1f}" y2="{y}" stroke="{HOT}" '
              f'stroke-width="1" stroke-dasharray="2 2"/>')
            a(f'<circle cx="{fx+26:.1f}" cy="{y}" r="4.5" fill="none" stroke="{HOT}" '
              f'stroke-width="1.6"/>')
            anno("cited by name on session 2 &#183; claimed as this project&#39;s own "
                 "coinage on session 26", HOT)
        elif verdict == "field-owned-uncredited":
            a(f'<rect x="{fx-5:.1f}" y="{y-5}" width="10" height="10" fill="{HOT}"/>')
            anno(f"{age} years old on arrival &#183; nobody named in the file that "
                 f"first writes it", HOT)
        elif verdict == "sense-collision":
            a(f'<path d="M{fx:.1f},{y-6} L{fx+6:.1f},{y} L{fx:.1f},{y+6} '
              f'L{fx-6:.1f},{y} Z" fill="{PAPER}" stroke="{COOL}" stroke-width="1.6"/>')
            anno("same word, different sense &#8212; a homonym, not a loan")
        else:
            a(f'<circle cx="{fx:.1f}" cy="{y}" r="5" fill="{PAPER}" stroke="{COOL}" '
              f'stroke-width="1.8"/>')
            anno("owner named in the same file &#8212; this is what crediting looks like")
    else:
        a(f'<line x1="{x(fy):.1f}" y1="{y}" x2="{ANNO:.1f}" y2="{y}" stroke="{MUTE}" '
          f'stroke-width="1" stroke-dasharray="3 4"/>')
        anno("never written here &#8212; the claim arrived without the word")

# footer
fy2 = TOP + len(ROWS) * LANE + 26
a(f'<line x1="36" y1="{fy2-16}" x2="{W-36}" y2="{fy2-16}" stroke="{RULE}" stroke-width="0.7"/>')
a(f'<text x="36" y="{fy2+4}" font-size="11.5" fill="{MUTE}">'
  f'Measured by audit.py off journal/ and works/, excluding everything dated 2026-08-16 and '
  f'works/INDEX.md, a catalogue of the corpus rather than part of it. Field dates sourced in '
  f'register.json.</text>')
a(f'<text x="36" y="{fy2+22}" font-size="11.5" fill="{MUTE}">'
  f'The credit test is generous: it passes if the owner&#39;s name appears anywhere in the '
  f'file that first writes the word. Every failure it reports is a floor.</text>')
a(f'<text x="36" y="{fy2+44}" font-size="12.5" fill="{INK}">'
  f'&#8220;Infrastructure does not grow de novo; it wrestles with the inertia of the '
  f'installed base and inherits strengths and limitations from that base.&#8221; '
  f'&#8212; Star, 1999</text>')
a('</svg>')

open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8").write("\n".join(o))
print(f"figure.svg written: {W}x{H}, {len(ROWS)} lanes")
