"""prepare.py -- one material, one grain, two briefs. Reads the committed NRCS SCAN answer (sources/): Starkville,
Mississippi (2064:MS:SCAN, 33.47 N, 88.78 W, 270 ft), soil temperature at 2 inches (5 cm), sensor ordinal 1, hourly,
2025-07-15 00:00 to 2025-09-13 23:00 local standard time, whole degrees Fahrenheit as the service stores them.
1,464 hours, none empty. Writes materials/F/plot.svg with Session 123's drawing (one dot per hour, no axes, ticks,
numbers or words); render.js renders it at 300 x 90 as JPEG quality 30 (grain F, unchanged since experiment 19).

Two cells of makers, the only words that differ between briefs (both true):
  N   "You are not told what was measured, where or when."
  W   "It was recorded from 15 July to 13 September 2025. " ... "You are not told what was measured or where."
      (when; the picture can neither confirm nor refute it: no weekly regular, no annual cycle within 61 days)

It measures what the record and the picture hold (materials/holds.json) BEFORE any maker runs, assigns twelve
makers to the cells with seed 135, and writes one brief each and plan.json.
Run: python3 prepare.py svg && node render.js && python3 prepare.py"""
import json, os, random, sys, cmath, statistics as st, datetime as dt
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "materials")
els = json.load(open(os.path.join(HERE, "sources", "sto_2in_hourly.json")))[0]["data"]
el = [e for e in els if e["stationElement"]["ordinal"] == 1][0]
T0 = dt.datetime(2025, 7, 15)
vals = {v["date"]: v.get("value") for v in el["values"]}
hours = [T0 + dt.timedelta(hours=i) for i in range(1464)]
rows = [vals[h.strftime("%Y-%m-%d %H:%M")] for h in hours]
assert all(r is not None for r in rows)
LO, HI = min(rows) - 0.04 * (max(rows) - min(rows)), max(rows) + 0.04 * (max(rows) - min(rows))
W, H = 300, 90
def frame(w, h):
    px, py = 0.01 * w, 0.03 * h
    X = lambda i: px + i / (len(rows) - 1) * (w - 2 * px)
    Y = lambda val: py + (HI - val) / (HI - LO) * (h - 2 * py)
    return X, Y
if sys.argv[1:] == ["svg"]:
    json.dump({"soil_temp_2in_degF": rows, "start_local_standard_time": "2025-07-15T00:00", "step": "1 hour",
               "station": "Starkville, MS (SCAN 2064)", "lat": 33.47094, "lon": -88.78051, "elevation_ft": 270},
              open(os.path.join(M, "hourly.json"), "w"))
    X, Y = frame(W, H)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (W, H),
           '<rect width="%d" height="%d" fill="#ffffff"/>' % (W, H)]
    svg += ['<circle cx="%.3f" cy="%.3f" r="0.8" fill="#222"/>' % (X(i), Y(x)) for i, x in enumerate(rows)]
    open(os.path.join(M, "F", "plot.svg"), "w", encoding="utf-8").write("\n".join(svg + ["</svg>"]))
    print("plot.svg", len(rows), min(rows), max(rows)); sys.exit()
from PIL import Image
def amp(series, period):
    n = len(series); m = sum(series) / n
    return abs(sum((x - m) * cmath.exp(-2j * cmath.pi * i / period) for i, x in enumerate(series))) * 2 / n
path = os.path.join(M, "F", "record.jpg")
im = Image.open(path).convert("L"); assert im.size == (W, H); px = im.load()
dark = [[255 - px[x, y] for y in range(H)] for x in range(W)]
cen = [sum(y * c for y, c in enumerate(col)) / max(1, sum(col)) for col in dark]
hpc = len(rows) / W
daily_mean = [sum(rows[d * 24:(d + 1) * 24]) / 24 for d in range(61)]
n = len(daily_mean); mx = (n - 1) / 2; my = sum(daily_mean) / n
slope = sum((i - mx) * (y - my) for i, y in enumerate(daily_mean)) / sum((i - mx) ** 2 for i in range(n))
holds = {"file": "record.jpg", "size": [W, H], "jpeg_quality": 30, "bytes": os.path.getsize(path),
         "hours_per_column": round(hpc, 2), "daily_columns_per_cycle": round(24 / hpc, 2),
         "ink_centre_amp_daily": round(amp(cen, 24 / hpc), 3), "distinct_grey_levels": len(set(im.getdata())),
         "distinct_values_degF": sorted(set(rows)), "range_degF": [min(rows), max(rows)]}
holds["record_amp_degF"] = {name: round(amp(rows, p), 3) for name, p in
    [("24h", 24.0), ("12h", 12.0), ("12.42h M2 tide", 12.4206), ("168h week", 168.0)]}
comp = [st.median(rows[i] for i in range(h, 1464, 24)) for h in range(24)]
holds["daily_composite_median_degF_by_local_hour"] = comp
holds["daily_mean_degF"] = [round(x, 2) for x in daily_mean]
holds["daily_range_degF"] = [max(rows[d * 24:(d + 1) * 24]) - min(rows[d * 24:(d + 1) * 24]) for d in range(61)]
holds["daily_mean_trend_degF_per_day"] = round(slope, 4)
wd = [st.mean(daily_mean[d] for d in range(61) if (T0 + dt.timedelta(days=d)).weekday() == k) for k in range(7)]
holds["mean_by_weekday_mon_to_sun_degF"] = [round(x, 2) for x in wd]
json.dump(holds, open(os.path.join(M, "holds.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in holds.items() if not isinstance(v, list) or len(v) < 30}, indent=1))
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
WHEN = "It was recorded from 15 July to 13 September 2025. "
NOTTOLD = {"N": "You are not told what was measured, where or when.", "W": "You are not told what was measured or where."}
TOLD = {"N": "", "W": WHEN}
def brief(c, base):
    return (BRIEF.replace("{FOLDER}", base + "/work").replace("{SCRATCH}", base + "/scratch")
            .replace("{TOLD}", TOLD[c]).replace("{NOTTOLD}", NOTTOLD[c]))
rng = random.Random(135)
cells = ["N", "W"] * 6
rng.shuffle(cells)
plan = []
for i, c in enumerate(cells, 1):
    m = "m%02d" % i
    base = "/tmp/claude-0/s135/mk/%s" % m
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(brief(c, base))
    plan.append({"maker": m, "cell": c, "folder": base + "/work", "scratch": base + "/scratch", "file": "record.jpg"})
json.dump({"makers": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([p["cell"] for p in plan])
