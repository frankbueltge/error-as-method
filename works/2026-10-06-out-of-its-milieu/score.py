"""Score the pre-registered predictions from the readings' blind tags and home.json. Strict rules only;
the post-hoc layer (POSTHOC below) is written after home.py ran and is reported beside, never instead."""
import json, re, glob
H = json.load(open("home.json"))
tags = {}
for p in sorted(glob.glob("readings/R-*.md")):
    for k, t in re.findall(r"^- \*\*([EMG]\d) ([GH])\b", open(p).read(), re.M): tags[k] = t
assert len(tags) == 16, tags
inst = lambda k: {"E": "ear", "M": "mould", "G": "grid24"}[k[0]]
claims = [{"id": k, "instrument": inst(k), "blind": t, "verdict": H[k]["verdict"], "match": t == H[k]["verdict"]} for k, t in tags.items()]
new = {"E3", "E4"}  # declared new (not K1-K6) in R-1, at claim time
# POSTHOC (written after home.py ran; see the journal): for claims tagged G that the check called H,
# what the per-second series shows of the feature itself.
POSTHOC = {
 "E3": "G, size wrong: the 60 s line is real and dashed, ratio 0.9-1.4 at 00-04 UTC and up to 5.3 at 06 UTC; the month-mean ratio 2.75 fell under the bar of 3",
 "E4": "G, check wrong: the check measured 1 s increments (min hour 0.79 of median); in the band the ear heard (11-150 s) the night hours 00-03 UTC hold 0.37-0.47 of the median energy",
 "E7": "G, size wrong: 94.1 % of seconds within +/-0.125 Hz, against a claimed 95 %",
 "M1": "G, size wrong: 69.7 % of cells dip below 50 Hz, against a claimed 70 %",
 "M2": "G, size wrong: 22.4 % of cells reach 49.9 Hz, against a claimed 25 %"}
dec = [c for c in claims if c["verdict"] in "GH"]
nH = sum(c["verdict"] == "H" for c in dec); nm = sum(c["match"] for c in dec)
share = {i: [sum(c["verdict"] == "G" for c in dec if c["instrument"] == i), sum(c["instrument"] == i for c in dec)] for i in ("ear", "mould", "grid24")}
r = lambda i: share[i][0] / share[i][1]
# LITERATURE: the second adjudicator named in PREDICTIONS.md step 4, read after home.py ran.
LIT = {
 "E3": "G: a one-minute pattern in GB frequency is reported, 'a persistent one-minute oscillatory pattern' traced to battery storage energy management, its amplitude 'increased substantially in the Nordic and British grids' (Hartmann et al. 2025, arXiv:2510.09862)",
 "E1": "G in kind: 'regular power dispatch actions every 15 minutes are clearly observable in the ... British (GB) ... grids' (Rydin Gorjao et al. 2020, arXiv:2006.02481); the half-hour itself not named there",
 "E7": "consistent: NESO's operational target is 'within 0.2Hz of 50Hz in normal conditions' (neso.energy, What is frequency?)"}
R = {"claims": claims, "posthoc": POSTHOC, "literature": LIT,
 "P1": {"rule": "H >= half of decided", "value": f"{nH}/{len(dec)}", "holds": nH * 2 >= len(dec)},
 "P2": {"rule": "a claim G and new", "value": [c["id"] for c in dec if c["id"] in new and c["verdict"] == "G"], "holds": any(c["id"] in new and c["verdict"] == "G" for c in dec),
        "posthoc": "E3 and E4 both true of the grid (see posthoc); P2 would hold", "literature": "E3 is G by the literature (arXiv:2510.09862); with the literature deciding, P2 holds"},
 "P3": {"rule": "blind tag matches >= 70 %", "value": f"{nm}/{len(dec)}", "holds": nm / len(dec) >= 0.7,
        "posthoc": "by kind (instrument vs grid feature) 16/16: every H-tag confirmed, every G-tagged feature present in the grid; the five misses are sizes and one check"},
 "P4": {"rule": "ear lowest share of G, grid24 highest", "value": {i: f"{a}/{b}" for i, (a, b) in share.items()},
        "holds": r("ear") < min(r("mould"), r("grid24")) and r("grid24") > max(r("ear"), r("mould")), "note": "ear and mould tie at 25 %"},
 "P5": {"rule": "ear rhythm finds the day; mould floor pale", "value": "day found at 1.959 s; floor dark", "holds": False},
 "F2": {"rule": ">= 8 decided claims", "value": len(dec), "fires": len(dec) < 8},
 "F4": {"rule": "every claim tagged H and H", "fires": all(c["blind"] == "H" == c["verdict"] for c in dec)}}
json.dump(R, open("results.json", "w"), indent=1)
for k in ("P1", "P2", "P3", "P4", "P5"): print(k, R[k]["value"], "holds" if R[k]["holds"] else "FAILS")
