"""prepare.py -- one material, two grains, three briefs. Reads the committed USGS file (sources/): Potomac River
near Washington, DC, Little Falls Pump Station (01646500), dissolved oxygen in mg/L, 5-minute values
2025-07-01 00:00 UTC to 2025-08-31 00:00 UTC (17,569 values, all approved). Averages each twelve to one hourly
value: 1,464 values (61 days). Writes materials/<grain>/plot.svg with Session 123's drawing (one dot per hour,
no axes, ticks, numbers or words); render.js renders each at its size as JPEG quality 30:

  F  300 x 90   ~4.9 hours per column   the daily cycle ~4.9 columns a cycle (measurable)
  C   40 x 12   ~36.6 hours per column  the daily cycle ~0.66 columns a cycle (not measurable)

Three cells, the only words that differ between briefs:
  F  the 300-px picture, "1,464 values taken one after another at equal intervals"
  U  the 40-px picture,  "one value every hour for 61 consecutive days, 1,464 values"
  X  the 40-px picture,  "values taken one after another at equal intervals"   (no count, no interval)

It measures what each picture holds (materials/holds.json) BEFORE any maker runs, assigns twelve makers to
F, U, X with seed 124 (four each), and writes one brief per maker and plan.json.
Run: python3 prepare.py svg && node render.js && python3 prepare.py"""
import json, os, random, sys, cmath
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(HERE, "materials")
def hourly(code):
    d = json.load(open(os.path.join(HERE, "sources", "usgs_01646500_%s_20250701_20250831.json" % code)))
    blk = [b for b in d["value"]["timeSeries"][0]["values"] if b["value"]][0]["value"]
    assert len(blk) == 17569 and blk[0]["dateTime"] == "2025-06-30T20:00:00.000-04:00"
    assert all(x["qualifiers"] == ["A"] for x in blk)
    v = [float(x["value"]) for x in blk][:17568]
    return [sum(v[i:i + 12]) / 12 for i in range(0, 17568, 12)]
rows = hourly("00300"); assert len(rows) == 1464
LO, HI = 5.5, 11.0                                                  # mg/L; min 6.01, max 10.58 (hourly)
GRAINS = {"F": (300, 90), "C": (40, 12)}
def frame(w, h):
    px, py = 0.01 * w, 0.03 * h
    X = lambda i: px + i / (len(rows) - 1) * (w - 2 * px)
    Y = lambda v: py + (HI - v) / (HI - LO) * (h - 2 * py)
    return X, Y
if sys.argv[1:] == ["svg"]:
    json.dump({"do_mg_l": [round(v, 3) for v in rows], "water_temp_c": [round(v, 3) for v in hourly("00010")],
               "start_utc": "2025-07-01T00:00Z", "step": "1 hour"}, open(os.path.join(M, "hourly.json"), "w"))
    for g, (w, h) in GRAINS.items():
        X, Y = frame(w, h)
        dd = os.path.join(M, g); os.makedirs(dd, exist_ok=True)
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (w, h),
               '<rect width="%d" height="%d" fill="#ffffff"/>' % (w, h)]
        svg += ['<circle cx="%.3f" cy="%.3f" r="0.8" fill="#222"/>' % (X(i), Y(v)) for i, v in enumerate(rows)]
        open(os.path.join(dd, "plot.svg"), "w", encoding="utf-8").write("\n".join(svg + ["</svg>"]))
    print("two plot.svg", len(rows)); sys.exit()
from PIL import Image
def power(series, period):
    n = len(series); m = sum(series) / n
    return abs(sum((v - m) * cmath.exp(-2j * cmath.pi * i / period) for i, v in enumerate(series))) / n
holds = {}
for g, (w, h) in GRAINS.items():
    path = os.path.join(M, g, "record.jpg")
    im = Image.open(path).convert("L"); assert im.size == (w, h); px = im.load()
    dark = [[255 - px[x, y] for y in range(h)] for x in range(w)]
    cen = [sum(y * v for y, v in enumerate(c)) / max(1, sum(c)) for c in dark]
    spread = [sum(1 for v in c if v > 0.3 * max(c)) for c in dark]
    hpc = len(rows) / w
    holds[g] = {"file": "record.jpg", "size": [w, h], "jpeg_quality": 30, "bytes": os.path.getsize(path),
                "hours_per_column": round(hpc, 2), "daily_columns_per_cycle": round(24 / hpc, 2),
                "daily_measurable": 24 / hpc >= 2,
                "ink_centre_amplitude_at_daily_period": round(power(cen, 24 / hpc), 3) if 24 / hpc >= 2 else None,
                "ink_rows_per_column": spread, "mean_ink_rows_per_column": round(sum(spread) / w, 2),
                "distinct_grey_levels": len(set(im.getdata()))}
# the record's own daily swing per day (max - min of 24 hours), for the face and for P7
holds["daily_range_mg_l"] = [round(max(rows[i:i + 24]) - min(rows[i:i + 24]), 2) for i in range(0, 1464, 24)]
json.dump(holds, open(os.path.join(M, "holds.json"), "w"), indent=1)
print(json.dumps({g: {k: v for k, v in holds[g].items() if k != "ink_rows_per_column"} for g in GRAINS}, indent=1))
print("C ink rows per column", holds["C"]["ink_rows_per_column"])
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
DESC = {g: "a picture %d pixels wide and %d high (JPEG, compressed)" % s for g, s in GRAINS.items()}
ACCOUNT = {"F": "1,464 values taken one after another at equal intervals",
           "U": "one value every hour for 61 consecutive days, 1,464 values",
           "X": "values taken one after another at equal intervals"}
GRAIN = {"F": "F", "U": "C", "X": "C"}
cells = ["F", "U", "X"] * 4
random.Random(124).shuffle(cells)
plan = []
for i, c in enumerate(cells, 1):
    m = "m%02d" % i
    base = "/tmp/claude-0/s124/mk/%s" % m
    text = (BRIEF.replace("{FOLDER}", base + "/work").replace("{SCRATCH}", base + "/scratch")
            .replace("{FILE}", "record.jpg").replace("{AS}", DESC[GRAIN[c]]).replace("{ACCOUNT}", ACCOUNT[c]))
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(text)
    plan.append({"maker": m, "cell": c, "grain": GRAIN[c], "folder": base + "/work", "scratch": base + "/scratch",
                 "file": "record.jpg"})
json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([p["cell"] for p in plan])
