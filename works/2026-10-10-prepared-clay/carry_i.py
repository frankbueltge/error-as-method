"""carry_i.py -- M3 for arm I: decodes what each picture-arm page carries, by each page's own encoding
(read by hand from its code), and compares it with the source. m02: one character per year from 812,
'.' = none, day = code - 65 + 80 (its own loop). m09: 'gap.day' tokens, year starts at 800 (its own loop).
m01: static SVG; ring radius r = 9 + 0.28418*(year-812) from its innermost and outermost rings (812 and 2026;
its year labels sit about 3 px inside their rings, and a first decode from them was wrong), angle from the top
clockwise = (day-1)*360/365 (its month labels suggested day-0.5, which put 812, 1323 and 2026 one day early); centre (385,400). m10: static SVG; 13 columns at
x = 86.25 + 76.9225*k (k = century - 8), 1.45 px per day about day 105 at the column centre, row
y = 144.93 + 5.85*(year mod 100), all from its own labels and first marks. Decoded geometry is rounded
to whole years and days."""
import csv, json, math, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
COL = "Day of the year with peak cherry blossom"
truth = {int(r["Year"]): int(r[COL]) for r in csv.DictReader(open(os.path.join(HERE, "sources", "owid-kyoto-cherry-blossom.csv"), encoding="utf-8")) if r[COL]}
read = lambda m: open(os.path.join(HERE, "makers", m, "index.html"), encoding="utf-8").read()

def m02():
    s = read("m02"); raw = re.search(r'const DATA = "((?:[^"\\]|\\.)*)"', s).group(1).encode().decode("unicode_escape")
    return {812 + i: ord(c) - 65 + 80 for i, c in enumerate(raw) if c != "."}
def m09():
    s = read("m09"); raw = re.search(r'const RAW = "([^"]*)"', s).group(1); yr, out = 800, {}
    for t in raw.split():
        g, d = map(int, t.split(".")); yr += g; out[yr] = d
    return out
def m01():
    s = read("m01"); g = s[s.find('class="dots"'):]; g = g[:g.find("</g>")]; out = {}
    for cx, cy in re.findall(r'cx="([\d.]+)" cy="([\d.]+)"', g):
        dx, dy = float(cx) - 385, float(cy) - 400
        r = math.hypot(dx, dy); a = math.degrees(math.atan2(dx, -dy)) % 360
        out.setdefault(round(812 + (r - 9) / 0.28418), round(a * 365 / 360 + 1))
    return out
def m10():
    s = read("m10"); g = s[s.find('<g fill="#c4416a">'):]; g = g[:g.find("</g>")]; out = {}
    for cx, cy in re.findall(r'cx="([\d.]+)" cy="([\d.]+)"', g):
        x, y = float(cx), float(cy); k = round((x - 86.25) / 76.9225)
        out.setdefault(800 + 100 * k + round((y - 144.93) / 5.85), round(105 + (x - (86.25 + 76.9225 * k)) / 1.45))
    return out

res = {}
for m, f in [("m01", m01), ("m02", m02), ("m09", m09), ("m10", m10)]:
    got = f(); both = [y for y in got if y in truth]
    res[m] = {"pairs": len(got), "years_in_source": len(both), "years_not_in_source": sorted(set(got) - set(truth)),
              "source_years_missing": len(set(truth) - set(got)), "exact": sum(got[y] == truth[y] for y in both),
              "mae_days": round(sum(abs(got[y] - truth[y]) for y in both) / len(both), 3),
              "max_err": max(abs(got[y] - truth[y]) for y in both), "checks": {y: got.get(y) for y in (812, 1323, 1409, 2021, 2023, 2026)}}
    print(m, {k: (v if k != "years_not_in_source" else v[:12]) for k, v in res[m].items()})
json.dump(res, open(os.path.join(HERE, "carry_i.json"), "w"), indent=1)
