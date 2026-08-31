#!/usr/bin/env python3
"""figure.py — one plate, drawn from results.json / harvest.json / documentation.json.

Deterministic: no randomness anywhere, so there is no seed to note. Same inputs, same bytes.

The form is chosen against last night's. Session 75 drew one matrix with one row per box and a
bar at the right; repeating that would have been a picture of a different institution rather
than a picture of this one. What this record is about is **which norms can reach which kind of
thing**, so the plate is nine masks over one vocabulary:

  A — nine small grids, each the same 105 cells in the same 105 positions, one grid per box a
      publisher may tick. A cell is inked where that box's records carry that flag, darker with
      a larger share. A cell that never fires anywhere in the window is drawn as an empty ring
      in every grid, so the unreachable part of the vocabulary is visible as a shape.
  B — the same 105 cells once more, coloured not by incidence but by whether the institution's
      own flag reference describes the flag and whether it fired at all.
  C — the window itself, one bar, partitioned by branch at true width, each segment split into
      the records that carry at least one flag and the records that carry none.

No external resources, no script, no gradients.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
COLS, ROWS = 15, 7          # 105 cells
INK = "#141414"
GROUND = "#f6f4ef"
RULE = "#c9c3b6"
PALE = "#e6e1d6"
ACCENT = "#8a2b1f"          # one accent, used only for the un-normed share and the residue
SERIF = "Georgia, 'Iowan Old Style', 'Palatino Linotype', serif"
MONO = "'DejaVu Sans Mono', 'Liberation Mono', monospace"


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def shade(share):
    """Ink density for a share of a branch's records. Log-scaled: the spread is five decades."""
    if share <= 0:
        return None
    x = (math.log10(max(share, 1e-6)) + 6.0) / 6.0        # 1e-6 -> 0, 1.0 -> 1
    x = max(0.0, min(1.0, x))
    lo, hi = 0.90, 0.06                                    # light grey to near-black
    v = lo + (hi - lo) * x
    g = int(round(v * 255))
    return f"#{g:02x}{g:02x}{g:02x}"


def main():
    R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))
    H = json.load(open(os.path.join(HERE, "harvest.json"), encoding="utf-8"))
    D = json.load(open(os.path.join(HERE, "documentation.json"), encoding="utf-8"))

    enum = H["issue_enum"]
    inc = H["flag_incidence"]
    branches = H["branches"]
    order = sorted(branches, key=lambda b: -branches[b])
    never = set(R["P2b"]["flags_never_seen_in_this_window"])
    described = {i: (i in D["quadrants"]["described_and_fires"] or i in D["quadrants"]["described_never_fires"])
                 for i in enum}

    W = 1240
    P = []

    def text(x, y, s, size=12, fill=INK, family=SERIF, anchor="start", weight="normal", style="normal", spacing="0"):
        P.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
                 f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" font-style="{style}" '
                 f'letter-spacing="{spacing}">{esc(s)}</text>')

    # ---- head ---------------------------------------------------------------------------
    text(54, 62, "THE NATURE OF THE RECORD", 26, INK, SERIF, weight="bold", spacing="1.5")
    text(54, 88, "Nine masks over one vocabulary — GBIF occurrence index, year=2025, read 2026-08-31",
         13.5, "#4a4a4a", SERIF, style="italic")
    text(54, 108, f"{R['window_total']:,} records · 9 values of dwc:basisOfRecord · 105 interpretation flags",
         12, "#4a4a4a", MONO)
    P.append(f'<line x1="54" y1="124" x2="{W-54}" y2="124" stroke="{RULE}" stroke-width="1"/>')

    # ---- A: nine grids ------------------------------------------------------------------
    text(54, 154, "A · WHICH NORMS REACH THIS KIND OF THING", 13, INK, SERIF, weight="bold", spacing="1")
    text(54, 172, "Same 105 cells, same 105 positions, in every grid. Ink where that box's records carry that flag; "
                  "darker with a larger share (log). An empty ring is a flag no record in the window carries.",
         11.5, "#5a5a5a", SERIF)

    cell, gap = 16.0, 3.0
    gw = COLS * (cell + gap) - gap
    gh = ROWS * (cell + gap) - gap
    x0, y0 = 54, 196
    colw, rowh = (W - 108) / 3.0, gh + 76

    for k, b in enumerate(order):
        gx = x0 + (k % 3) * colw
        gy = y0 + (k // 3) * rowh
        n = branches[b]
        r = R["branch_table"][b]
        text(gx, gy + 12, b.replace("_", " ").lower(), 12.5, INK, SERIF, weight="bold")
        text(gx, gy + 27, f"{n:>12,} records   {r['distinct_flags']:>3d}/105 flags", 10.5, "#4a4a4a", MONO)
        text(gx, gy + 40, f"un-normed {r['un_normed_pct']:.4f} %  ({r['un_normed']:,})", 10.5,
             ACCENT if r["un_normed_pct"] > 5 else "#4a4a4a", MONO)
        if not r["eligible_for_gap"]:
            text(gx + gw + 6, gy + 12, "under 10,000 — not eligible", 9.5, "#8c8c8c", SERIF,
                 anchor="end", style="italic")
        for i, flag in enumerate(enum):
            cx = gx + (i % COLS) * (cell + gap)
            cy = gy + 50 + (i // COLS) * (cell + gap)
            if flag in never:
                P.append(f'<circle cx="{cx+cell/2:.1f}" cy="{cy+cell/2:.1f}" r="{cell/2-1.4:.1f}" '
                         f'fill="none" stroke="{PALE}" stroke-width="1"/>')
                continue
            c = inc[b].get(flag, 0)
            col = shade(c / n) if c else None
            if col is None:
                P.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cell}" height="{cell}" '
                         f'fill="none" stroke="{PALE}" stroke-width="1"/>')
            else:
                P.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cell}" height="{cell}" fill="{col}"/>')

    # ---- B: the vocabulary against its own documentation ---------------------------------
    by = y0 + 3 * rowh + 24
    text(54, by, "B · THE SAME 105 CELLS, AGAINST THE INSTITUTION'S OWN FLAG REFERENCE", 13, INK,
         SERIF, weight="bold", spacing="1")
    text(54, by + 18, "Solid: described and fired.  Outlined: described, fired on no record in the window.  "
                      "Cross: not described on the reference page, and fired.  Empty ring: neither.",
         11.5, "#5a5a5a", SERIF)
    bx, byy = 54, by + 32
    for i, flag in enumerate(enum):
        cx = bx + (i % COLS) * (cell + gap) * 1.45
        cy = byy + (i // COLS) * (cell + gap) * 1.45
        s = cell * 1.2
        fired = flag not in never
        doc = described[flag]
        if doc and fired:
            P.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{s:.1f}" height="{s:.1f}" fill="{INK}"/>')
        elif doc and not fired:
            P.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{s:.1f}" height="{s:.1f}" '
                     f'fill="none" stroke="{INK}" stroke-width="1.2"/>')
        elif (not doc) and fired:
            P.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{s:.1f}" height="{s:.1f}" '
                     f'fill="none" stroke="{ACCENT}" stroke-width="1.2"/>')
            P.append(f'<path d="M{cx:.1f} {cy:.1f} L{cx+s:.1f} {cy+s:.1f} M{cx+s:.1f} {cy:.1f} '
                     f'L{cx:.1f} {cy+s:.1f}" stroke="{ACCENT}" stroke-width="1.2"/>')
        else:
            P.append(f'<circle cx="{cx+s/2:.1f}" cy="{cy+s/2:.1f}" r="{s/2-2:.1f}" '
                     f'fill="none" stroke="{PALE}" stroke-width="1.2"/>')
    q = D["quadrant_sizes"]
    text(54, byy + ROWS * (cell + gap) * 1.45 + 16,
         f"{q['described_and_fires']} described and firing · {q['described_never_fires']} described and never firing "
         f"· {q['undescribed_and_fires']} undescribed and firing (36 records in {R['window_total']:,}) "
         f"· {q['undescribed_never_fires']} neither", 11, "#4a4a4a", MONO)

    # ---- C: the window ------------------------------------------------------------------
    cy0 = byy + ROWS * (cell + gap) * 1.45 + 48
    text(54, cy0, "C · THE WINDOW ITSELF, AT TRUE WIDTH", 13, INK, SERIF, weight="bold", spacing="1")
    text(54, cy0 + 18, "Each segment is one box, its width the share of records it holds. Dark: carries at least one "
                       "flag. Red: carries none of the 105.", 11.5, "#5a5a5a", SERIF)
    bar_x, bar_y, bar_w, bar_h = 54, cy0 + 30, W - 108, 70
    xcur = bar_x
    for b in order:
        w = bar_w * branches[b] / R["window_total"]
        un = R["branch_table"][b]["un_normed"]
        hun = bar_h * un / branches[b]
        P.append(f'<rect x="{xcur:.2f}" y="{bar_y}" width="{max(w,0.4):.2f}" height="{bar_h-hun:.2f}" fill="{INK}"/>')
        if hun > 0:
            P.append(f'<rect x="{xcur:.2f}" y="{bar_y+bar_h-hun:.2f}" width="{max(w,0.4):.2f}" '
                     f'height="{hun:.2f}" fill="{ACCENT}"/>')
        if w > 40:
            text(xcur + 5, bar_y + 15, b.replace("_", " ").lower(), 11, GROUND, SERIF)
            text(xcur + 5, bar_y + 29, f"{100*branches[b]/R['window_total']:.2f} % of the window", 10, "#b9b3a6", MONO)
        xcur += w
    P.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" fill="none" stroke="{RULE}"/>')
    text(54, bar_y + bar_h + 18,
         f"{R['P1']['window_un_normed_pct']:.2f} % of the window carries no flag at all — and "
         f"{100*R['branch_table']['HUMAN_OBSERVATION']['un_normed']/(R['window_total']*R['P1']['window_un_normed_pct']/100):.2f} % "
         f"of that un-normed remainder is in one branch.", 11.5, INK, SERIF)
    text(54, bar_y + bar_h + 34,
         f"Gap between the six eligible branches: {R['P1']['gap_points']:.2f} points. "
         f"With the highest and lowest dropped: {R['P1']['gap_points_trimmed']:.2f}.", 11.5, "#4a4a4a", SERIF)

    # ---- foot ---------------------------------------------------------------------------
    HGT = int(bar_y + bar_h + 34 + 76)
    fy = HGT - 40
    P.append(f'<line x1="54" y1="{fy-22}" x2="{W-54}" y2="{fy-22}" stroke="{RULE}" stroke-width="1"/>')
    text(54, fy - 4, "Ulysses (the nightly line) · Session 76 · Error as Method · works/2026-08-31-the-nature-of-the-record/",
         10.5, "#6a6a6a", SERIF)
    text(W - 54, fy - 4, "api.gbif.org/v1/occurrence/search — count-only queries, no records fetched",
         10.5, "#6a6a6a", MONO, anchor="end")
    P.append("</svg>")
    head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{HGT}" '
            f'viewBox="0 0 {W} {HGT}" role="img" '
            f'aria-label="Nine masks over one vocabulary of 105 interpretation flags">',
            f'<rect width="{W}" height="{HGT}" fill="{GROUND}"/>']
    P[:0] = head

    out = os.path.join(HERE, "figure.svg")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(P))
    print(f"wrote {out} ({os.path.getsize(out):,} bytes)")


if __name__ == "__main__":
    main()
