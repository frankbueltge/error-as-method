"""score.py: joins the blind codes to the key and the arms, and scores P1-P4 and P6 as fixed in PREDICTIONS.md.
P5 and P7 are the practice's readings, written into READINGS below before running and scored here."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); J = lambda p: json.load(open(os.path.join(H, p)))
key = J("coder/key.json"); codes = {c["id"]: c for c in J("coder/codes.json")}
arm = {r["room"]: r["arm"] for r in J("plan.json")["rooms"]}
by = {key[m]: codes[m] for m in key}
N = sorted(r for r in arm if arm[r] == "N"); L = sorted(r for r in arm if arm[r] == "L")
X = sorted(k for k in by if k.startswith("X"))
cnt = lambda rs, cs: sum(by[r]["code"] in cs for r in rs)
# P5: does an L choice fall in a listed domain (by the list's own words)? P7: is the choice among the maker's
# own first three (same dataset, or same phenomenon from the same publisher)? Read from CHOICE.md by the practice.
READINGS = {"P5": {"r06": False, "r07": False, "r08": False, "r10": False, "r11": False, "r12": False},
            "P7": {"r01": True, "r02": True, "r03": True, "r04": True, "r05": True, "r06": False, "r07": True,
                   "r08": True, "r09": False, "r10": True, "r11": True, "r12": True}}
fetched = {r: True for r in arm}  # rooms/MANIFEST.json against sources/refetch.txt; r07 by its Overpass header
dom = [by[r]["domain"] for r in N]
res = {
 "P1": {"N_SAME": cnt(N, ["SAME"]), "holds": cnt(N, ["SAME"]) >= 4},
 "P2": {"L_SAME_KIN": cnt(L, ["SAME", "KIN"]), "L_SAME": cnt(L, ["SAME"]), "holds": cnt(L, ["SAME", "KIN"]) >= 4},
 "P3": {"line_SAME": cnt(X, ["SAME"]), "line_KIN": cnt(X, ["KIN"]), "holds": cnt(X, ["SAME"]) <= 9},
 "P4": {"N_domains": dom, "distinct": len(set(dom)), "holds": len(set(dom)) < len(dom)},
 "P5": {"in_listed_domain": sum(READINGS["P5"].values()), "holds": sum(READINGS["P5"].values()) == 0},
 "P6": {"fetched": sum(fetched.values()), "holds": sum(fetched.values()) >= 11},
 "P7": {"among_first_three": sum(READINGS["P7"].values()), "holds": sum(READINGS["P7"].values()) >= 9},
 "rooms": {r: {"arm": arm[r], **by[r]} for r in sorted(arm)},
 "line": {x: by[x] for x in X}}
json.dump(res, open(os.path.join(H, "results.json"), "w"), indent=1, ensure_ascii=False)
for k in ["P1","P2","P3","P4","P5","P6","P7"]: print(k, {a: b for a, b in res[k].items()})
for r in sorted(arm): print(r, arm[r], by[r]["code"], by[r]["domain"])
