"""The river's own tool: answers the five questions R1-R5 directly from series.json, without the
ear. Written and committed before the material, so its thresholds cannot be set at a picture's
edge (Session 109's F-180). Each yes/no question has a margin: between the two bars the answer is
'undecided' and the cell is scored as neither right nor wrong.

  python3 home.py   ->  home.json
"""
import json
from statistics import median


def acf(x, lag):
    m = sum(x) / len(x); v = sum((a - m) ** 2 for a in x)
    return sum((x[i] - m) * (x[i + lag] - m) for i in range(len(x) - lag)) / v


def ranks(x):
    o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]:
            j += 1
        for t in range(i, j + 1):
            r[o[t]] = (i + j) / 2
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b); ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den


def yesno(v, yes, no):
    return "yes" if v >= yes else "no" if v <= no else "undecided"


s = json.load(open("series.json")); q = s["q"]
from adapt import daymean
h = [a - b for a, b in zip(q, daymean(q))]
days = [q[i:i + 96] for i in range(0, len(q) - len(q) % 96, 96)]
dmean = [sum(d) / len(d) for d in days]; drange = [max(d) - min(d) for d in days]
months = {"April": (0, 30), "May": (30, 61), "June": (61, 91), "July": (91, 122)}
mmean = {k: sum(dmean[a:b]) / (b - a) for k, (a, b) in months.items()}

r1 = acf(h, 96)
r3 = spearman(dmean, drange)
ratios = []
for i, r in enumerate(drange):
    nb = [drange[j] for j in range(max(0, i - 7), min(len(drange), i + 8)) if j != i]
    ratios.append(r / median(nb))
r4 = max(ratios)
# local clock (PDT for the whole record): the 15-minute slot of each day's maximum, as an hour
hours = [0] * 24
for d in days:
    hours[d.index(max(d)) // 4] += 1
out = {
    "R1_day": {"acf_lag96_of_day_only": round(r1, 3), "bars": "yes >= 0.4, no <= 0.2", "answer": yesno(r1, 0.4, 0.2)},
    "R2_season": {"monthly_mean_cfs": {k: round(v, 1) for k, v in mmean.items()},
                  "answer": max(mmean, key=mmean.get)},
    "R3_coupling": {"spearman_daily_mean_vs_daily_range": round(r3, 3), "bars": "yes >= 0.5, no <= 0.2",
                    "answer": yesno(r3, 0.5, 0.2)},
    "R4_irregular": {"max_range_over_fortnight_median": round(r4, 2),
                     "day": s["first"][:10] + " + " + str(ratios.index(r4)) + " days",
                     "days_at_or_above_3": sum(1 for r in ratios if r >= 3),
                     "bars": "yes >= 3, no <= 2", "answer": yesno(r4, 3, 2)},
    "R5_peak_hour": {"daily_max_hour_counts": {h: c for h, c in enumerate(hours) if c},
                     "answer": hours.index(max(hours)), "scored_right_within": "2 hours, circular"},
}
json.dump(out, open("home.json", "w"), indent=1)
print(json.dumps(out, indent=1))
