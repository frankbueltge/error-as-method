"""prepare.py -- one material, two grains, two accounts. Reads the committed Energy-Charts file (sources/):
public net electricity, Germany, 15-minute values, 15 Nov 2025 00:00 UTC - 15 Jan 2026 00:00 UTC. Takes the
series named "Load", averages each four quarter-hours to one hourly value: 1,464 values (61 days).
Writes materials/<grain>/plot.svg, a plot with one dot per hour and nothing else on it (the same drawing as
Session 122's prepare.py: no axes, ticks, numbers or words). render.js renders each at its own size as JPEG
quality 30:

  F  record.jpg  300 x 90   ~4.9 hours per column  the daily cycle ~4.9 columns a cycle (resolvable)
  C  record.jpg   40 x 12   ~36.6 hours per column the daily cycle ~0.66 columns a cycle (not resolvable);
                                                    the weekly cycle ~4.6 columns a cycle (resolvable)

Two accounts of the same picture, the only words that differ between briefs:
  U  "one value every hour for 61 consecutive days, 1,464 values"
  N  "1,464 values taken one after another at equal intervals"

It measures what each picture still holds (materials/holds.json) BEFORE any maker runs, assigns twelve makers
to the four cells FU, FN, CU, CN with seed 123 (three each), and writes one brief per maker and plan.json.
Run: python3 prepare.py svg && node render.js && python3 prepare.py"""
import json, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources", "energy-charts_public_power_de_20251115_20260115.json")
M = os.path.join(HERE, "materials")
d = json.load(open(SRC))
assert d["unix_seconds"][0] == 1763164800 and len(d["unix_seconds"]) == 5857
q = [p for p in d["production_types"] if p["name"] == "Load"][0]["data"][:5856]
assert None not in q
rows = [sum(q[i:i + 4]) / 4 for i in range(0, 5856, 4)]
assert len(rows) == 1464
LO, HI = 35000.0, 80000.0                                           # MW; min 39,200, max 77,144
GRAINS = {"F": (300, 90), "C": (40, 12)}
def frame(w, h):
    px, py = 0.01 * w, 0.03 * h
    X = lambda i: px + i / (len(rows) - 1) * (w - 2 * px)
    Y = lambda v: py + (HI - v) / (HI - LO) * (h - 2 * py)          # larger values higher up
    return X, Y

if sys.argv[1:] == ["svg"]:
    json.dump([round(v, 1) for v in rows], open(os.path.join(M, "hourly.json"), "w"))
    for g, (w, h) in GRAINS.items():
        X, Y = frame(w, h)
        dd = os.path.join(M, g); os.makedirs(dd, exist_ok=True)
        svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (w, h),
               '<rect width="%d" height="%d" fill="#ffffff"/>' % (w, h)]
        svg += ['<circle cx="%.3f" cy="%.3f" r="0.8" fill="#222"/>' % (X(i), Y(v)) for i, v in enumerate(rows)]
        open(os.path.join(dd, "plot.svg"), "w", encoding="utf-8").write("\n".join(svg + ["</svg>"]))
    print("two plot.svg", len(rows)); sys.exit()

from PIL import Image
import cmath
holds = {}
def power(series, period):                                         # normalised amplitude of one period
    n = len(series); m = sum(series) / n
    z = sum((v - m) * cmath.exp(-2j * cmath.pi * i / period) for i, v in enumerate(series))
    return abs(z) / n
for g, (w, h) in GRAINS.items():
    path = os.path.join(M, g, "record.jpg")
    im = Image.open(path).convert("L"); assert im.size == (w, h); px = im.load()
    dark = [[255 - px[x, y] for y in range(h)] for x in range(w)]
    # the centre of ink per column, and its spread: what a decoder of this picture can read
    cen = [sum(y * v for y, v in enumerate(c)) / max(1, sum(c)) for c in dark]
    spread = [sum(1 for v in c if v > 0.3 * max(c)) for c in dark]
    hpc = len(rows) / w
    holds[g] = {"file": "record.jpg", "size": [w, h], "jpeg_quality": 30, "bytes": os.path.getsize(path),
                "hours_per_column": round(hpc, 2),
                "daily_columns_per_cycle": round(24 / hpc, 2),
                "weekly_columns_per_cycle": round(168 / hpc, 2),
                "daily_resolvable": 24 / hpc >= 2, "weekly_resolvable": 168 / hpc >= 2,
                "ink_centre_amplitude_at_daily_period": round(power(cen, 24 / hpc), 3) if 24 / hpc >= 2 else None,
                "ink_centre_amplitude_at_weekly_period": round(power(cen, 168 / hpc), 3),
                "mean_ink_rows_per_column": round(sum(spread) / w, 2),
                "distinct_grey_levels": len(set(im.getdata()))}
json.dump(holds, open(os.path.join(M, "holds.json"), "w"), indent=1)
print(json.dumps(holds, indent=1))
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
DESC = {g: "a picture %d pixels wide and %d high (JPEG, compressed)" % s for g, s in GRAINS.items()}
ACCOUNT = {"U": "one value every hour for 61 consecutive days, 1,464 values",
           "N": "1,464 values taken one after another at equal intervals"}
cells = ["FU", "FN", "CU", "CN"] * 3
random.Random(123).shuffle(cells)
plan = []
for i, c in enumerate(cells, 1):
    m = "m%02d" % i
    base = "/tmp/claude-0/s123/mk/%s" % m
    text = (BRIEF.replace("{FOLDER}", base + "/work").replace("{SCRATCH}", base + "/scratch")
            .replace("{FILE}", "record.jpg").replace("{AS}", DESC[c[0]]).replace("{ACCOUNT}", ACCOUNT[c[1]]))
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(text)
    plan.append({"maker": m, "cell": c, "grain": c[0], "account": c[1],
                 "folder": base + "/work", "scratch": base + "/scratch", "file": "record.jpg"})
json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print([p["cell"] for p in plan])
