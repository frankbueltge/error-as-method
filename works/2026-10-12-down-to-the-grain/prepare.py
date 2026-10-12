"""prepare.py -- one material, four grains. Reads the committed NOAA CO-OPS file (sources/): hourly water
level at The Battery, New York (station 8518750), 15 Sep - 14 Nov 2012, 1,464 values in metres above MLLW.
Writes materials/master.svg, a plot with one dot per hour and nothing else on it: no axes, ticks, numbers or
words. render.js renders it at 2400 x 720. This script then reduces that render by area averaging (box
filter) to four sizes, and writes the four preparations:

  G1  record.png  1200 x 360, PNG (lossless)       ~1.2 hours per pixel column
  G2  record.jpg   300 x  90, JPEG quality 30      ~4.9 hours per column
  G3  record.jpg    75 x  23, JPEG quality 20      ~19.5 hours per column
  G4  record.jpg    19 x   6, JPEG quality 15      ~77 hours per column

It measures what each preparation still holds (materials/holds.json) BEFORE any maker runs, assigns twelve
makers to the four grains with seed 122 (three each), and writes one brief per maker and plan.json.
Run: python3 prepare.py svg && node render.js && python3 prepare.py"""
import csv, datetime, io, json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources", "CO-OPS_8518750_hourly_height_20120915-20121114.csv")
M = os.path.join(HERE, "materials")
rows = []
for r in list(csv.reader(open(SRC, encoding="utf-8")))[1:]:
    rows.append((datetime.datetime.strptime(r[0], "%Y-%m-%d %H:%M"), float(r[1])))
assert len(rows) == 1464 and rows[0][1] == 1.652 and max(v for _, v in rows) == 4.263
LO, HI = -0.5, 4.5
GRAINS = {"G1": (1200, 360), "G2": (300, 90), "G3": (75, 23), "G4": (19, 6)}
QUALITY = 30
def frame(w, h):
    px, py = 0.01 * w, 0.03 * h
    X = lambda i: px + i / (len(rows) - 1) * (w - 2 * px)
    Y = lambda v: py + (HI - v) / (HI - LO) * (h - 2 * py)          # more water higher up
    return X, Y

if sys.argv[1:] == ["svg"]:
    for g, (w, h) in GRAINS.items():
        X, Y = frame(w, h)
        d = os.path.join(M, g); os.makedirs(d, exist_ok=True)
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (w, h),
               '<rect width="%d" height="%d" fill="#ffffff"/>' % (w, h)]
        svg += ['<circle cx="%.3f" cy="%.3f" r="0.8" fill="#222"/>' % (X(i), Y(v)) for i, (_, v) in enumerate(rows)]
        open(os.path.join(d, "plot.svg"), "w", encoding="utf-8").write("\n".join(svg + ["</svg>"]))
    print("four plot.svg", len(rows)); sys.exit()

from PIL import Image
holds = {}
peak = max(range(len(rows)), key=lambda i: rows[i][1])
for g, (w, h) in GRAINS.items():
    fn = "record.jpg"; path = os.path.join(M, g, fn)
    im = Image.open(path).convert("L"); assert im.size == (w, h); px = im.load()
    X, Y = frame(w, h)
    dark = [[255 - px[x, y] for y in range(h)] for x in range(w)]
    dmax = max(max(c) for c in dark)
    top = [min([y for y in range(h) if c[y] >= 0.5 * dmax] or [None]) if any(v >= 0.5 * dmax for v in c) else None for c in dark]
    surge = min(w - 1, int(X(peak)))
    others = [top[x] for x in range(w) if top[x] is not None and abs(x - surge) > max(1, w // 60)]
    hpc = len(rows) / w
    holds[g] = {"file": fn, "size": [w, h], "jpeg_quality": QUALITY, "bytes": os.path.getsize(path),
                "hours_per_column": round(hpc, 2),
                "semidiurnal_columns_per_cycle": round(12.42 / hpc, 2),
                "fortnight_columns_per_cycle": round(354.37 / hpc, 2),
                "rows_per_metre": round((h - 2 * 0.03 * h) / (HI - LO), 2),
                "surge_column": surge, "surge_top_row": top[surge],
                "highest_top_elsewhere": min(others) if others else None,
                "surge_stands_out_by_rows": (min(others) - top[surge]) if others and top[surge] is not None else None,
                "distinct_grey_levels": len(set(im.getdata()))}
json.dump(holds, open(os.path.join(M, "holds.json"), "w"), indent=1)
print(json.dumps(holds))
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
DESC = {g: "a picture %d pixels wide and %d high (JPEG, compressed)" % s for g, s in GRAINS.items()}
grains = ["G1", "G2", "G3", "G4"] * 3
random.Random(122).shuffle(grains)
plan = []
for i, g in enumerate(grains, 1):
    m = "m%02d" % i
    base = "/tmp/claude-0/s122/mk/%s" % m
    fn = "record.jpg"
    text = (BRIEF.replace("{FOLDER}", base + "/work").replace("{SCRATCH}", base + "/scratch")
            .replace("{FILE}", fn).replace("{AS}", DESC[g]))
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(text)
    plan.append({"maker": m, "grain": g, "folder": base + "/work", "scratch": base + "/scratch", "file": fn})
json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([p["grain"] for p in plan])
