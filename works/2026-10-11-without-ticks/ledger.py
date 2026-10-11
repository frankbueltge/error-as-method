"""ledger.py -- written AFTER the makers and the coder (post hoc, declared as such). Two things:
1. M1 as pre-registered, coded by the practice from each maker's scratch scripts, page and report (CODES below,
   with the evidence for each), plus a post-hoc code of the UNIT each page carries: ROW (the table's rows), DAY (one
   reconstructed value per day, fitted from the picture) or PIXEL (the picture's own pixels, with their darkness).
2. A ledger of what each maker NAMED, searched in NOTE.md + report + the page's source (lower-cased), for seven
   things this material is known for. The patterns are mine and post hoc; the pre-registered keyword count is
   features.py. Writes ledger.json."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
CODES = {  # maker: (M1 codes, unit, evidence)
 "m01": (["DECODE", "EMBED"], "PIXEL", "report: ImageMagick to raw greyscale; 'every pixel darker than the background (about 22,000) went into a compact string inside the page'"),
 "m02": (["TABLE"], "ROW", "scratch explore.py/resid.py parse births.csv; page carries 5,479 cells"),
 "m03": (["DECODE"], "DAY", "scratch dots.py/mass.py/poisson.py: blobs to dots, hidden days added by a Poisson correction; page carries reconstructed days"),
 "m04": (["DECODE"], "DAY", "scratch decode.py/fit.py: discs fitted to ink, 5,501 dots; page carries reconstructed days"),
 "m05": (["DECODE", "EMBED"], "PIXEL", "report: 'kept the cropped pixel darkness (470x174) and embedded it in the page as base64'"),
 "m06": (["DECODE", "EMBED"], "PIXEL", "report: 'kept every pixel darker than a threshold (15,742 of them), with its position and darkness, and packed them into the page'"),
 "m07": (["DECODE", "EMBED"], "PIXEL", "scratch ink.py/encode.py: ink per source pixel, run-length encoded into the page; 'each source pixel column becomes a short streak'"),
 "m08": (["TABLE"], "ROW", "scratch explore.py parses births.csv; page carries 5,479 values"),
 "m09": (["DECODE"], "DAY", "scratch decode.py/blobs.py/dots.py: blobs split into 4,995 dots; page carries reconstructed days"),
 "m10": (["DECODE", "EMBED"], "PIXEL", "report: 'I kept every inked pixel of the source as a point: 15,743 pixels, with their darkness, stored inside the page'"),
 "m11": (["TABLE"], "ROW", "scratch explore.py parses births.csv; page carries 5,479 counts as one string"),
 "m12": (["TABLE"], "ROW", "scratch explore.py/ex2.py parse births.csv; page carries one list of daily counts"),
}
FORM = {  # post hoc, the practice's own reading of the twelve screenshots: what the form does with time
 "m01": "FOLD-RADIAL", "m02": "FOLD-GRID", "m03": "NO-TIME", "m04": "NO-TIME", "m05": "FOLD-LINEAR", "m06": "FOLD-RADIAL",
 "m07": "FOLD-LINEAR", "m08": "FOLD-LINEAR", "m09": "FOLD-RADIAL", "m10": "FOLD-RADIAL", "m11": "FOLD-GRID", "m12": "FOLD-LINEAR"}
NAMED = {
 "the week (two bands)": r"weekday|weekend|working week|monday|saturday|sunday",
 "holidays": r"christmas|new year|thanksgiving|4 jul|july 4|fourth of july|labor day",
 "the September swell": r"september|\bsep\b|late summer",
 "the peak around 2007": r"2007|2006.08|boom",
 "repeating dates (9.9.09 …)": r"9\.9\.09|9/9/09|11\.11\.11|11/11/11|12\.12\.12|12/12/12|6\.6\.06|6/6/06|8\.8\.08",
 "the 13th": r"13th|friday the 13",
 "one day's exact count": r"(?<!\d)(?<!\d,)(16,081|5,728)(?!\d)(?!,\d)",  # comma forms, not inside packed data strings
}
plan = json.load(open(os.path.join(HERE, "plan.json")))
out = {}
for p in plan:
    m = p["maker"]; txt = ""
    for f in (os.path.join(HERE, "makers", m, "NOTE.md"), os.path.join(HERE, "reports", m + ".md"), os.path.join(HERE, "makers", m, "index.html")):
        txt += open(f, encoding="utf-8").read().lower() + "\n"
    c, u, ev = CODES[m]
    out[m] = {"arm": p["arm"], "m1": c, "unit": u, "form": FORM[m], "evidence": ev, "named": {k: bool(re.search(r, txt)) for k, r in NAMED.items()}}
json.dump(out, open(os.path.join(HERE, "ledger.json"), "w"), indent=1)
for arm in "TIL":
    ms = [m for m in out if out[m]["arm"] == arm]
    print(arm, "units", [out[m]["unit"] for m in ms], [out[m]["form"] for m in ms], {k: sum(out[m]["named"][k] for m in ms) for k in NAMED})
