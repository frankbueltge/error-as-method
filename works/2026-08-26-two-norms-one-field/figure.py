#!/usr/bin/env python3
"""figure.py — Session 71, 2026-08-26.

Draws figure.svg: one continuous timeline, raw SVG, no library, no randomness
and therefore no seed. Deterministic — same inputs, same bytes.

The form is deliberately not last night's. Session 70 drew three panels of
counts. This draws one thing: **how long each value in this field spent being
false.**

Every (setting, Changed) pair in Go's GODEBUG table is one horizontal segment.
It starts the moment that value first appears anywhere in the record — review,
commit or release — and ends the moment the release it names is actually tagged.
For that whole segment the field holds a statement about a release that has not
happened, in a field whose own comment is in the past tense.

The release tags are vertical rules. Almost every segment ends exactly on one:
a value is written during a cycle and comes true when that cycle ships. The comb
is the norm. What the figure is for is the segment that does not end — the one
still running at the right edge, with no rule to land on.

Usage:
    python3 figure.py
"""

import datetime as dt
import json
import os

from forecasts import WHEN, ts, when_of
from measure import parse_table

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GRIDS = os.path.join(REPO, "works", "2026-08-25-under-the-commit", "grids.json")

W, H = 1240, 830
L, R, T, B = 268, 52, 118, 96
TODAY = dt.datetime(2026, 8, 26)

INK = "#171614"
FAINT = "#c9c4bb"
RULE = "#8d867a"
OPEN = "#a8321e"
PAPER = "#f4f1ea"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def main():
    grids = json.load(open(GRIDS))
    fc = json.load(open(os.path.join(HERE, "forecasts.json")))
    dates = {int(k): v for k, v in fc["release_dates"].items()}
    parsed = {b: parse_table(t) for b, t in grids["blobs"].items()}

    # First and last moment each (name, Changed) value appears anywhere in the
    # record. Both are needed: a value's span of being false ends either when
    # its release ships or when the value itself is deleted, whichever comes
    # first. Drawing to the right edge in the second case would show a value
    # that lived nineteen hours as a three-year standing falsehood.
    first, last = {}, {}
    for p in grids["points"]:
        w = when_of(p)
        if w is None or p["grid"] not in WHEN:
            continue
        for info in parsed[p["blob"]]["All"]:
            ch = info.get("Changed", 0)
            if not isinstance(ch, int) or ch == 0:
                continue
            k = (info.get("Name"), ch)
            if k not in first or w < first[k]:
                first[k] = w
            if k not in last or w > last[k]:
                last[k] = w

    live = {(e["name"], e["changed"]) for e in fc["master_tonight"]["all"]
            if e["changed"]}

    rows = []
    for k, start in first.items():
        name, ch = k
        rel = dates.get(ch)
        reldate = ts(rel) if rel else None
        # Three cases, and the deletion question is asked ONLY where it has to
        # be. A value whose named release has shipped stopped being false on
        # that day, whatever later became of the value; drawing to its last
        # appearance instead would confuse "the release arrived" with "somebody
        # edited the line". A value whose named release does NOT exist has never
        # stopped being false, so the only honest right-hand end is the last
        # moment it was in the record at all — or an open arrow if it is in
        # master tonight.
        if reldate is not None and reldate > start:
            fate, end = "came true", reldate
        elif reldate is not None:
            fate, end = "true when written", start
        elif k in live:
            fate, end = "still false", None
        else:
            fate, end = "gone, never true", last[k]
        rows.append({"name": name, "changed": ch, "start": start,
                     "end": end, "fate": fate})
    rows.sort(key=lambda r: (r["start"], r["name"]))

    lo = min(r["start"] for r in rows)
    hi = TODAY + dt.timedelta(days=210)          # room past the right edge
    span = (hi - lo).total_seconds()

    def x(d):
        return L + (W - L - R) * ((d - lo).total_seconds() / span)

    step = (H - T - B) / max(1, len(rows) - 1)

    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
      f'viewBox="0 0 {W} {H}" font-family="Iowan Old Style, Palatino, '
      f'Georgia, serif">')
    a(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

    a(f'<text x="{28}" y="34" font-size="17" fill="{INK}">'
      f'How long each value in one field spent being false</text>')
    a(f'<text x="{28}" y="55" font-size="11.5" fill="{RULE}">'
      f'src/internal/godebugs/table.go &#183; every (setting, Changed) pair, '
      f'from its first appearance in the record to the day the release it '
      f'names was tagged</text>')
    a(f'<text x="{28}" y="71" font-size="11.5" fill="{RULE}">'
      f'{len(rows)} values &#183; 840 review states, 94 commits, 78 releases '
      f'&#183; measured 2026-08-26</text>')

    # release rules
    for n in sorted(dates):
        if not dates[n]:
            continue
        d = ts(dates[n])
        if d < lo or d > hi:
            continue
        xx = x(d)
        a(f'<line x1="{xx:.1f}" y1="{T-30}" x2="{xx:.1f}" y2="{H-B+10}" '
          f'stroke="{FAINT}" stroke-width="1"/>')
        a(f'<text x="{xx:.1f}" y="{T-36}" font-size="10.5" fill="{RULE}" '
          f'text-anchor="middle">go1.{n}</text>')
        a(f'<text x="{xx:.1f}" y="{H-B+24}" font-size="9.5" fill="{RULE}" '
          f'text-anchor="middle">{dates[n][:10]}</text>')

    # today
    xt = x(TODAY)
    a(f'<line x1="{xt:.1f}" y1="{T-30}" x2="{xt:.1f}" y2="{H-B+10}" '
      f'stroke="{RULE}" stroke-width="1" stroke-dasharray="2 3"/>')
    a(f'<text x="{xt+5:.1f}" y="{T-50}" font-size="10.5" fill="{RULE}">'
      f'tonight</text>')

    for i, r in enumerate(rows):
        y = T + i * step
        x0 = x(r["start"])
        x1 = x(r["end"]) if r["end"] else x(hi) - 6
        red = r["fate"] in ("still false", "gone, never true")
        col = OPEN if red else INK
        wid = 2.6 if red else 1.5
        a(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" '
          f'stroke="{col}" stroke-width="{wid}"/>')
        a(f'<circle cx="{x0:.1f}" cy="{y:.1f}" r="2.1" fill="{col}"/>')
        if r["fate"] == "still false":
            a(f'<polygon points="{x1:.1f},{y-4:.1f} {x1+7:.1f},{y:.1f} '
              f'{x1:.1f},{y+4:.1f}" fill="{col}"/>')
        elif r["fate"] == "gone, never true":
            a(f'<line x1="{x1-3:.1f}" y1="{y-3:.1f}" x2="{x1+3:.1f}" '
              f'y2="{y+3:.1f}" stroke="{col}" stroke-width="1.4"/>')
            a(f'<line x1="{x1-3:.1f}" y1="{y+3:.1f}" x2="{x1+3:.1f}" '
              f'y2="{y-3:.1f}" stroke="{col}" stroke-width="1.4"/>')
        lab = esc(r["name"]) + ' &#8594; 1.' + str(r["changed"])
        a(f'<text x="{L-9}" y="{y+3.2:.1f}" font-size="9.6" '
          f'fill="{col}" text-anchor="end" '
          f'font-family="Courier New, monospace">{lab}</text>')

    op = [r for r in rows if r["fate"] == "still false"]
    if op:
        r = op[0]
        yy = T + rows.index(r) * step
        a(f'<text x="{x(r["start"])-16:.1f}" y="{yy-9:.1f}" font-size="10.5" '
          f'fill="{OPEN}" text-anchor="end">'
          f'still false tonight &#183; go1.{r["changed"]} does not exist, and '
          f'master carries this value now</text>')

    a(f'<text x="{28}" y="{H-30}" font-size="10.5" fill="{RULE}">'
      f'Black: the release this value names has since happened &#8212; the '
      f'segment is the wait, not the value\u2019s life. '
      f'Red &#215;: left the record while its release still did not exist. '
      f'Red arrow: still false, and in master tonight. '
      f'No shipped release has ever carried a red segment; master carries one.'
      f'</text>')
    a(f'<text x="{28}" y="{H-14}" font-size="10.5" fill="{RULE}">'
      f'Ulysses (the nightly line), Session 71 &#183; '
      f'works/2026-08-26-two-norms-one-field/</text>')
    a("</svg>")

    out = os.path.join(HERE, "figure.svg")
    with open(out, "w") as f:
        f.write("\n".join(o) + "\n")
    import collections
    tally = collections.Counter(r["fate"] for r in rows)
    print(f"wrote figure.svg: {len(rows)} values")
    for k, v in sorted(tally.items()):
        print(f"  {k:22s} {v}")
    for r in rows:
        if r["fate"] != "came true":
            print(f"    {r['fate']:22s} {r['name']} -> 1.{r['changed']} "
                  f"(from {r['start'].date()})")


if __name__ == "__main__":
    main()
