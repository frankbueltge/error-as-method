"""prepare.py -- one material, three preparations. Reads the committed OWID file (sources/), writes
materials/bloom.csv (T), materials/bloom.txt (P) and materials/bloom.svg (I, rendered to bloom.png by
render_png.js), assigns twelve makers to the three arms with seed 119, and writes one brief per maker
to briefs/run/ and the plan to plan.json. Every maker gets the same brief; only the sentence naming
the file differs. Run: python3 prepare.py && node render_png.js"""
import csv, json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources", "owid-kyoto-cherry-blossom.csv")
COL = "Day of the year with peak cherry blossom"
rows = [(int(r["Year"]), int(r[COL])) for r in csv.DictReader(open(SRC, encoding="utf-8")) if r[COL]]
assert len(rows) == 838 and rows[0] == (812, 92) and rows[-1] == (2026, 88)
M = os.path.join(HERE, "materials")
os.makedirs(M, exist_ok=True)

# T: the table
with open(os.path.join(M, "bloom.csv"), "w", encoding="utf-8", newline="\n") as f:
    f.write("year,day_of_year\n")
    for y, d in rows:
        f.write("%d,%d\n" % (y, d))

# P: the same values as sentences, one per year, one template (the variable is the format, not the wording)
def ordinal(n):
    s = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return "%d%s" % (n, s)

with open(os.path.join(M, "bloom.txt"), "w", encoding="utf-8", newline="\n") as f:
    for y, d in rows:
        f.write("In %d, the cherry trees of Kyoto came into full bloom on the %s day of the year.\n" % (y, ordinal(d)))

# I: the same values as a plot, one dot per year, plain axes
W, H, L, R, T, B = 1100, 500, 70, 20, 20, 50
x0, x1, y0, y1 = 800, 2030, 80, 128
X = lambda y: L + (y - x0) / (x1 - x0) * (W - L - R)
Y = lambda d: T + (d - y0) / (y1 - y0) * (H - T - B)   # later days lower down
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="DejaVu Sans, sans-serif" font-size="13">' % (W, H),
       '<rect width="%d" height="%d" fill="#ffffff"/>' % (W, H)]
for d in range(80, 129, 10):
    svg.append('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" stroke="#dddddd"/>' % (L, W - R, Y(d), Y(d)))
    svg.append('<text x="%d" y="%.1f" text-anchor="end" fill="#333">%d</text>' % (L - 8, Y(d) + 4, d))
for y in range(800, 2031, 100):
    svg.append('<line x1="%.1f" x2="%.1f" y1="%d" y2="%d" stroke="#333"/>' % (X(y), X(y), H - B, H - B + 5))
    svg.append('<text x="%.1f" y="%d" text-anchor="middle" fill="#333">%d</text>' % (X(y), H - B + 20, y))
svg.append('<line x1="%d" x2="%d" y1="%d" y2="%d" stroke="#333"/>' % (L, W - R, H - B, H - B))
svg.append('<line x1="%d" x2="%d" y1="%d" y2="%d" stroke="#333"/>' % (L, L, T, H - B))
svg.append('<text x="%.1f" y="%d" text-anchor="middle" fill="#333">year</text>' % ((L + W - R) / 2, H - 8))
svg.append('<text transform="translate(18 %.1f) rotate(-90)" text-anchor="middle" fill="#333">day of the year of full bloom</text>' % ((T + H - B) / 2))
for y, d in rows:
    svg.append('<circle cx="%.1f" cy="%.1f" r="2.2" fill="#222"/>' % (X(y), Y(d)))
svg.append("</svg>")
open(os.path.join(M, "bloom.svg"), "w", encoding="utf-8").write("\n".join(svg))

ARMS = {
    "T": ("bloom.csv", "as a table (`bloom.csv`, one row per year: the year and the day of the year)"),
    "P": ("bloom.txt", "as sentences (`bloom.txt`, one sentence per year)"),
    "I": ("bloom.png", "as a picture (`bloom.png`, a plot with one dot per year)"),
}
BRIEF = open(os.path.join(HERE, "briefs", "BRIEF.md"), encoding="utf-8").read()
arms = ["T"] * 4 + ["P"] * 4 + ["I"] * 4
random.Random(119).shuffle(arms)
plan = []
for i, a in enumerate(arms, 1):
    m = "m%02d" % i
    folder = "/tmp/claude-0/s119/mk/%s/work" % m
    fn, desc = ARMS[a]
    text = BRIEF.replace("{FOLDER}", folder).replace("{FILE}", fn).replace("{AS}", desc)
    open(os.path.join(HERE, "briefs", "run", m + ".md"), "w", encoding="utf-8").write(text)
    plan.append({"maker": m, "arm": a, "folder": folder, "file": fn})
json.dump(plan, open(os.path.join(HERE, "plan.json"), "w"), indent=1)
print(len(rows), [p["arm"] for p in plan])
