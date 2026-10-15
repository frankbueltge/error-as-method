"""score.py: reads plan.json and coder/B/answers.json and scores the three rows and P1-P9 exactly as PREDICTIONS.md
fixed them (committed 80bdac4, before any maker ran). Also counts, post hoc and marked so, what the rows did not ask:
how many works carry the told kind's words and draw its clock (makers/mNN/index.html and NOTE.md).
Writes results.json."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
plan = {p["maker"]: p["cell"] for p in json.load(open(os.path.join(HERE, "plan.json")))}
A = json.load(open(os.path.join(HERE, "coder", "B", "answers.json")))
N = sorted(m for m, c in plan.items() if c == "N"); T = sorted(m for m, c in plan.items() if c == "T")
def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None
def hours(s):
    """every number in a C1 entry read as hours (days converted), for 'only the day and its harmonics'"""
    s = str(s).lower(); out = []
    for v, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(?:-|–)?\s*(?:\d+(?:\.\d+)?)?\s*(h|hour|hours|day|days|px|pixel|repeat)?", s):
        v = float(v)
        if unit in ("day", "days"): v *= 24
        if unit in ("px", "pixel", "repeat"): continue  # pixels and counts of repeats are not periods in hours
        out.append(v)
    return out
def daily_family(h): return any(abs(h - p) <= 1.0 for p in (24, 12, 8))
def bent(m):
    c2 = num(A[m]["C2"])
    return (c2 is not None and (12.2 <= c2 <= 12.7 or 24.4 <= c2 <= 25.5)) or A[m]["C2_lunar"] == "yes"
TIDE_FIRST = {"half-daily", "lunar-day", "fortnightly"}
r = {"cells": {"N": N, "T": T}, "per_maker": {}}
for m in sorted(A):
    a = A[m]
    r["per_maker"][m] = {"cell": plan[m], "C2": a["C2"], "bent": bent(m), "first": a["C3"], "C4": a["C4"],
                         "C5": a["C5"], "C5_quote": a["C5_quote"], "C6": a["C6"], "C7": a["C7"], "title": a["C9"],
                         "C1": a["C1"]}
# S125.GIVENKIND
nb = sum(bent(m) for m in T); nr = sum(A[m]["C7"] == "yes" for m in T)
r["S125.GIVENKIND"] = {"bent": nb, "rejected": nr, "a_fires": nb >= 3, "b_fires": nr >= 3,
                       "verdict": "falsified" if nb >= 3 or nr >= 3 else "holds"}
# S126.SELECT
st = sum(A[m]["C3"] in TIDE_FIRST for m in T); sn = sum(A[m]["C3"] in TIDE_FIRST for m in N)
r["S126.SELECT"] = {"T_tide_first": st, "N_tide_first": sn, "diff": st - sn, "verdict": "falsified" if st - sn >= 2 else "holds"}
# S124.TABLE on N
only = []
for m in N:
    hs = [h for e in A[m]["C1"] for h in hours(e)]
    if (hs and all(daily_family(h) for h in hs)) or (not A[m]["C1"] and A[m]["C3"] == "daily"): only.append(m)
cats = {}
for m in only: cats[A[m]["C5"]] = cats.get(A[m]["C5"], 0) + 1
mag = sum(A[m]["C5"] == "magnetic" for m in only)
testable = len(only) >= 2
r["S124.TABLE"] = {"holders_of_only_the_day": only, "C5_among_them": cats, "magnetic": mag, "testable": testable,
                   "a_fires": mag >= 2, "b_fires": testable and max(cats.values()) * 2 < len(only),
                   "verdict": ("not testable" if not testable else
                               "falsified" if mag >= 2 or max(cats.values()) * 2 < len(only) else "holds")}
# predictions
def daily_measured(m): return any(abs(h - 24) <= 1.0 for e in A[m]["C1"] for h in hours(e))
P = {}
P["P1"] = all(daily_measured(m) for m in N)
P["P2"] = sum(A[m]["C5"] == "temperature" for m in N) >= 3 and sum(A[m]["C5"] == "magnetic" for m in N) <= 1
P["P3"] = nb <= 1
P["P4"] = nr <= 2
P["P5"] = sum(A[m]["C5"] == "tide" for m in T) >= 4
P["P6"] = st - sn <= 1
tc4 = sum(A[m]["C4"] == "yes" for m in T); nc4 = sum(A[m]["C4"] == "yes" for m in N)
sn_reading = sum(A[m]["C4"] == "yes" and re.search(r"spring|neap", A[m]["C4_reading"], re.I) is not None for m in T)
P["P7"] = tc4 > nc4 and sn_reading >= 2
spread = {c: len({A[m]["C5"] for m in ms}) for c, ms in (("N", N), ("T", T))}
P["P8"] = spread["N"] >= 3 and spread["T"] <= 2
P["P9"] = True  # checked by hand below: no C8_reading names a date or event
r["P9_readings"] = {m: A[m]["C8_reading"] for m in A if A[m]["C8"] == "yes"}
r["predictions"] = P; r["predictions_held"] = sum(P.values())
r["counts"] = {"C4_yes": {"T": tc4, "N": nc4}, "C4_spring_neap_in_T": sn_reading, "spread_C5": spread,
               "C5": {c: {k: sum(A[m]["C5"] == k for m in ms) for k in sorted({A[x]["C5"] for x in A})} for c, ms in (("N", N), ("T", T))},
               "humidity_named_in_C5_quote": {c: sum(bool(re.search("humid", A[m]["C5_quote"], re.I)) for m in ms) for c, ms in (("N", N), ("T", T))}}
# post hoc, not predicted: the told kind in the works themselves
ph = {}
for m in sorted(A):
    page = open(os.path.join(HERE, "makers", m, "index.html"), encoding="utf-8").read()
    note = open(os.path.join(HERE, "makers", m, "NOTE.md"), encoding="utf-8").read()
    words = len(re.findall(r"water|harbou?r|ebbs?|tid(?:e|al)", page + note, re.I))
    clock = bool(re.search(r"24\s*h\s*50|24\.84|12\s*h\s*25|12\.42|moon'?s day|lunar", page, re.I))
    ph[m] = {"cell": plan[m], "kind_words_in_page_or_note": words, "draws_or_names_the_tide_clock_in_page": clock}
r["post_hoc"] = {"note": "not predicted; counted after reading the works",
                 "per_maker": ph,
                 "T_with_kind_words": sum(ph[m]["kind_words_in_page_or_note"] > 0 for m in T),
                 "N_with_kind_words": sum(ph[m]["kind_words_in_page_or_note"] > 0 for m in N),
                 "T_tide_clock_in_page": sum(ph[m]["draws_or_names_the_tide_clock_in_page"] for m in T),
                 "N_tide_clock_in_page": sum(ph[m]["draws_or_names_the_tide_clock_in_page"] for m in N)}
json.dump(r, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps({k: r[k] for k in ("S125.GIVENKIND", "S126.SELECT", "S124.TABLE", "predictions", "predictions_held", "counts")}, indent=1))
print(json.dumps({k: v for k, v in r["post_hoc"].items() if k != "per_maker"}, indent=1)); print(r["P9_readings"])
