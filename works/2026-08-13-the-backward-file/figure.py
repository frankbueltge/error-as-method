#!/usr/bin/env python3
"""
Generates figure.svg from results.json. Deterministic: no randomness, no seed, no
network. Run measure.py first.

One panel and one rail, and the argument is the shape rather than the numbers.

  THE WALL. One vertical stripe per tzdata release, 1993 to 2026, its height the size
  of the identifier namespace. The lower, solid part is canonical zones; the upper,
  hatched part is compatibility links -- names the institution has itself declared
  wrong or superseded and continues to ship. The wall never gets shorter. The single
  notch is the only identifier withdrawn from the namespace since 1999.

  THE RAIL. Underneath, the same 33 years as events. A faint tick for every release:
  each one exists because the data behind the names was corrected. A tall mark for
  each of the five releases whose own NEWS reports a change to a zone name. One rust
  mark for the withdrawal. The institution corrects its data on a schedule and its
  names almost never, and never by taking one away.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))
T = R["trajectory"]

PAPER = "#eef0f1"
INK = "#14181c"
MUTE = "#6b737a"
RULE = "#b9c0c4"
ZONE = "#33424c"        # names the institution still stands behind
LINK = "#8b979e"        # names it has superseded and cannot stop shipping
RUST = "#9c3b1e"        # the one withdrawal

W, H = 1000, 700
PX, PY = 78, 74          # plot origin (left, top)
PW, PH = 862, 372        # plot size
RAIL_Y = PY + PH + 92

S = []


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def t(x, y, s, size=12.5, fill=INK, anchor="start", weight=None, style=None,
      family='"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif'):
    wt = f' font-weight="{weight}"' if weight else ""
    st = f' font-style="{style}"' if style else ""
    S.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
             f'text-anchor="{anchor}" font-family=\'{family}\'{wt}{st}>{esc(s)}</text>')


def mono(x, y, s, size=11, fill=MUTE, anchor="start"):
    t(x, y, s, size, fill, anchor,
      family='"IBM Plex Mono","DejaVu Sans Mono",monospace')


def line(x1, y1, x2, y2, stroke=RULE, sw=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    S.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
             f'stroke="{stroke}" stroke-width="{sw}"{d}/>')


def rect(x, y, w, h, fill, op=None):
    o = f' fill-opacity="{op}"' if op is not None else ""
    S.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" '
             f'fill="{fill}"{o}/>')


def year_of(d):
    return int(d[:4]) + (int(d[5:7]) - 1) / 12.0


def main():
    y0, y1 = year_of(T[0]["date"]), year_of(T[-1]["date"])
    ymax = 820.0            # headroom above the wall, so the note has somewhere to sit

    def X(yr):
        return PX + (yr - y0) / (y1 - y0) * PW

    def Y(n):
        return PY + PH - n / ymax * PH

    S.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    S.append('<defs><pattern id="acc" width="5" height="5" patternUnits="userSpaceOnUse" '
             f'patternTransform="rotate(45)"><rect width="5" height="5" fill="{PAPER}"/>'
             f'<line x1="0" y1="0" x2="0" y2="5" stroke="{LINK}" stroke-width="2.4"/>'
             '</pattern></defs>')

    # ---- titles -------------------------------------------------------------
    t(PX, 36, "The wall of names", 22)
    t(PX, 56, "Every tzdata release, 1993–2026: the identifier namespace of the "
              "IANA time zone database, and what it never puts down.", 13, MUTE)

    # ---- axes ---------------------------------------------------------------
    for n in range(0, 801, 200):
        line(PX, Y(n), PX + PW, Y(n), RULE if n else INK, 1 if n else 1.4)
        mono(PX - 9, Y(n) + 4, str(n), 10.5, MUTE, "end")
    mono(PX - 9, PY - 12, "names", 10.5, MUTE, "end")
    for yr in range(1995, 2027, 5):
        if y0 <= yr <= y1:
            mono(X(yr), PY + PH + 18, str(yr), 10.5, MUTE, "middle")

    # ---- the wall: one stripe per release ------------------------------------
    for i, r in enumerate(T):
        xa = X(year_of(r["date"]))
        xb = X(year_of(T[i + 1]["date"])) if i + 1 < len(T) else xa + 2.2
        w = max(1.7, xb - xa - 0.35)
        rect(xa, Y(r["zones"]), w, Y(0) - Y(r["zones"]), ZONE)
        rect(xa, Y(r["names"]), w, Y(r["names"]) * 0 + (Y(r["zones"]) - Y(r["names"])),
             "url(#acc)")

    # outline of the top edge, so the monotonicity is visible as a line
    pts = []
    for i, r in enumerate(T):
        xa = X(year_of(r["date"]))
        pts.append((xa, Y(r["names"])))
        if i + 1 < len(T):
            pts.append((X(year_of(T[i + 1]["date"])), Y(r["names"])))
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    S.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.3"/>')

    # ---- the one withdrawal --------------------------------------------------
    w2017 = None
    for r in T:
        if r["release"] == "tzdata2017c":
            w2017 = r
    if w2017:
        xw = X(year_of(w2017["date"]))
        line(xw, Y(w2017["names"]) - 6, xw, PY + 6, RUST, 1.4)
        S.append(f'<circle cx="{xw:.1f}" cy="{Y(w2017["names"]) - 6:.1f}" r="3" fill="{RUST}"/>')
        t(xw - 10, PY + 18, "the only withdrawal since 1999:", 11.5, RUST, "end")
        t(xw - 10, PY + 33, "Canada/East-Saskatchewan, 2017c —", 11.5, RUST, "end")
        t(xw - 10, PY + 48, "“an unused misnomer anyway”", 11.5, RUST, "end", style="italic")

    # ---- legend --------------------------------------------------------------
    lx, ly = PX + 10, PY + 18
    rect(lx, ly - 9, 13, 11, ZONE)
    t(lx + 20, ly, "%d canonical zones — the names it still stands behind"
      % R["namespace"]["live_canonical_zones"], 12.5, INK)
    rect(lx, ly + 20 - 9, 13, 11, "url(#acc)")
    t(lx + 20, ly + 20, "%d compatibility links — %.0f%% of the namespace is names it "
      "has superseded" % (R["namespace"]["live_compatibility_links"],
                          R["namespace"]["link_share_now"] * 100), 12.5, INK)

    # ---- the rail ------------------------------------------------------------
    t(PX, RAIL_Y - 44, "What it changes, and what it will not", 16)
    t(PX, RAIL_Y - 26, "One tick per release. Each exists because the data behind the "
                       "names was corrected.", 12.5, MUTE)
    line(PX, RAIL_Y, PX + PW, RAIL_Y, RULE, 1)
    for r in T:
        x = X(year_of(r["date"]))
        line(x, RAIL_Y, x, RAIL_Y - 9, MUTE, 1)

    renames = [("2016g", "Rangoon→Yangon", 0), ("2021b", "Enderbury→Kanton", 1),
               ("2021c", "", 0), ("2022b", "Kiev→Kyiv", 0), ("2017c", "", 0)]
    for rel, lab, tier in renames:
        for r in T:
            if r["release"] == "tzdata" + rel:
                x = X(year_of(r["date"]))
                top = RAIL_Y - (26 + 17 * tier)
                line(x, RAIL_Y, x, top, INK, 1.6)
                if lab:
                    t(x, top - 6, lab, 11, INK, "middle")
    if w2017:
        x = X(year_of(w2017["date"]))
        line(x, RAIL_Y, x, RAIL_Y + 22, RUST, 1.6)
        t(x, RAIL_Y + 36, "the withdrawal", 11, RUST, "middle")

    n = R["news_sections"]
    t(PX, RAIL_Y + 66,
      "%d releases in 33 years. %d of the %d whose NEWS carries section headings report a "
      "change to timestamps; %d report a change to a zone name."
      % (R["releases_measured"], n["releases_reporting_timestamp_changes"],
         n["release_blocks_with_section_headings"],
         n["releases_reporting_zone_name_changes"]), 12.5, INK)
    t(PX, RAIL_Y + 84,
      "%d identifiers have ever existed; %d were withdrawn, %d of them before 1999. "
      "RFC 6557, which governs this database, gives three criteria for adding a name and "
      "for changing"
      % (R["namespace"]["identifiers_ever"], R["withdrawals"]["total_ever"],
         R["withdrawals"]["before_2000"]), 12.5, INK)
    t(PX, RAIL_Y + 101, "what one means. It gives no procedure for removing one.",
      12.5, INK)

    mono(PX, H - 16, "data.iana.org/time-zones/releases/ · 272 releases parsed · "
                     "SHA-256 in sources/MANIFEST.json · Error as Method, 2026-08-13",
         9.5, MUTE)

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">\n' + "\n".join(S) + "\n</svg>\n")
    with open(os.path.join(HERE, "figure.svg"), "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("figure.svg written: %d releases, %d bytes" % (len(T), len(svg)))


if __name__ == "__main__":
    main()
