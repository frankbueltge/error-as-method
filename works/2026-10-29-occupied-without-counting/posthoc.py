"""Session 161, POST HOC: written after results.json was read. Nothing here was predicted.
Questions: (1) where do the describers' p50s stand relative to the family's own value: on it, one whole step toward the
scale's middle, on the people's, elsewhere? (2) does arm F's lower error come from the space between the steps?
(3) how many of the family's own ratings follow the sentence's position alone?
Run: python3 posthoc.py   (reads results.json, plan.json, people.json, rooms/; writes posthoc.json)
"""
import json, re, statistics as st
from pathlib import Path
HERE = Path(__file__).parent
plan = json.load(open(HERE / "plan.json")); people = json.load(open(HERE / "people.json"))
res = json.load(open(HERE / "results.json"))
KEYS = [k["key"] for k in plan["keys"]]; cond = {k["key"]: k["cond"] for k in plan["keys"]}
A = res["A"]; ppl = res["people_median"]; div = res["diverging"]

def p50s(letter):
    out = {}
    for i in range(1, 7):
        m = f"{letter}{i}"; order = plan["orders"][m]
        for line in (HERE / "rooms" / f"{m}.txt").read_text().splitlines():
            mm = re.match(r"\s*(\d+)\s*:.*p50=(-?[\d.]+)", line)
            if mm and 1 <= int(mm.group(1)) <= 32:
                v = float(mm.group(2)); out[(m, order[int(mm.group(1)) - 1])] = v if letter == "S" else 1 + 6 * v / 100
    return out

def toward_mid(a):
    return a + 1 if a < 4 else a - 1 if a > 4 else a

out = {}
for L in ("S", "F"):
    d = p50s(L); kinds = {"on the family's own value": 0, "one step toward the middle": 0, "on the people's": 0, "other": 0}
    for (m, k), v in d.items():
        a = A[k]
        if a != int(a): kinds["other"] += 1; continue      # half-step family medians: not classifiable this way
        if abs(v - toward_mid(a)) < 0.06 and abs(toward_mid(a) - ppl[k]) >= 0.06: kinds["one step toward the middle"] += 1
        elif abs(v - a) < 0.06 and abs(a - ppl[k]) >= 0.06: kinds["on the family's own value"] += 1
        elif abs(v - ppl[k]) < 0.06: kinds["on the people's"] += 1
        else: kinds["other"] += 1
    out[L] = {"placements": len(d), "kinds": kinds}
# (1b) how far from the family's own value, against how far the people are
for L in ("S", "F"):
    d = p50s(L)
    near = sum(1 for (m, k), v in d.items() if abs(v - A[k]) <= 1.06)
    far = [(m, k) for (m, k) in d if abs(ppl[k] - A[k]) >= 1.5]
    near_far = sum(1 for (m, k) in far if abs(d[(m, k)] - A[k]) <= 1.06)
    out[L]["within_one_step_of_family"] = near
    out[L]["keys_people_1.5_or_more_away_placements"] = len(far)
    out[L]["of_those_within_one_step_of_family"] = near_far
# (2) arm F snapped to the nearest whole step, mean error on the diverging keys
F = p50s("F"); S = p50s("S")
def mae(d, snap=False):
    P = {k: st.mean([(round(v) if snap else v) for (m, kk), v in d.items() if kk == k]) for k in KEYS}
    return st.mean(abs(P[k] - ppl[k]) for k in div)
out["mae"] = {"S": mae(S), "F": mae(F), "F_snapped_to_steps": mae(F, True)}
# (3) the family's own ratings by position
ratings = {"insitu": [], "extrap": []}
for i in range(1, 7):
    m = f"A{i}"; order = plan["orders"][m]
    for line in (HERE / "rooms" / f"{m}.txt").read_text().splitlines():
        mm = re.match(r"\s*(\d+)\s*:\s*(\d+)\s*$", line)
        if mm and 1 <= int(mm.group(1)) <= 32:
            ratings[cond[order[int(mm.group(1)) - 1]].split("/")[2]].append(int(mm.group(2)))
out["family_by_position"] = {p: {str(v): r.count(v) for v in range(1, 8) if r.count(v)} for p, r in ratings.items()}
pp = {"insitu": [], "extrap": []}
for k in KEYS: pp[cond[k].split("/")[2]] += people[k]["ratings"]
out["people_by_position"] = {p: {str(v): r.count(v) for v in range(1, 8)} for p, r in pp.items()}
out["people_median_by_position"] = {p: sorted(ppl[k] for k in KEYS if cond[k].endswith(p)) for p in ("insitu", "extrap")}
json.dump(out, open(HERE / "posthoc.json", "w"), indent=1)
print(json.dumps(out, indent=1))
