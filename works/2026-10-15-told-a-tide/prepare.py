"""prepare.py -- one material, one grain, two briefs. Reads the committed USGS Geomagnetism Program file (sources/):
Boulder observatory (BOU), horizontal intensity H in nT, one-minute values ("adjusted"), 2025-07-02 00:00 UTC to
2025-08-31 23:59 UTC (87,840 values, 2 missing). Averages each sixty to one hourly value: 1,464 values (61 days).
Writes materials/F/plot.svg with Session 123's drawing (one dot per hour, no axes, ticks, numbers or words);
render.js renders it at 300 x 90 as JPEG quality 30 (Session 124's grain F: ~4.9 hours a column, the daily cycle
~4.9 columns a cycle, measurable).

Two cells, the only words that differ between briefs:
  N  "one value every hour for 61 consecutive days, 1,464 values". You are not told what was measured, where or when.
  T  the same, and before the picture is described: "It is a record of the water level in a tidal harbour."
     (false: it is the Earth's magnetic field at Boulder, Colorado). Where and when are not told.

It measures what the record and the picture hold (materials/holds.json) BEFORE any maker runs, assigns twelve makers
to N and T with seed 128 (six each), and writes one brief per maker and plan.json.
Run: python3 prepare.py svg && node render.js && python3 prepare.py"""
import json, os, random, sys, cmath
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "materials")
d = json.load(open(os.path.join(HERE, "sources", "usgs_geomag_BOU_H_minute_20250702_20250901.json")))
assert d["times"][0] == "2025-07-02T00:00:00.000Z" and len(d["times"]) == 87840
v = d["values"][0]["values"]
rows = []
for i in range(0, 87840, 60):
    w = [x for x in v[i:i + 60] if x is not None]
    assert len(w) >= 58
    rows.append(sum(w) / len(w))
assert len(rows) == 1464
LO, HI = min(rows) - 0.04 * (max(rows) - min(rows)), max(rows) + 0.04 * (max(rows) - min(rows))
W, H = 300, 90
def frame(w, h):
    px, py = 0.01 * w, 0.03 * h
    X = lambda i: px + i / (len(rows) - 1) * (w - 2 * px)
    Y = lambda val: py + (HI - val) / (HI - LO) * (h - 2 * py)
    return X, Y
if sys.argv[1:] == ["svg"]:
    json.dump({"h_nT": [round(x, 2) for x in rows], "start_utc": "2025-07-02T00:00Z", "step": "1 hour",
               "station": "BOU", "element": "H"}, open(os.path.join(M, "hourly.json"), "w"))
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
         "semidiurnal_columns_per_cycle": round(12.42 / hpc, 2),
         "ink_centre_amp_daily": round(amp(cen, 24 / hpc), 3), "ink_centre_amp_12_42h": round(amp(cen, 12.42 / hpc), 3),
         "distinct_grey_levels": len(set(im.getdata()))}
# the record's own amplitudes (nT) at the periods the true kind and the false kind each predict
holds["record_amp_nT"] = {name: round(amp(rows, p), 2) for name, p in
    [("24.00h solar day", 24.0), ("12.00h", 12.0), ("8.00h", 8.0), ("12.42h M2 tide", 12.4206),
     ("25.82h O1 tide", 25.8193), ("23.93h K1", 23.9345), ("24.84h lunar day", 24.8412),
     ("354.4h spring-neap 14.77d", 354.37), ("655.7h 27.3d", 655.7)]}
holds["daily_range_nT"] = [round(max(rows[i:i + 24]) - min(rows[i:i + 24]), 1) for i in range(0, 1464, 24)]
holds["daily_min_hour_utc"] = [min(range(24), key=lambda h: rows[i + h]) for i in range(0, 1464, 24)]
holds["range_nT"] = [round(min(rows), 1), round(max(rows), 1)]
json.dump(holds, open(os.path.join(M, "holds.json"), "w"), indent=1)
print(json.dumps({k: x for k, x in holds.items() if k not in ("daily_range_nT", "daily_min_hour_utc")}, indent=1))
print("daily range", holds["daily_range_nT"]); print("hour of daily min (UTC)", holds["daily_min_hour_utc"])
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
NOTTOLD = {"N": "You are not told what was measured, where or when.", "T": "You are not told where or when."}
TOLD = {"N": "", "T": "It is a record of the water level in a tidal harbour. "}
cells = ["N", "T"] * 6
random.Random(128).shuffle(cells)
plan = []
for i, c in enumerate(cells, 1):
    m = "m%02d" % i
    base = "/tmp/claude-0/s128/mk/%s" % m
    text = (BRIEF.replace("{FOLDER}", base + "/work").replace("{SCRATCH}", base + "/scratch")
            .replace("{TOLD}", TOLD[c]).replace("{NOTTOLD}", NOTTOLD[c]))
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(text)
    plan.append({"maker": m, "cell": c, "folder": base + "/work", "scratch": base + "/scratch", "file": "record.jpg"})
json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([p["cell"] for p in plan])
