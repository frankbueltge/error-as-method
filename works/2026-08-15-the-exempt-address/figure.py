#!/usr/bin/env python3
"""
figure.py -- Session 57. Draws figure.svg from results.json plus the dated events
declared below. Deterministic: no randomness, no clock, same input same bytes.

The figure has one job. Five two-letter addresses, one namespace, one scarcity.
The heavy bar is the interval during which the DNS root zone served an address
whose country ISO had already withdrawn -- service that IANA's own eligibility
rule does not authorise. Three lanes have no heavy bar at all, because their
countries died before the DNS could point at them. One heavy bar stops. One
does not, and runs off the right-hand edge of the drawing.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "results.json")))

X0, X1 = 1970.0, 2032.0          # year span of the drawing
L, RGT, TOP, LANE = 132, 44, 104, 78
W, H = 1080, TOP + 5 * LANE + 118

def x(year):
    return L + (year - X0) / (X1 - X0) * (W - L - RGT)

def yr(datestr):
    """'1993-03-29' -> 1993.24 ; '1975' -> 1975.0"""
    p = datestr.split("-")
    y = float(p[0])
    if len(p) >= 2:
        y += (int(p[1]) - 1) / 12.0
    if len(p) >= 3:
        y += (int(p[2]) - 1) / 365.0
    return y

# Lane data. Every date here is measured in results.json or cited in work.md.
def iana(addr):
    for e in R["natural_experiment"]:
        if e["address"] == addr:
            return e["iana_record"]["registration_date"]
    return None

LANES = [
    dict(code="SK", dead="Sikkim", withdrawn="1975",
         delegated=iana("SK"), tenant="Slovakia", ineligible=None),
    dict(code="AI", dead="French Afars and Issas", withdrawn="1977",
         delegated=iana("AI"), tenant="Anguilla", ineligible=None),
    dict(code="GE", dead="Gilbert and Ellice Islands", withdrawn="1979",
         delegated=iana("GE"), tenant="Georgia", ineligible=None),
    # .yu: delegated 1989 per the IANA removal report; ISO withdrew YU 2003-07-23;
    # delegation removed from the root zone 2010-04-01.
    dict(code="YU", dead="Yugoslavia", withdrawn="2003-07-23",
         delegated="1989", tenant=None, ineligible=("2003-07-23", "2010-04-01"),
         removed="2010-04-01"),
    dict(code="SU", dead="USSR", withdrawn="1992-08-30",
         delegated=iana("SU"), tenant=None, ineligible=("1992-08-30", "2026-08-15"),
         reclassified="2008-06"),
]

INK   = "#1b1b18"
FAINT = "#b9b5ab"
RULE  = "#6f6a5e"
PAPER = "#f4f1e8"

o = []
o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
         'viewBox="0 0 %d %d" font-family="Iowan Old Style, Palatino Linotype, '
         'Palatino, Georgia, serif">' % (W, H, W, H))
o.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, PAPER))

o.append('<text x="%d" y="34" font-size="19" fill="%s">Five addresses in one '
         'namespace, and how long each served a country that had stopped '
         'existing</text>' % (L - 96, INK))
o.append('<text x="%d" y="55" font-size="12.5" fill="%s">Root zone serial %s '
         '&#183; 248 two-letter delegations &#183; scarcity identical for all five '
         '&#183; heavy bar = service ISO 3166-1 eligibility does not '
         'authorise</text>' % (L - 96, RULE, R["root_zone"]["soa_serial"]))

# decade grid
for d in range(1970, 2031, 10):
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
             'stroke-width="0.7"/>' % (x(d), TOP - 16, x(d), TOP + 5 * LANE - 22, FAINT))
    o.append('<text x="%.1f" y="%d" font-size="11.5" fill="%s" '
             'text-anchor="middle">%d</text>' % (x(d), TOP + 5 * LANE + 2, RULE, d))

for i, ln in enumerate(LANES):
    y = TOP + i * LANE
    o.append('<text x="14" y="%d" font-size="20" fill="%s" '
             'letter-spacing="1.5">%s</text>' % (y + 6, INK, ln["code"]))
    o.append('<text x="14" y="%d" font-size="11" fill="%s">%s</text>'
             % (y + 22, RULE, ln["dead"][:26]))

    # baseline
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
             'stroke-width="0.9"/>' % (x(X0), y, x(X1), y, FAINT))

    # the country's ISO withdrawal
    wx = x(yr(ln["withdrawn"]))
    o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
             'stroke-width="1.6"/>' % (wx, y - 15, wx, y + 15, INK))
    o.append('<text x="%.1f" y="%d" font-size="10.5" fill="%s" '
             'text-anchor="middle">withdrawn %s</text>'
             % (wx, y - 21, INK, ln["withdrawn"][:4]))

    # the heavy bar: delegated while ineligible
    if ln["ineligible"]:
        a, b = x(yr(ln["ineligible"][0])), x(yr(ln["ineligible"][1]))
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="13" fill="%s"/>'
                 % (a, y - 6, b - a, INK))
        span = yr(ln["ineligible"][1]) - yr(ln["ineligible"][0])
        yrs, mons = int(span), int(round((span - int(span)) * 12))
        if mons == 12:                      # 33y 12m is not a duration
            yrs, mons = yrs + 1, 0
        dur = "%d years" % yrs if mons == 0 else "%d years %d months" % (yrs, mons)
        if ln["code"] == "SU":
            for k in range(7):                       # runs off the edge
                o.append('<rect x="%.1f" y="%d" width="7" height="13" fill="%s" '
                         'opacity="%.2f"/>' % (b + 3 + k * 11, y - 6, INK,
                                               0.82 - k * 0.11))
            o.append('<text x="%.1f" y="%d" font-size="11.5" fill="%s">%s, and '
                     'still served</text>' % (a + 8, y + 27, INK, dur))
        else:
            o.append('<text x="%.1f" y="%d" font-size="11.5" fill="%s">%s, then '
                     'removed</text>' % (a + 6, y + 27, INK, dur))
    else:
        o.append('<text x="%.1f" y="%d" font-size="11" fill="%s">no DNS to point '
                 'at it &#8212; address re-let without overlap</text>'
                 % (wx + 10, y + 24, RULE))

    # the address changing hands, or not
    if ln["delegated"]:
        dx = x(yr(ln["delegated"]))
        o.append('<circle cx="%.1f" cy="%d" r="5.5" fill="%s" stroke="%s" '
                 'stroke-width="1.6"/>' % (dx, y, PAPER, INK))
        label = (".%s delegated to %s" % (ln["code"].lower(), ln["tenant"])
                 if ln["tenant"] else ".%s delegated" % ln["code"].lower())
        anchor = "end" if ln["code"] in ("YU", "SU") else "start"
        off = -11 if anchor == "end" else 11
        o.append('<text x="%.1f" y="%d" font-size="10.5" fill="%s" '
                 'text-anchor="%s">%s</text>' % (dx + off, y - 12, RULE, anchor, label))

    if ln.get("removed"):
        rx = x(yr(ln["removed"]))
        o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
                 'stroke-width="2.6"/>' % (rx, y - 13, rx, y + 13, INK))
        o.append('<text x="%.1f" y="%d" font-size="10.5" fill="%s">removed '
                 '%s</text>' % (rx + 8, y - 12, INK, ln["removed"]))

    if ln.get("reclassified"):
        cx = x(yr(ln["reclassified"]))
        o.append('<circle cx="%.1f" cy="%d" r="4" fill="%s"/>' % (cx, y, PAPER))
        o.append('<circle cx="%.1f" cy="%d" r="4" fill="none" stroke="%s" '
                 'stroke-width="1.5"/>' % (cx, y, PAPER))
        o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" '
                 'stroke-width="1.2" stroke-dasharray="2 2"/>'
                 % (cx, y + 8, cx, y + 34, INK))
        o.append('<text x="%.1f" y="%d" font-size="10.5" fill="%s" '
                 'text-anchor="middle">June 2008: ISO moves this address out of the</text>'
                 % (cx, y + 47, INK))
        o.append('<text x="%.1f" y="%d" font-size="10.5" fill="%s" '
                 'text-anchor="middle">re-lettable pool, at the registry\'s own request</text>'
                 % (cx, y + 59, INK))

foot = ("Sources: DNS root zone, serial %s. ISO 3166-1 / 3166-3 via the iso-codes "
        "compilation. Delegation dates from the IANA root zone database. "
        "YU dates from IANA's removal report, 1 April 2010." % R["root_zone"]["soa_serial"])
o.append('<text x="14" y="%d" font-size="10.5" fill="%s">%s</text>' % (H - 26, RULE, foot))
o.append('<text x="14" y="%d" font-size="10.5" fill="%s">Error as Method &#183; '
         'Session 57 &#183; 2026-08-15 &#183; works/2026-08-15-the-exempt-address/</text>'
         % (H - 11, RULE))
o.append("</svg>")

out = os.path.join(HERE, "figure.svg")
with open(out, "w") as fh:
    fh.write("\n".join(o) + "\n")
print("wrote figure.svg (%d bytes, %d elements)"
      % (os.path.getsize(out), len(o)))
