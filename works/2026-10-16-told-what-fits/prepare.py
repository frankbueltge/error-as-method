"""prepare.py -- one material, one grain, three briefs. Reads the committed TreeNet extract (sources/): Pfynwald
(Valais, Switzerland), control plot, Scots pine tree 1038, point dendrometer series 1548, stem radius change in
micrometres, every 10 minutes, 2024-07-09 00:00 UTC to 2024-09-07 23:50 UTC (8,784 rows, none missing). The hourly
value is the mean of the six 10-minute values in that UTC hour (1,464 hours).
Writes materials/F/plot.svg with Session 123's drawing (one dot per hour, no axes, ticks, numbers or words);
render.js renders it at 300 x 90 as JPEG quality 30 (grain F, unchanged since experiment 19).

Three cells of makers, the only words that differ between briefs:
  N  "You are not told what was measured, where or when."
  T  "It is a record of the radius of a tree's trunk, measured at one point on its bark. " ... "You are not told
     where or when."  (true)
  C  "It is a record of the carbon dioxide content of the air at a measuring station. " ... "You are not told where
     or when."  (false; the words experiment 21's told-true makers were given, when they were true)

It measures what the record and the picture hold (materials/holds.json) BEFORE any maker runs, assigns eighteen makers
to N, T and C with seed 131, and writes one brief each and plan.json.
Run: python3 prepare.py svg && node render.js && python3 prepare.py"""
import json, os, random, sys, cmath, csv, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "materials")
SRC = os.path.join(HERE, "sources", "pfynwald_1548_src_10min_20240709_20240907.csv")
raw = list(csv.DictReader(open(SRC)))
assert len(raw) == 8784 and raw[0]["timestamp_utc"] == "2024-07-09T00:00Z" and raw[-1]["timestamp_utc"] == "2024-09-07T23:50Z"
rows = [sum(float(r["value_um"]) for r in raw[i:i + 6]) / 6 for i in range(0, 8784, 6)]
assert len(rows) == 1464
LO, HI = min(rows) - 0.04 * (max(rows) - min(rows)), max(rows) + 0.04 * (max(rows) - min(rows))
W, H = 300, 90
def frame(w, h):
    px, py = 0.01 * w, 0.03 * h
    X = lambda i: px + i / (len(rows) - 1) * (w - 2 * px)
    Y = lambda val: py + (HI - val) / (HI - LO) * (h - 2 * py)
    return X, Y
if sys.argv[1:] == ["svg"]:
    json.dump({"stem_radius_change_um": [round(x, 3) for x in rows], "start_utc": "2024-07-09T00:00Z", "step": "1 hour",
               "site": "Pfynwald-Control", "tree": "1038", "series_id": 1548, "species": "Pinus sylvestris"},
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
holds["record_amp_um"] = {name: round(amp(rows, p), 2) for name, p in
    [("24.00h solar day", 24.0), ("12.00h", 12.0), ("12.42h M2 tide", 12.4206), ("24.84h lunar day", 24.8412), ("168h week", 168.0)]}
comp = [st.median(rows[i] for i in range(h, 1464, 24)) for h in range(24)]
hmax, hmin = comp.index(max(comp)), comp.index(min(comp))
holds["daily_composite_median_um_by_utc_hour"] = [round(x, 1) for x in comp]
holds["daily_shape"] = {"hour_of_max_utc": hmax, "hour_of_min_utc": hmin, "local_time_of_max": "UTC+2 (CEST) in summer",
    "hours_falling_max_to_min": (hmin - hmax) % 24, "hours_rising_min_to_max": (hmax - hmin) % 24,
    "harmonic_ratio_12h_to_24h": round(amp(comp * 61, 12.0) / amp(comp * 61, 24.0), 3)}
dm = [sum(rows[i:i + 24]) / 24 for i in range(0, 1464, 24)]
holds["daily_mean_um"] = [round(x, 1) for x in dm]
holds["daily_range_um"] = [round(max(rows[i:i + 24]) - min(rows[i:i + 24]), 1) for i in range(0, 1464, 24)]
holds["day_to_day_mean_jumps_over_30um"] = [(d, round(dm[d] - dm[d - 1], 1)) for d in range(1, 61) if abs(dm[d] - dm[d - 1]) > 30]
holds["range_um"] = [round(min(rows), 1), round(max(rows), 1)]
json.dump(holds, open(os.path.join(M, "holds.json"), "w"), indent=1)
print(json.dumps(holds, indent=1))
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
NOTTOLD = {"N": "You are not told what was measured, where or when.", "T": "You are not told where or when.",
           "C": "You are not told where or when."}
TOLD = {"N": "", "T": "It is a record of the radius of a tree's trunk, measured at one point on its bark. ",
        "C": "It is a record of the carbon dioxide content of the air at a measuring station. "}
def brief(c, base):
    return (BRIEF.replace("{FOLDER}", base + "/work").replace("{SCRATCH}", base + "/scratch")
            .replace("{TOLD}", TOLD[c]).replace("{NOTTOLD}", NOTTOLD[c]))
rng = random.Random(131)
cells = ["N", "T", "C"] * 6
rng.shuffle(cells)
plan = []
for i, c in enumerate(cells, 1):
    m = "m%02d" % i
    base = "/tmp/claude-0/s131/mk/%s" % m
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(brief(c, base))
    plan.append({"maker": m, "cell": c, "folder": base + "/work", "scratch": base + "/scratch", "file": "record.jpg"})
json.dump({"makers": plan}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([p["cell"] for p in plan])
