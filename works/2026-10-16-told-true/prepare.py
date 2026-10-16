"""prepare.py -- one material, one grain, three briefs and an inquiry. Reads the committed NOAA GML extract
(sources/): West Branch, Iowa (WBI) tall tower, carbon dioxide dry-air mole fraction in ppm, hourly, intake 31 m
above ground, 2019-07-15 00:00 UTC to 2019-09-13 23:00 UTC (1,464 hours, 2 missing, filled by linear interpolation
between their neighbours). Only rows whose rejection flag (first qcflag character) is '.' are used.
Writes materials/F/plot.svg with Session 123's drawing (one dot per hour, no axes, ticks, numbers or words);
render.js renders it at 300 x 90 as JPEG quality 30 (Session 124's grain F, unchanged since experiment 19).

Three cells of makers, the only words that differ between briefs:
  N  "You are not told what was measured, where or when."
  T  "It is a record of the carbon dioxide content of the air at a measuring station. " ... "You are not told where
     or when."  (true)
  F  "It is a record of the water level in a tidal harbour. " ... "You are not told where or when."  (false; the same
     words experiment 20's told makers were given)

And Orne's pre-experimental inquiry (row S129.INQUIRY): eight fresh agents, four shown the T brief and four the F
brief word for word, without the picture, asked what a maker would do and what the commissioner wants.

It measures what the record and the picture hold (materials/holds.json) BEFORE any maker runs, assigns eighteen makers
to N, T and F and eight inquirers to T and F with seed 130, and writes one brief each and plan.json.
Run: python3 prepare.py svg && node render.js && python3 prepare.py"""
import json, os, random, sys, cmath, datetime as dt, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "materials")
SRC = os.path.join(HERE, "sources", "noaa_gml_co2_wbi_tower_hourly_20190715_20190913.txt")
START = dt.datetime(2019, 7, 15)
V = {}
for line in open(SRC):
    if line.startswith("#") or line.startswith("site_code"): continue
    p = line.split()
    if float(p[18]) != 31.0 or p[-1][0] != ".": continue
    V[dt.datetime(int(p[1]), int(p[2]), int(p[3]), int(p[4]))] = float(p[10])
ts = [START + dt.timedelta(hours=i) for i in range(1464)]
missing = [t for t in ts if t not in V]
assert len(missing) == 2, missing
rows = [V.get(t) for t in ts]
for i, x in enumerate(rows):
    if x is None:
        rows[i] = (rows[i - 1] + V[ts[i + 1]]) / 2  # both gaps are single hours
assert len(rows) == 1464
LO, HI = min(rows) - 0.04 * (max(rows) - min(rows)), max(rows) + 0.04 * (max(rows) - min(rows))
W, H = 300, 90
def frame(w, h):
    px, py = 0.01 * w, 0.03 * h
    X = lambda i: px + i / (len(rows) - 1) * (w - 2 * px)
    Y = lambda val: py + (HI - val) / (HI - LO) * (h - 2 * py)
    return X, Y
if sys.argv[1:] == ["svg"]:
    json.dump({"co2_ppm": [round(x, 3) for x in rows], "start_utc": "2019-07-15T00:00Z", "step": "1 hour",
               "station": "WBI", "intake_m": 31, "filled": [t.isoformat() for t in missing]},
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
         "semidiurnal_columns_per_cycle": round(12.42 / hpc, 2),
         "ink_centre_amp_daily": round(amp(cen, 24 / hpc), 3), "ink_centre_amp_12_42h": round(amp(cen, 12.42 / hpc), 3),
         "distinct_grey_levels": len(set(im.getdata()))}
holds["record_amp_ppm"] = {name: round(amp(rows, p), 2) for name, p in
    [("24.00h solar day", 24.0), ("12.00h", 12.0), ("8.00h", 8.0), ("12.42h M2 tide", 12.4206),
     ("25.82h O1 tide", 25.8193), ("23.93h K1", 23.9345), ("24.84h lunar day", 24.8412),
     ("354.4h spring-neap 14.77d", 354.37), ("168h week", 168.0)]}
# the daily regular's shape (row S128.SHAPE needs it to be neither a ceiling with a dip nor a near-sine swing)
comp = [st.median(rows[i] for i in range(h, 1464, 24)) for h in range(24)]
hmax, hmin = comp.index(max(comp)), comp.index(min(comp))
holds["daily_composite_median_ppm_by_utc_hour"] = [round(x, 1) for x in comp]
holds["daily_shape"] = {"hour_of_max_utc": hmax, "hour_of_min_utc": hmin,
    "hours_rising_min_to_max": (hmax - hmin) % 24, "hours_falling_max_to_min": (hmin - hmax) % 24,
    "share_of_composite_range_in_lower_fifth_hours": sum(x < min(comp) + 0.2 * (max(comp) - min(comp)) for x in comp),
    "harmonic_ratio_12h_to_24h": round(amp(comp * 61, 12.0) / amp(comp * 61, 24.0), 3),
    "local_standard_time": "UTC-6 (site_utc2lst in the source header)"}
holds["daily_range_ppm"] = [round(max(rows[i:i + 24]) - min(rows[i:i + 24]), 1) for i in range(0, 1464, 24)]
holds["daily_max_hour_utc"] = [max(range(24), key=lambda h: rows[i + h]) for i in range(0, 1464, 24)]
holds["range_ppm"] = [round(min(rows), 1), round(max(rows), 1)]
holds["filled_hours_utc"] = [t.isoformat() for t in missing]
json.dump(holds, open(os.path.join(M, "holds.json"), "w"), indent=1)
print(json.dumps({k: x for k, x in holds.items() if k not in ("daily_range_ppm", "daily_max_hour_utc")}, indent=1))
print("daily range", holds["daily_range_ppm"]); print("hour of daily max (UTC)", holds["daily_max_hour_utc"])
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
NOTTOLD = {"N": "You are not told what was measured, where or when.", "T": "You are not told where or when.",
           "F": "You are not told where or when."}
TOLD = {"N": "", "T": "It is a record of the carbon dioxide content of the air at a measuring station. ",
        "F": "It is a record of the water level in a tidal harbour. "}
def brief(c, base):
    return (BRIEF.replace("{FOLDER}", base + "/work").replace("{SCRATCH}", base + "/scratch")
            .replace("{TOLD}", TOLD[c]).replace("{NOTTOLD}", NOTTOLD[c]))
rng = random.Random(130)
cells = ["N", "T", "F"] * 6
rng.shuffle(cells)
plan = []
for i, c in enumerate(cells, 1):
    m = "m%02d" % i
    base = "/tmp/claude-0/s130/mk/%s" % m
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(brief(c, base))
    plan.append({"maker": m, "cell": c, "folder": base + "/work", "scratch": base + "/scratch", "file": "record.jpg"})
# the inquiry: the told briefs word for word, as a maker in that cell would receive them (paths of an unused folder)
INQ = open(os.path.join(HERE, "inquiry", "INQUIRY.md"), encoding="utf-8").read()
qcells = ["T", "F"] * 4
rng.shuffle(qcells)
inq = []
for i, c in enumerate(qcells, 1):
    q = "q%02d" % i
    text = INQ.replace("{BRIEF}", brief(c, "/tmp/claude-0/s130/mk/m19"))
    open(os.path.join(HERE, "inquiry", q + ".md"), "w", encoding="utf-8").write(text)
    inq.append({"inquirer": q, "cell": c})
json.dump({"makers": plan, "inquiry": inq}, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([p["cell"] for p in plan]); print([p["cell"] for p in inq])
