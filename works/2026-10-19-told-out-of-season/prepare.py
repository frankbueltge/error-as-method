"""prepare.py -- one material, one grain, three briefs (Session 137). Reads the committed USGS answer (sources/):
Dinwoody Creek above lakes near Burris, Wyoming (06221400), discharge in cubic feet per second, every 15 minutes,
averaged into hours of local standard time (UTC-7), 2025-08-01 00:00 to 2025-09-30 23:00, 1,464 hours. Writes
materials/F/plot.svg with Session 123's drawing (one dot per hour, no axes, ticks, numbers or words); render.js renders
it at 300 x 90 as JPEG quality 30 (grain F, unchanged since experiment 19).

Three cells of makers, the only words that differ between briefs. Both dates are FALSE; the record ran 1 August to
30 September 2025. The lie is this practice's, told to the makers for row S135.DEFAULT and stated here, in
PREDICTIONS.md and in work.md, never to the makers:
  C  "It was recorded from 15 January to 16 March 2025. "  (contradicts the family's unaided season for a falling
     record, autumn, under the northern hemisphere; Session 135's row)
  A  "It was recorded from 15 October to 14 December 2025. " (agrees with it)
  N  "You are not told what was measured, where or when."  (the default, measured again on this record)
C and A both end "You are not told what was measured or where." Each span is 61 days.

It measures what the record and the picture hold (materials/holds.json) BEFORE any maker runs, assigns eighteen makers
to the cells with seed 137, and writes one brief each and plan.json.
Run: python3 prepare.py svg && node render.js && python3 prepare.py"""
import json, os, random, sys, cmath, statistics as st, datetime as dt
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "materials")
v = json.load(open(os.path.join(HERE, "sources", "usgs_06221400_00060_iv.json")))["value"]["timeSeries"][0]["values"][0]["value"]
MST = dt.timezone(dt.timedelta(hours=-7))
acc = defaultdict(list); quals = defaultdict(int)
for x in v:
    t = dt.datetime.fromisoformat(x["dateTime"]).astimezone(MST).replace(tzinfo=None, minute=0)
    acc[t].append(float(x["value"]))
    for q in x["qualifiers"]: quals[q] += 1
T0 = dt.datetime(2025, 8, 1)
hours = [T0 + dt.timedelta(hours=i) for i in range(1464)]
assert all(acc.get(h) for h in hours)
rows = [round(sum(acc[h]) / len(acc[h]), 2) for h in hours]
LO, HI = min(rows) - 0.04 * (max(rows) - min(rows)), max(rows) + 0.04 * (max(rows) - min(rows))
W, H = 300, 90
def frame(w, h):
    px, py = 0.01 * w, 0.03 * h
    X = lambda i: px + i / (len(rows) - 1) * (w - 2 * px)
    Y = lambda val: py + (HI - val) / (HI - LO) * (h - 2 * py)
    return X, Y
if sys.argv[1:] == ["svg"]:
    json.dump({"discharge_cfs": rows, "start_local_standard_time": "2025-08-01T00:00", "utc_offset": "-07:00",
               "step": "1 hour (mean of 15-minute values)", "site": "USGS 06221400 Dinwoody Creek above lakes near Burris, WY",
               "usgs_qualifiers_count": dict(quals)}, open(os.path.join(M, "hourly.json"), "w"))
    X, Y = frame(W, H)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (W, H),
           '<rect width="%d" height="%d" fill="#ffffff"/>' % (W, H)]
    svg += ['<circle cx="%.3f" cy="%.3f" r="0.8" fill="#222"/>' % (X(i), Y(x)) for i, x in enumerate(rows)]
    open(os.path.join(M, "F", "plot.svg"), "w", encoding="utf-8").write("\n".join(svg + ["</svg>"]))
    print("plot.svg", len(rows), min(rows), max(rows), dict(quals)); sys.exit()
from PIL import Image
def amp(series, period):
    n = len(series); m = sum(series) / n
    return abs(sum((x - m) * cmath.exp(-2j * cmath.pi * i / period) for i, x in enumerate(series))) * 2 / n
path = os.path.join(M, "F", "record.jpg")
im = Image.open(path).convert("L"); assert im.size == (W, H)
daily_mean = [sum(rows[d * 24:(d + 1) * 24]) / 24 for d in range(61)]
n = len(daily_mean); mx = (n - 1) / 2; my = sum(daily_mean) / n
slope = sum((i - mx) * (y - my) for i, y in enumerate(daily_mean)) / sum((i - mx) ** 2 for i in range(n))
holds = {"file": "record.jpg", "size": [W, H], "jpeg_quality": 30, "bytes": os.path.getsize(path),
         "hours_per_column": round(len(rows) / W, 2), "range_cfs": [min(rows), max(rows)],
         "record_amp_cfs": {name: round(amp(rows, p), 3) for name, p in
            [("24h", 24.0), ("12h", 12.0), ("12.42h M2 tide", 12.4206), ("168h week", 168.0)]},
         "first_half_amp24_cfs": round(amp(rows[:732], 24.0), 2), "second_half_amp24_cfs": round(amp(rows[732:], 24.0), 2),
         "daily_composite_median_cfs_by_local_hour": [st.median(rows[i] for i in range(h, 1464, 24)) for h in range(24)],
         "daily_mean_cfs": [round(x, 1) for x in daily_mean],
         "daily_range_cfs": [round(max(rows[d * 24:(d + 1) * 24]) - min(rows[d * 24:(d + 1) * 24]), 1) for d in range(61)],
         "daily_mean_trend_cfs_per_day": round(slope, 3),
         "first_week_mean_cfs": round(sum(daily_mean[:7]) / 7, 1), "last_week_mean_cfs": round(sum(daily_mean[-7:]) / 7, 1),
         "highest_hour": [hours[rows.index(max(rows))].isoformat(), max(rows)]}
json.dump(holds, open(os.path.join(M, "holds.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in holds.items() if not isinstance(v, list) or len(v) < 30}, indent=1))
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
TOLD = {"N": "", "C": "It was recorded from 15 January to 16 March 2025. ",
        "A": "It was recorded from 15 October to 14 December 2025. "}
NOTTOLD = {"N": "You are not told what was measured, where or when.", "C": "You are not told what was measured or where.",
           "A": "You are not told what was measured or where."}
def brief(c, base):
    return (BRIEF.replace("{FOLDER}", base + "/work").replace("{SCRATCH}", base + "/scratch")
            .replace("{TOLD}", TOLD[c]).replace("{NOTTOLD}", NOTTOLD[c]))
rng = random.Random(137)
cells = ["C", "A", "N"] * 6
rng.shuffle(cells)
plan = []
for i, c in enumerate(cells, 1):
    m = "m%02d" % i
    base = "/tmp/claude-0/s137/mk/%s" % m
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(brief(c, base))
    plan.append({"maker": m, "cell": c, "folder": base + "/work", "scratch": base + "/scratch", "file": "record.jpg"})
json.dump({"makers": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([p["cell"] for p in plan])
