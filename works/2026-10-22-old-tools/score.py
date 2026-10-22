"""score.py: joins the blind codes to the keys and the arms, and scores P1-P7 and S142.SHELF as fixed in
PREDICTIONS.md. P5, P6, P7 and the S142.SHELF grouping are the practice's readings, written into READINGS
below from the rooms' CHOICE.md and NOTE.md before this file was first run."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); J = lambda p: json.load(open(os.path.join(H, p)))
plan = {r["room"]: r["arm"] for r in J("plan.json")["rooms"]}
NAME = {"P": "PLOT", "C": "CYCLES", "G": "GAPS", "D": "DIGITS"}
skey = {v: k for k, v in J("coder/shelf-key.json").items()}          # instrument name -> S label
key = J("coder/key.json"); A = {c["id"]: c for c in J("coder/codes-A.json")}
byA = {key[x]: A[x] for x in key}
keyB = J("coder/key-B.json"); B = {c["id"]: c for c in J("coder/codes-B.json")}
byB = {keyB[y]: B[y] for y in keyB}
hit = lambda r, shelf: byA[r][skey[shelf]]["code"] in ("SAME", "KIN")
INST = sorted(r for r in plan if plan[r] != "P")

READINGS = {
 # P5: is the chosen material one of the maker's own first three (same dataset or same phenomenon from the same publisher)?
 "P5": {"r01": True, "r02": True, "r03": True, "r04": True, "r05": True, "r06": True, "r07": True, "r08": True,
        "r09": True, "r10": True, "r11": False, "r12": True, "r13": True, "r14": True, "r15": True, "r16": True},
 # P6: FIRST DIGITS choices that are counts of people, areas or money (house prices r07, payments r03: yes; asteroid diameters r02, r12: no)
 "P6": {"r02": False, "r03": True, "r07": True, "r12": False},
 # P7: data re-fetchable or row-matched by the practice (see sources/refetch.txt)
 "P7": None,
 # S142.SHELF: the practice's grouping of the sixteen choices into items
 "ITEMS": {"r01": "NYC 311 noise complaints", "r13": "NYC 311 noise complaints", "r02": "JPL asteroid diameters",
           "r12": "JPL asteroid diameters", "r06": "Billboard Hot 100 chart dates", "r08": "Billboard Hot 100 chart dates",
           "r03": "UK government spending over 25k", "r04": "England and Wales measles", "r05": "US weekly gasoline price",
           "r07": "UK house prices paid", "r09": "Curiosity rover weather", "r10": "Great Lakes water levels",
           "r11": "xkcd publication dates", "r14": "US influenza-like illness", "r15": "Bank of England Bank Rate",
           "r16": "Lake Mendota ice"},
 # S142.SHELF second clause: items that stand among the first three of each maker (read from CHOICE.md)
 "FIRST3_SHARED": {"Melbourne pedestrian counts": ["r01", "r04", "r13", "r14"],
                   "US weekly gasoline price": ["r01", "r05", "r10", "r16"],
                   "populations of towns or municipalities": ["r02", "r03", "r07", "r12"],
                   "global surface temperature (GISTEMP or kin)": ["r05", "r15", "r16"],
                   "Central England Temperature": ["r09", "r11"],
                   "Billboard Hot 100 chart dates": ["r06", "r08"],
                   "Astronomy Picture of the Day dates": ["r08", "r11"],
                   "asteroid diameters": ["r02", "r12"]},
}
try: READINGS["P7"] = J("sources/refetch.json")
except FileNotFoundError: pass

own = {r: hit(r, NAME[plan[r]]) for r in INST}
other = {s: sum(hit(r, s) for r in INST if NAME[plan[r]] != s) for s in ["CYCLES", "GAPS", "DIGITS"]}
own_by = {s: sum(own[r] for r in INST if NAME[plan[r]] == s) for s in ["CYCLES", "GAPS", "DIGITS"]}
# P2: per arm, own-shelf hits against hits of the same makers on each of the other two instrument shelves
p2 = {}
for s in ["CYCLES", "GAPS", "DIGITS"]:
    rs = [r for r in INST if NAME[plan[r]] == s]
    p2[s] = {"own": sum(hit(r, s) for r in rs), **{t: sum(hit(r, t) for r in rs) for t in ["CYCLES", "GAPS", "DIGITS"] if t != s}}
p2_holds = all(v["own"] > max(x for k, x in v.items() if k != "own") for v in p2.values())
gen = sum(hit(r, "GENERAL28") for r in plan)
met = [byB[r]["met"] for r in sorted(plan)]
items = READINGS["ITEMS"]; nitems = len(set(items.values()))
shared = max(len(v) for v in READINGS["FIRST3_SHARED"].values())
p7 = READINGS["P7"]
res = {
 "P1": {"own_shelf_hits": sum(own.values()), "of": len(INST), "by_arm": own_by, "holds": sum(own.values()) >= 8},
 "P2": {"by_arm": p2, "holds": p2_holds},
 "P3": {"general_shelf_hits": gen, "rooms": [r for r in sorted(plan) if hit(r, "GENERAL28")], "holds": gen <= 4},
 "P4": {"MET": met.count("MET"), "PARTLY": met.count("PARTLY"), "NOT_MET": met.count("NOT_MET"), "holds": met.count("MET") >= 10},
 "P5": {"among_first_three": sum(READINGS["P5"].values()), "holds": sum(READINGS["P5"].values()) >= 12},
 "P6": {"people_area_money": sum(READINGS["P6"].values()), "holds": sum(READINGS["P6"].values()) >= 3},
 "P7": {"refetched_or_matched": (sum(1 for v in p7.values() if v["ok"]) if p7 else None),
        "holds": (sum(1 for v in p7.values() if v["ok"]) >= 14) if p7 else None},
 "S142.SHELF": {"different_items": nitems, "largest_first_three_share": shared,
                "falsified": nitems >= 13 or shared < 8},
 "rooms": {r: {"arm": NAME[plan[r]], "item": items[r], "domain": byA[r]["domain"],
               "codes": {s: byA[r][skey[s]]["code"] for s in skey}, "met": byB[r]["met"],
               "specific": byB[r]["specific"], "met_reason": byB[r]["reason"]} for r in sorted(plan)}}
json.dump(res, open(os.path.join(H, "results.json"), "w"), indent=1, ensure_ascii=False)
for k in ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "S142.SHELF"]: print(k, res[k])
for r in sorted(plan): x = res["rooms"][r]; print(r, x["arm"], x["codes"], x["met"], x["item"])
