"""features.py -- M3, mechanically: which feature words each maker's NOTE.md and report contain. The lists are
copied from PREDICTIONS.md (committed before any maker ran). Case-insensitive substring match; crude by design."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
LISTS = {
 "weekly": ["weekend", "weekday", "saturday", "sunday", "seven-day", "day of the week", "week"],
 "holiday": ["christmas", "new year", "july 4", "fourth of july", "independence day", "thanksgiving", "holiday", "labor day", "memorial day"],
 "season": ["september", "summer", "season", "autumn", "fall", "august"],
 "decline": ["2007", "2008", "recession", "decline", "fell", "fewer", "drop"],
 "superstition": ["friday the 13", "13th", "superstition"],
 "inexact": ["approximate", "estimate", "not exact", "inexact", "relative", "uncalibrated", "no scale", "cannot be read", "can't be read", "could not", "lossy", "compress"],
}
out = {}
for p in json.load(open(os.path.join(HERE, "plan.json"))):
    m = p["maker"]
    txt = ""
    for f in (os.path.join(HERE, "makers", m, "NOTE.md"), os.path.join(HERE, "reports", m + ".md")):
        if os.path.exists(f): txt += open(f, encoding="utf-8").read().lower() + "\n"
    out[m] = {"arm": p["arm"], **{k: sorted({w for w in ws if w in txt}) for k, ws in LISTS.items()}}
json.dump(out, open(os.path.join(HERE, "features.json"), "w"), indent=1)
for arm in "TIL":
    ms = [m for m in out if out[m]["arm"] == arm]
    print(arm, {k: sum(1 for m in ms if out[m][k]) for k in LISTS})
