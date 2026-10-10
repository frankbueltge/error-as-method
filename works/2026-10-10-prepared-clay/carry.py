"""carry.py -- M2 and M3: what each page carries of the material, read mechanically from index.html.
Year-day pairs are found three ways: literal pairs ("812,92", [812,92], {y:812,d:92}); parallel arrays
(a list of >=100 years in 812..2026 and a list of days in 60..150 of equal length); and a year-keyed
object ("812:92"). The largest set found counts. Each count was checked against the code by hand
(results.json says where the mechanical reading needed help). MAE is against the source, over matched years."""
import csv, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
COL = "Day of the year with peak cherry blossom"
truth = {int(r["Year"]): int(r[COL]) for r in csv.DictReader(open(os.path.join(HERE, "sources", "owid-kyoto-cherry-blossom.csv"), encoding="utf-8")) if r[COL]}

def pairs_literal(s):
    out = {}
    for y, d in re.findall(r"(?<![\d.])(\d{3,4})\s*[,:]\s*(?:d\s*:\s*)?(\d{2,3})(?![\d.])", s):
        y, d = int(y), int(d)
        if 812 <= y <= 2026 and 60 <= d <= 150:
            out.setdefault(y, d)
    return out

def pairs_arrays(s):
    lists = [[int(x) for x in re.findall(r"-?\d+", L)] for L in re.findall(r"\[([\d,\s\-]{300,})\]", s)]
    ys = [L for L in lists if len(L) >= 100 and all(812 <= v <= 2026 for v in L)]
    ds = [L for L in lists if len(L) >= 100 and all(60 <= v <= 150 for v in L)]
    best = {}
    for Y in ys:
        for D in ds:
            if len(Y) == len(D):
                cand = dict(zip(Y, D))
                if len(cand) > len(best):
                    best = cand
    return best

res = {}
for p in json.load(open(os.path.join(HERE, "plan.json"))):
    f = os.path.join(HERE, "makers", p["maker"], "index.html")
    s = open(f, encoding="utf-8").read()
    a, b = pairs_literal(s), pairs_arrays(s)
    got = a if len(a) >= len(b) else b
    m = [y for y in got if y in truth]
    mae = round(sum(abs(got[y] - truth[y]) for y in m) / len(m), 2) if m else None
    exact = sum(1 for y in m if got[y] == truth[y])
    res[p["maker"]] = {"arm": p["arm"], "bytes": len(s.encode()), "pairs": len(got), "matched_years": len(m),
                       "exact": exact, "mae_days": mae, "how": "literal" if got is a else "arrays",
                       "template_phrase": ("came into full bloom" in s), "embedded_image": ("data:image" in s)}
    print(p["maker"], res[p["maker"]])
json.dump(res, open(os.path.join(HERE, "carry.json"), "w"), indent=1)
