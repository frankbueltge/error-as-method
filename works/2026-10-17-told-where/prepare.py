"""prepare.py -- one material, one grain, four briefs. Reads the committed SURFRAD extract (sources/): Fort Peck,
Montana, downwelling global solar irradiance (W m-2) every minute, 2025-07-15 00:00 to 2025-09-13 23:59 UTC. Each
line's time is the END of its minute (README_SURFRAD.txt), so a line stamped hh:00 belongs to the previous hour. The
hourly value is the mean of the minutes in that UTC hour that are present and carry QC flag 0 (the provider's own
flag). 33 minutes are missing, 23 of them on 8 August 18 UTC, and 10 are flagged, all in the instrument fault that
follows that gap and reads up to 8,566 W m-2. 1,464 hours, none empty.
Writes materials/F/plot.svg with Session 123's drawing (one dot per hour, no axes, ticks, numbers or words);
render.js renders it at 300 x 90 as JPEG quality 30 (grain F, unchanged since experiment 19).

Four cells of makers, the only words that differ between briefs (all true):
  N   "You are not told what was measured, where or when."
  K   "It is a record of the sunlight reaching the ground: the solar radiation falling on a level surface. "
      ... "You are not told where or when."                       (the kind; the picture can confirm it)
  P   "It was recorded at a station called Fort Peck, in north-eastern Montana, USA, 634 metres above sea level. "
      ... "You are not told what was measured or when."          (where; the picture can neither confirm nor refute it)
  KP  both sentences ... "You are not told when."

It measures what the record and the picture hold (materials/holds.json) BEFORE any maker runs, assigns twenty-four
makers to the cells with seed 133, and writes one brief each and plan.json.
Run: python3 prepare.py svg && node render.js && python3 prepare.py"""
import json, os, random, sys, cmath, csv, statistics as st, datetime as dt, collections
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "materials")
SRC = os.path.join(HERE, "sources", "fpk_dwsolar_1min_20250715_20250913.csv")
acc = collections.defaultdict(list); fault = []
for r in csv.DictReader(open(SRC)):
    t = dt.datetime(int(r["year"]), int(r["month"]), int(r["day"]), int(r["hour"]), int(r["min"])) - dt.timedelta(minutes=1)
    v, q = float(r["dw_solar_wm2"]), int(r["qc_dwsolar"])
    if q != 0 or v < -9000:
        fault.append((t.isoformat(), v, q)); continue
    acc[t.replace(minute=0)].append(v)
T0 = dt.datetime(2025, 7, 15)
hours = [T0 + dt.timedelta(hours=i) for i in range(1464)]
assert all(acc[h] for h in hours)
rows = [sum(acc[h]) / len(acc[h]) for h in hours]
LO, HI = min(rows) - 0.04 * (max(rows) - min(rows)), max(rows) + 0.04 * (max(rows) - min(rows))
W, H = 300, 90
def frame(w, h):
    px, py = 0.01 * w, 0.03 * h
    X = lambda i: px + i / (len(rows) - 1) * (w - 2 * px)
    Y = lambda val: py + (HI - val) / (HI - LO) * (h - 2 * py)
    return X, Y
if sys.argv[1:] == ["svg"]:
    json.dump({"dw_solar_wm2": [round(x, 2) for x in rows], "start_utc": "2025-07-15T00:00Z", "step": "1 hour",
               "station": "Fort Peck, MT (SURFRAD fpk)", "lat": 48.31, "lon": -105.10, "elevation_m": 634,
               "minutes_per_hour": [len(acc[h]) for h in hours]},
              open(os.path.join(M, "hourly.json"), "w"))
    X, Y = frame(W, H)
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (W, H),
           '<rect width="%d" height="%d" fill="#ffffff"/>' % (W, H)]
    svg += ['<circle cx="%.3f" cy="%.3f" r="0.8" fill="#222"/>' % (X(i), Y(x)) for i, x in enumerate(rows)]
    open(os.path.join(M, "F", "plot.svg"), "w", encoding="utf-8").write("\n".join(svg + ["</svg>"]))
    print("plot.svg", len(rows), round(min(rows), 1), round(max(rows), 1)); sys.exit()
from PIL import Image
def amp(series, period):
    n = len(series); m = sum(series) / n
    return abs(sum((x - m) * cmath.exp(-2j * cmath.pi * i / period) for i, x in enumerate(series))) * 2 / n
path = os.path.join(M, "F", "record.jpg")
im = Image.open(path).convert("L"); assert im.size == (W, H); px = im.load()
dark = [[255 - px[x, y] for y in range(H)] for x in range(W)]
cen = [sum(y * c for y, c in enumerate(col)) / max(1, sum(col)) for col in dark]
hpc = len(rows) / W
holds = {"file": "record.jpg", "size": [W, H], "jpeg_quality": 30, "bytes": os.path.getsize(path),
         "hours_per_column": round(hpc, 2), "daily_columns_per_cycle": round(24 / hpc, 2),
         "ink_centre_amp_daily": round(amp(cen, 24 / hpc), 3), "ink_centre_amp_12_42h": round(amp(cen, 12.42 / hpc), 3),
         "distinct_grey_levels": len(set(im.getdata()))}
holds["record_amp_wm2"] = {name: round(amp(rows, p), 2) for name, p in
    [("24.00h solar day", 24.0), ("12.00h", 12.0), ("12.42h M2 tide", 12.4206), ("24.84h lunar day", 24.8412), ("168h week", 168.0)]}
comp = [st.median(rows[i] for i in range(h, 1464, 24)) for h in range(24)]
holds["daily_composite_median_wm2_by_utc_hour"] = [round(x, 1) for x in comp]
holds["hours_per_day_above_5_wm2"] = [sum(1 for x in rows[d * 24:(d + 1) * 24] if x > 5) for d in range(61)]
holds["night_floor"] = {"hours_below_5_wm2": sum(1 for x in rows if x < 5), "share": round(sum(1 for x in rows if x < 5) / 1464, 3),
                        "min_wm2": round(min(rows), 2)}
holds["daily_total_kwh_m2"] = [round(sum(rows[d * 24:(d + 1) * 24]) / 1000, 2) for d in range(61)]
holds["daily_max_wm2"] = [round(max(rows[d * 24:(d + 1) * 24]), 1) for d in range(61)]
holds["range_wm2"] = [round(min(rows), 2), round(max(rows), 2)]
holds["excluded_minutes"] = {"count": len(fault), "first": fault[0] if fault else None, "last": fault[-1] if fault else None,
                             "max_flagged_wm2": max((v for _, v, _ in fault), default=None)}
json.dump(holds, open(os.path.join(M, "holds.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in holds.items() if not isinstance(v, list) or len(v) < 30}, indent=1))
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
KIND = "It is a record of the sunlight reaching the ground: the solar radiation falling on a level surface. "
PLACE = "It was recorded at a station called Fort Peck, in north-eastern Montana, USA, 634 metres above sea level. "
NOTTOLD = {"N": "You are not told what was measured, where or when.", "K": "You are not told where or when.",
           "P": "You are not told what was measured or when.", "KP": "You are not told when."}
TOLD = {"N": "", "K": KIND, "P": PLACE, "KP": KIND + PLACE}
def brief(c, base):
    return (BRIEF.replace("{FOLDER}", base + "/work").replace("{SCRATCH}", base + "/scratch")
            .replace("{TOLD}", TOLD[c]).replace("{NOTTOLD}", NOTTOLD[c]))
rng = random.Random(133)
cells = ["N", "K", "P", "KP"] * 6
rng.shuffle(cells)
plan = []
for i, c in enumerate(cells, 1):
    m = "m%02d" % i
    base = "/tmp/claude-0/s133/mk/%s" % m
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(brief(c, base))
    plan.append({"maker": m, "cell": c, "folder": base + "/work", "scratch": base + "/scratch", "file": "record.jpg"})
json.dump({"makers": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([p["cell"] for p in plan])
