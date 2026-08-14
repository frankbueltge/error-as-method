#!/usr/bin/env python3
"""figure.py -- draw the register as a register.

One row per country name withdrawn from ISO 3166 since 1974, oldest first, ruled where the
IANA registry's memory floor falls. Five columns, one per place the name could still be:
the authority's own register of the dead, the two live namespaces it was evicted from or
left vacant, and the two downstream registers that had to decide what to inherit.

The form is a ledger page rather than a timeline, because the finding is not about when the
deaths happened -- it is about which column has room.

Deterministic: same results.json, same SVG. No network, no dependencies.

    python3 figure.py             -> figure.svg
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

W = 1000
BG, INK, MUTE, RULE = "#f4f1ea", "#1b1a17", "#7d766a", "#cfc7b6"
GONE = "#a8402c"
SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif"
MONO = "'IBM Plex Mono','DejaVu Sans Mono',monospace"

TOP = 150.0
ROW = 19.0
XC = [430.0, 530.0, 630.0, 760.0, 880.0]
HEADS = [
    ("ISO 3166-3", "the register of", "the dead (α-4)"),
    ("CLDR", "territory", "alias (α-2)"),
    ("BCP 47", "IANA subtag", "registry (α-2)"),
    ("ISO 3166-1", "α-2 address", "today"),
    ("ISO 3166-1", "α-3 address", "today"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=11, fill=INK, anchor="start", family=MONO, weight=None, op=None):
    w = " font-weight='%s'" % weight if weight else ""
    o = " opacity='%s'" % op if op else ""
    return ("<text x='%.1f' y='%.1f' font-size='%s' fill='%s' text-anchor='%s' "
            "font-family=\"%s\"%s%s>%s</text>" % (x, y, size, fill, anchor, family, w, o, esc(s)))


def mark(x, y, kind):
    """filled = the name is here; open = it is not; barred = the address is, someone else is in it."""
    s = 9.0
    x0, y0 = x - s / 2, y - s / 2
    if kind == "held":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='%s'/>"
                % (x0, y0, s, s, INK))
    if kind == "empty":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='none' "
                "stroke='%s' stroke-width='1'/>" % (x0, y0, s, s, RULE))
    if kind == "vacant":
        return ("<circle cx='%.1f' cy='%.1f' r='2.2' fill='none' stroke='%s' "
                "stroke-width='1'/>" % (x, y, RULE))
    if kind == "other":
        return ("<rect x='%.1f' y='%.1f' width='%.1f' height='%.1f' fill='none' stroke='%s' "
                "stroke-width='1.2'/><line x1='%.1f' y1='%.1f' x2='%.1f' y2='%.1f' stroke='%s' "
                "stroke-width='1.6'/>" % (x0, y0, s, s, GONE, x0, y0 + s, x0 + s, y0, GONE))
    raise ValueError(kind)


def main():
    res = json.load(open(os.path.join(HERE, "results.json")))
    rows = res["rows"]
    n = len(rows)
    # The floor falls between the last pre-floor row and the first post-floor one.
    split = next(i for i, r in enumerate(rows) if not r["before_floor"])
    VGAP = 26.0            # room for the floor rule to be read without sitting on a row
    H = TOP + n * ROW + VGAP + 132

    out = ["<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d' "
           "viewBox='0 0 %d %d'>" % (W, H, W, H),
           "<rect width='%d' height='%d' fill='%s'/>" % (W, H, BG)]

    out.append(text(28, 48, "The fourth letter", 24, INK, family=SERIF))
    out.append(text(28, 71, "Thirty-one country names withdrawn from ISO 3166 since 1974, and "
                            "the five places one could still be.", 12.5, MUTE, family=SERIF))
    out.append(text(28, 89, "A name survives where the addresses are cheap. Where they are "
                            "scarce it is evicted, and no policy prevents it.", 12.5, MUTE,
                    family=SERIF))

    for x, (a, b, c) in zip(XC, HEADS):
        out.append(text(x, TOP - 44, a, 10.5, INK, "middle", weight="bold"))
        out.append(text(x, TOP - 31, b, 9.5, MUTE, "middle"))
        out.append(text(x, TOP - 19, c, 9.5, MUTE, "middle"))
    out.append("<line x1='28' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1'/>"
               % (TOP - 12, W - 28, TOP - 12, INK))

    for i, r in enumerate(rows):
        y = TOP + i * ROW + 4 + (VGAP if i >= split else 0)
        if i % 2 == 0:
            out.append("<rect x='28' y='%.1f' width='%d' height='%.1f' fill='%s' "
                       "opacity='0.35'/>" % (y - 13, W - 56, ROW, "#e7e1d3"))
        out.append(text(32, y, r["alpha_4"], 11, INK, weight="bold"))
        out.append(text(88, y, r["withdrawal_date"][:4], 10.5, MUTE))
        name = r["name"]
        name = name if len(name) <= 44 else name[:43] + "…"
        out.append(text(126, y, name, 11, INK, family=SERIF))

        cells = [
            "held",                                                   # ISO 3166-3
            "held" if r["cldr_alias"] else "empty",                   # CLDR
            {"deprecated-as-itself": "held", "live-as-itself": "held",
             "address-held-by-another": "other", "absent": "empty"}[r["iana"]],
            "other" if r["alpha_2_live_now"] else "vacant",           # alpha-2 today
            "other" if r["alpha_3_live_now"] else "vacant",           # alpha-3 today
        ]
        for x, kind in zip(XC, cells):
            out.append(mark(x, y - 3.5, kind))

    # The floor.
    yf = TOP + split * ROW + VGAP / 2 - 9.0
    out.append("<line x1='28' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1.4' "
               "stroke-dasharray='5 3'/>" % (yf, W - 28, yf, INK))
    out.append(text(32, yf - 6, "ISO 3166:1988 — the edition RFC 1766 cited in 1995, and "
                                "therefore the floor of the IANA registry's memory", 9.8, INK,
                    family=SERIF))

    ly = TOP + n * ROW + VGAP + 34
    out.append("<line x1='28' y1='%.1f' x2='%d' y2='%.1f' stroke='%s' stroke-width='1'/>"
               % (ly - 26, W - 28, ly - 26, RULE))
    out.append(mark(36, ly - 4, "held"))
    out.append(text(50, ly, "the name is recorded here", 10.5, INK))
    out.append(mark(300, ly - 4, "empty"))
    out.append(text(314, ly, "it is not — and never was removed, only never entered",
                    10.5, INK))
    out.append(mark(36, ly + 20, "other"))
    out.append(text(50, ly + 24, "the address exists and another country is in it", 10.5, GONE))
    out.append(mark(300, ly + 20, "vacant"))
    out.append(text(314, ly + 24, "(last two columns) the address is still vacant — nobody has "
                    "been let in", 10.5, MUTE))
    out.append(text(28, ly + 50,
                    "Sources: ISO 3166-3 and ISO 3166-1 via the iso-codes compilation; the IANA "
                    "Language Subtag Registry, File-Date %s; CLDR territoryAlias."
                    % res["registry_file_date"], 9.8, MUTE, family=SERIF))
    out.append(text(28, ly + 65,
                    "Measured offline by measure.py from files hashed in sources/MANIFEST.json. "
                    "Ulysses (the nightly line), Session 56, 2026-08-14.", 9.8, MUTE,
                    family=SERIF))

    out.append("</svg>")
    svg = "\n".join(out) + "\n"
    with open(os.path.join(HERE, "figure.svg"), "w") as f:
        f.write(svg)
    print("figure.svg  %d bytes, %d rows, floor after row %d, canvas %dx%d"
          % (len(svg), n, split, W, H))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
