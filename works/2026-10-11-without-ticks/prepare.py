"""prepare.py -- one material, three preparations. Reads the committed SSA/FiveThirtyEight file (sources/),
writes materials/births.csv (T, the table as published), materials/births.svg (I, a plain dot plot with axes,
rendered to births.png) and materials/lossy.svg (L, the same dots with no axes, no ticks, no numbers, rendered
small and as a heavily compressed JPEG, births.jpg). render.js renders both. Assigns twelve makers to the three
arms with seed 121 and writes one brief per maker to briefs/run/ and the plan to plan.json. Each maker gets
its own work folder and its own scratch folder (F-211). Run: python3 prepare.py && node render.js"""
import csv, datetime, json, os, random, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources", "US_births_2000-2014_SSA.csv")
rows = []
for r in csv.DictReader(open(SRC, encoding="utf-8")):
    d = datetime.date(int(r["year"]), int(r["month"]), int(r["date_of_month"]))
    assert d.isoweekday() == int(r["day_of_week"])
    rows.append((d, int(r["births"])))
assert len(rows) == 5479 and rows[0] == (datetime.date(2000, 1, 1), 9083) and rows[-1][1] == 11990
M = os.path.join(HERE, "materials")
os.makedirs(M, exist_ok=True)
shutil.copy(SRC, os.path.join(M, "births.csv"))   # T: the table exactly as published

d0, d1 = datetime.date(2000, 1, 1), datetime.date(2015, 1, 1)
lo, hi = 5000, 17000
def dots(W, H, L, R, T, B, rad):
    X = lambda d: L + (d - d0).days / (d1 - d0).days * (W - L - R)
    Y = lambda b: T + (hi - b) / (hi - lo) * (H - T - B)          # more births higher up
    return X, Y, ['<circle cx="%.2f" cy="%.2f" r="%s" fill="#222"/>' % (X(d), Y(b), rad) for d, b in rows]

# I: the plot, plain axes, ticks and labels
W, H, L, R, T, B = 1100, 500, 80, 20, 20, 50
X, Y, c = dots(W, H, L, R, T, B, "1.3")
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="DejaVu Sans, sans-serif" font-size="13">' % (W, H),
       '<rect width="%d" height="%d" fill="#ffffff"/>' % (W, H)]
for b in range(lo, hi + 1, 2000):
    svg.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#dddddd"/>' % (L, W - R, Y(b), Y(b)))
    svg.append('<text x="%d" y="%.1f" text-anchor="end" fill="#333">%s</text>' % (L - 8, Y(b) + 4, format(b, ",")))
for y in range(2000, 2016):
    x = X(datetime.date(y, 1, 1))
    svg.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="#333"/>' % (x, x, H - B, H - B + 5))
    if y < 2015:
        svg.append('<text x="%.1f" y="%d" text-anchor="middle" fill="#333">%d</text>' % (X(datetime.date(y, 7, 2)), H - B + 20, y))
svg.append('<line x1="%d" x2="%d" y1="%d" y2="%d" stroke="#333"/>' % (L, W - R, H - B, H - B))
svg.append('<line x1="%d" x2="%d" y1="%d" y2="%d" stroke="#333"/>' % (L, L, T, H - B))
svg.append('<text x="%.1f" y="%d" text-anchor="middle" fill="#333">date</text>' % ((L + W - R) / 2, H - 8))
svg.append('<text transform="translate(18 %.1f) rotate(-90)" text-anchor="middle" fill="#333">births in the United States that day</text>' % ((T + H - B) / 2))
svg += c + ["</svg>"]
open(os.path.join(M, "births.svg"), "w", encoding="utf-8").write("\n".join(svg))

# L: the same dots, small, with nothing to calibrate them by (no axes, ticks, numbers or words)
W, H = 480, 220
X, Y, c = dots(W, H, 6, 6, 6, 6, "0.8")
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d">' % (W, H), '<rect width="%d" height="%d" fill="#ffffff"/>' % (W, H)] + c + ["</svg>"]
open(os.path.join(M, "lossy.svg"), "w", encoding="utf-8").write("\n".join(svg))

ARMS = {
    "T": ("births.csv", "as a table (`births.csv`, one row per day: year, month, day of the month, day of the week, births)"),
    "I": ("births.png", "as a picture (`births.png`, a plot with one dot per day, with axes)"),
    "L": ("births.jpg", "as a picture (`births.jpg`, a small, compressed plot with one dot per day, without axes or numbers)"),
}
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
arms = ["T"] * 4 + ["I"] * 4 + ["L"] * 4
random.Random(121).shuffle(arms)
plan = []
for i, a in enumerate(arms, 1):
    m = "m%02d" % i
    base = "/tmp/claude-0/s121/mk/%s" % m
    fn, desc = ARMS[a]
    text = BRIEF.replace("{FOLDER}", base + "/work").replace("{SCRATCH}", base + "/scratch").replace("{FILE}", fn).replace("{AS}", desc)
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(text)
    plan.append({"maker": m, "arm": a, "folder": base + "/work", "scratch": base + "/scratch", "file": fn})
json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print(len(rows), [p["arm"] for p in plan])
