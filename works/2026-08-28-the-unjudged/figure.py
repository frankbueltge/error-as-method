#!/usr/bin/env python3
"""figure.py — Session 73, 2026-08-28.

Draws figure.svg: raw SVG, stdlib only, deterministic (no randomness, so no seed).

Two panels, and the shape is deliberately not last night's.

  Above: the two paths through one institution's norm, as Kaplan-Meier survival
  curves over the post-migration cohort — the probability that an erratum still
  has no verdict t days after somebody reported it. Editorial reports and
  technical reports are the same kind of object (a difference somebody found in
  a document that cannot be changed) and they are routed to two different desks
  by a box the reporter ticks. The distance between the two curves is that box.

  Below: the 728 that have no verdict at all, one hairline each, running from the
  day it was reported to today, sorted by report date. Every line is open at the
  right-hand edge, because none of them has ended. Under the standing position
  none of them is yet an error.

Usage:
    python3 figure.py --raw ../../../.raw --out figure.svg
"""

import argparse
import datetime
import json
import os

W, H = 980, 820
T_OBS = datetime.date(2026, 8, 28)
MIGRATION = datetime.date(2019, 9, 10)
QUARANTINED = {"6534"}

INK = "#1b1b1b"
FAINT = "#9a958c"
RULE = "#c9c3b8"
TECH = "#2f4858"
EDIT = "#a33b20"
PAPER = "#faf8f4"
FONT = ("Iowan Old Style, Palatino Linotype, Palatino, Charter, "
        "Georgia, 'Times New Roman', serif")
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

# panel A
AL, AR, AT, AH = 74, 26, 74, 300
# panel B
BL, BR, BT, BH = 74, 26, 470, 268


def parse_day(text):
    try:
        return datetime.date.fromisoformat((text or "").strip()[:10])
    except ValueError:
        return None


def kaplan_meier(observations):
    obs = sorted(observations, key=lambda o: (o[0], not o[1]))
    n = len(obs)
    curve = []
    surv = 1.0
    at_risk = n
    i = 0
    while i < n:
        t = obs[i][0]
        events = censored = 0
        j = i
        while j < n and obs[j][0] == t:
            if obs[j][1]:
                events += 1
            else:
                censored += 1
            j += 1
        if events and at_risk > 0:
            surv *= 1.0 - events / at_risk
        curve.append((t, surv))
        at_risk -= events + censored
        i = j
    return curve


def frac_year(day):
    start = datetime.date(day.year, 1, 1)
    end = datetime.date(day.year + 1, 1, 1)
    return day.year + (day - start).days / (end - start).days


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(os.path.dirname(__file__), "..", "..", "..", ".raw"))
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "figure.svg"))
    args = ap.parse_args()

    with open(os.path.join(os.path.abspath(args.raw), "errata.json"), encoding="utf-8") as fh:
        errata = json.load(fh)

    cohort = {"Editorial": [], "Technical": []}
    pending = []
    for e in errata:
        eid = str(e["errata_id"])
        sub = parse_day(e.get("submit_date"))
        if sub is None or sub > T_OBS or eid in QUARANTINED:
            if e["errata_status_code"] == "Reported" and sub and sub <= T_OBS:
                pending.append((sub, e["errata_type_code"]))
            continue
        if e["errata_status_code"] == "Reported":
            pending.append((sub, e["errata_type_code"]))
        if sub >= MIGRATION:
            kind = e["errata_type_code"]
            if e["errata_status_code"] == "Reported":
                cohort[kind].append(((T_OBS - sub).days, False))
            else:
                upd = parse_day(e.get("update_date"))
                if upd is not None:
                    cohort[kind].append((max((upd - sub).days, 0), True))

    curves = {k: kaplan_meier(v) for k, v in cohort.items()}

    plot_w = W - AL - AR
    tmax = 1825

    def ax(days):
        return AL + plot_w * min(days, tmax) / tmax

    def ay(surv):
        return AT + AH * (1 - surv)

    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
               f'width="{W}" height="{H}" font-family="{FONT}">')
    out.append(f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')

    out.append(f'<text x="{AL}" y="30" font-size="17" fill="{INK}">'
               'Two paths through one norm, and the differences that took neither</text>')
    out.append(f'<text x="{AL}" y="50" font-size="12" fill="{FAINT}">'
               'RFC Editor errata, 8,021 reports against published RFCs, read 2026-08-28. '
               'Above: 2,403 reports filed since 2019-09-10, by the type the reporter marked.</text>')

    # ---- panel A frame
    out.append(f'<rect x="{AL}" y="{AT}" width="{plot_w}" height="{AH}" fill="none" '
               f'stroke="{RULE}" stroke-width="1"/>')
    for share in (0, 0.25, 0.5, 0.75, 1.0):
        y = ay(share)
        out.append(f'<line x1="{AL}" y1="{y:.1f}" x2="{AL+plot_w}" y2="{y:.1f}" '
                   f'stroke="{RULE}" stroke-width=".5"/>')
        out.append(f'<text x="{AL-8}" y="{y+4:.1f}" font-size="11" fill="{FAINT}" '
                   f'text-anchor="end" font-family="{MONO}">{share:.2f}</text>')
    for days, label in ((0, "0"), (90, "90 d"), (365, "1 yr"), (730, "2 yr"),
                        (1095, "3 yr"), (1460, "4 yr"), (1825, "5 yr")):
        x = ax(days)
        out.append(f'<line x1="{x:.1f}" y1="{AT}" x2="{x:.1f}" y2="{AT+AH}" '
                   f'stroke="{RULE}" stroke-width=".5"/>')
        out.append(f'<text x="{x:.1f}" y="{AT+AH+16}" font-size="11" fill="{FAINT}" '
                   f'text-anchor="middle" font-family="{MONO}">{label}</text>')
    out.append(f'<text x="{AL-52}" y="{AT+AH/2:.1f}" font-size="12" fill="{FAINT}" '
               f'text-anchor="middle" transform="rotate(-90 {AL-52} {AT+AH/2:.1f})">'
               'still no verdict</text>')

    # ---- the two step curves
    for kind, colour in (("Technical", TECH), ("Editorial", EDIT)):
        pts = [f"{AL:.1f},{ay(1.0):.1f}"]
        last = 1.0
        for t, surv in curves[kind]:
            if t > tmax:
                break
            pts.append(f"{ax(t):.1f},{ay(last):.1f}")
            pts.append(f"{ax(t):.1f},{ay(surv):.1f}")
            last = surv
        pts.append(f"{AL+plot_w:.1f},{ay(last):.1f}")
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{colour}" '
                   f'stroke-width="1.8"/>')

    # medians, marked where each curve crosses 0.5
    def km_median(curve):
        for t, surv in curve:
            if surv <= 0.5:
                return t
        return None

    for kind, colour, dy in (("Editorial", EDIT, -10), ("Technical", TECH, -10)):
        med = km_median(curves[kind])
        if med is None:
            continue
        x = ax(med)
        out.append(f'<line x1="{x:.1f}" y1="{ay(0.5):.1f}" x2="{x:.1f}" y2="{AT+AH}" '
                   f'stroke="{colour}" stroke-width=".8" stroke-dasharray="3 3"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{ay(0.5):.1f}" r="3.2" fill="{colour}"/>')
        out.append(f'<text x="{x+6:.1f}" y="{ay(0.5)+dy:.1f}" font-size="12" fill="{colour}">'
                   f'median {med} d</text>')

    out.append(f'<text x="{ax(420):.1f}" y="{ay(0.62):.1f}" font-size="13" fill="{TECH}">'
               'Technical — routed to the working group and its Area Directors</text>')
    out.append(f'<text x="{ax(420):.1f}" y="{ay(0.10):.1f}" font-size="13" fill="{EDIT}">'
               'Editorial — routed first to the RFC Editor</text>')
    out.append(f'<text x="{AL}" y="{AT+AH+40}" font-size="11" fill="{FAINT}" '
               f'font-family="{MONO}">'
               'Kaplan-Meier; the still-unjudged are censored at 2026-08-28. '
               'n = 887 editorial, 1,516 technical.</text>')

    # ---- panel B: the 728, one line each
    pending.sort(key=lambda p: p[0])
    y0, y1 = 2009.5, 2026.9
    bw = W - BL - BR

    def bx(f):
        return BL + bw * (f - y0) / (y1 - y0)

    out.append(f'<text x="{BL}" y="{BT-26}" font-size="15" fill="{INK}">'
               'The 728 with no verdict at all — each line runs from the day it was reported '
               'to today</text>')
    out.append(f'<text x="{BL}" y="{BT-8}" font-size="12" fill="{FAINT}">'
               '617 technical, 111 editorial. None of the lines has an end: no norm has been '
               'imposed on any of them.</text>')
    out.append(f'<rect x="{BL}" y="{BT}" width="{bw}" height="{BH}" fill="none" '
               f'stroke="{RULE}" stroke-width="1"/>')
    for year in range(2010, 2027):
        x = bx(year)
        out.append(f'<line x1="{x:.1f}" y1="{BT}" x2="{x:.1f}" y2="{BT+BH}" '
                   f'stroke="{RULE}" stroke-width=".5"/>')
        if year % 2 == 0:
            out.append(f'<text x="{x:.1f}" y="{BT+BH+16}" font-size="11" fill="{FAINT}" '
                       f'text-anchor="middle" font-family="{MONO}">{year}</text>')

    step = BH / max(len(pending), 1)
    for i, (day, kind) in enumerate(pending):
        y = BT + 1 + i * step
        x_from = bx(frac_year(day))
        x_to = bx(frac_year(T_OBS))
        colour = EDIT if kind == "Editorial" else TECH
        out.append(f'<line x1="{x_from:.1f}" y1="{y:.2f}" x2="{x_to:.1f}" y2="{y:.2f}" '
                   f'stroke="{colour}" stroke-width=".7" opacity=".75"/>')

    x_today = bx(frac_year(T_OBS))
    out.append(f'<line x1="{x_today:.1f}" y1="{BT}" x2="{x_today:.1f}" y2="{BT+BH}" '
               f'stroke="{INK}" stroke-width="1"/>')
    out.append(f'<text x="{x_today-6:.1f}" y="{BT-4:.1f}" font-size="11" fill="{INK}" '
               f'text-anchor="end" font-family="{MONO}">today</text>')

    oldest = pending[0][0]
    age_years = (T_OBS - oldest).days / 365.25
    out.append(f'<text x="{BL+8}" y="{BT+BH-10}" font-size="11" fill="{FAINT}">'
               f'the line at the top was reported {oldest.isoformat()} — '
               f'{age_years:.1f} years, still Reported</text>')

    out.append(f'<text x="{BL}" y="{H-16}" font-size="11" fill="{FAINT}" '
               f'font-family="{MONO}">'
               'sources: rfc-editor.org/errata.json and rfc-index.xml, fetched 2026-08-28; '
               'method and numbers in results.json · Session 73, Error as Method</text>')
    out.append("</svg>")

    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print(f"{len(pending)} pending lines, "
          f"{len(cohort['Editorial'])}/{len(cohort['Technical'])} cohort observations -> {args.out}")


if __name__ == "__main__":
    main()
