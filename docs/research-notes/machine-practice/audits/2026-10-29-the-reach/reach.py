"""Session 162, AUDIT (post hoc on committed data, nothing here was predicted).
Question: does S161.TETHER's claim -- a describer stands at most one whole step from the family's own median, however
far the people are -- describe experiments 40 and 41 too, whose data were committed before the claim was made?
This is not the row's event (the row asks for the NEXT experiment); it is a re-reading of the record the row cites.
Measure, as the row fixes it: on the far keys (people's median at least 1.5 steps from the family's median), the share
of describer placements (each describer's stated p50) lying more than 1.05 steps from the family's median.
Run: python3 reach.py   (reads ../../../../../works/...; writes results.json beside this file)
"""
import json, re, statistics as st
from pathlib import Path
HERE = Path(__file__).parent
W = HERE.parents[4] / "works"

def tally(rows):
    """rows: (key, A, people, [p50 per describer]) on one step-scale."""
    far = [r for r in rows if abs(r[2] - r[1]) >= 1.5]
    pl = [(k, a, p, v) for k, a, p, vs in far for v in vs]
    beyond = [x for x in pl if abs(x[3] - x[1]) > 1.05]
    reached = [x for x in pl if abs(x[3] - x[2]) < 0.5]                       # within half a step of the people
    return {"keys": len(rows), "far_keys": len(far), "far_placements": len(pl),
            "beyond_one_step": len(beyond), "share_beyond": round(len(beyond) / len(pl), 3) if pl else None,
            "reached_people": len(reached),
            "far_rows": [{"key": k, "A": a, "people": p, "p50s": vs,
                          "max_from_A": max(abs(v - a) for v in vs)} for k, a, p, vs in far]}

out = {}
# experiment 40, Without a Tongue: 1-9 liking, six describers P1-P6, P_raw = quantiles p10..p90 per describer
r40 = json.load(open(W / "2026-10-26-without-a-tongue/results.json"))
rows = [(k["food"], k["median"]["A"], k["median"]["people"], [q[2] for q in k["P_raw"]]) for k in r40["keys"]]
out["exp40_P"] = tally(rows)
# experiment 41, Told the Half: 1-7 morality, P (described) and T (told the half)
r41 = json.load(open(W / "2026-10-28-told-the-half/results.json"))
for arm in ("P", "T"):
    rows = [(k["phrase"], k["A_q"][2], k["people_q"][2], k[f"{arm}_p50s"]) for k in r41["rows"]]
    out[f"exp41_{arm}"] = tally(rows)
# experiment 42, Occupied without Counting: 1-7 naturalness, S on steps; read from its rooms as its posthoc.py does
d42 = W / "2026-10-29-occupied-without-counting"
plan = json.load(open(d42 / "plan.json")); r42 = json.load(open(d42 / "results.json"))
p50 = {}
for i in range(1, 7):
    m = f"S{i}"; order = plan["orders"][m]
    for line in (d42 / "rooms" / f"{m}.txt").read_text().splitlines():
        mm = re.match(r"\s*(\d+)\s*:.*p50=(-?[\d.]+)", line)
        if mm and 1 <= int(mm.group(1)) <= 32:
            p50.setdefault(order[int(mm.group(1)) - 1], []).append(float(mm.group(2)))
rows = [(k, r42["A"][k], r42["people_median"][k], p50[k]) for k in sorted(p50)]
out["exp42_S"] = tally(rows)

json.dump(out, open(HERE / "results.json", "w"), indent=1)
for name, t in out.items():
    print(f"{name:8s} keys {t['keys']:3d}  far {t['far_keys']:3d}  far placements {t['far_placements']:4d}  "
          f"beyond 1 step {t['beyond_one_step']:3d} ({t['share_beyond']})  on the people's {t['reached_people']}")
    for fr in t["far_rows"]:
        if fr["max_from_A"] > 1.05:
            print(f"      {fr['key']:30s} A {fr['A']:4}  people {fr['people']:4}  p50s {fr['p50s']}")

# Direction. S161.TETHER's claim says the step goes "toward the scale's middle"; its falsifier tests only distance.
# On the keys where the people's median and the scale's middle lie on opposite sides of the family's median, count the
# describer placements that moved off the family's median, by side. A family median on a half step has no side of its
# own here and is skipped (experiment 42's only two such keys, k02 and k08, are of this kind).
def direction(rows, mid):
    t = {"keys_split": 0, "moved": 0, "toward_people": 0, "toward_middle": 0}
    for k, a, p, vs in rows:
        if a != int(a) or a == mid or p == a or (p - a) * (mid - a) > 0: continue   # half-step family medians skipped
        t["keys_split"] += 1
        for v in vs:
            if abs(v - a) < 0.05: continue
            t["moved"] += 1
            t["toward_people" if (v - a) * (p - a) > 0 else "toward_middle"] += 1
    return t
dirs = {}
dirs["exp40_P"] = direction([(k["food"], k["median"]["A"], k["median"]["people"], [q[2] for q in k["P_raw"]])
                              for k in r40["keys"]], 5)
for arm in ("P", "T"):
    dirs[f"exp41_{arm}"] = direction([(k["phrase"], k["A_q"][2], k["people_q"][2], k[f"{arm}_p50s"]) for k in r41["rows"]], 4)
dirs["exp42_S"] = direction(rows, 4)
out["direction"] = dirs
json.dump(out, open(HERE / "results.json", "w"), indent=1)
print("direction, keys where the people and the middle lie on opposite sides of the family:")
for n, t in dirs.items(): print(f"  {n:8s} {t}")

# The sign, on every key where the people's median differs from the family's integer median by at least one step:
# of the describer placements, how many stayed on the family's value, how many moved to the people's side, how many
# moved the wrong way. If the side is the people's and only the length is the family's, the sign is readable.
def sign(rows):
    t = {"keys": 0, "placements": 0, "stayed": 0, "people_side": 0, "wrong_side": 0}
    for k, a, p, vs in rows:
        if a != int(a) or abs(p - a) < 1: continue
        t["keys"] += 1
        for v in vs:
            t["placements"] += 1
            if abs(v - a) < 0.05: t["stayed"] += 1
            elif (v - a) * (p - a) > 0: t["people_side"] += 1
            else: t["wrong_side"] += 1
    return t
signs = {"exp40_P": sign([(k["food"], k["median"]["A"], k["median"]["people"], [q[2] for q in k["P_raw"]]) for k in r40["keys"]])}
for arm in ("P", "T"):
    signs[f"exp41_{arm}"] = sign([(k["phrase"], k["A_q"][2], k["people_q"][2], k[f"{arm}_p50s"]) for k in r41["rows"]])
signs["exp42_S"] = sign(rows)
out["sign"] = signs
json.dump(out, open(HERE / "results.json", "w"), indent=1)
print("sign, keys where the people stand at least one step from the family's integer median:")
for n, t in signs.items(): print(f"  {n:8s} {t}")
