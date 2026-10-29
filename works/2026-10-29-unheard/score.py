"""Session 163, experiment 43 (Unheard): score the eighteen hand-backs against PREDICTIONS.md.
Committed with the predictions, before any maker ran. Reads rooms/<id>.txt, plan.json, people.json.
Run: python3 score.py   (writes results.json, prints the verdicts)
"""
import json, re, statistics as st
from pathlib import Path

HERE = Path(__file__).parent
plan = json.load(open(HERE / "plan.json"))
people = {k["id"]: k for k in json.load(open(HERE / "people.json"))}
ANCH = set(plan["anchors"])
MID = 5.0

def parse(mid):
    t = (HERE / "rooms" / f"{mid}.txt").read_text()
    order = plan["makers"][mid]
    out, meta = {}, {}
    for line in t.splitlines():
        m = re.match(r"\s*(\d+):\s*(.*)$", line)
        if m and int(m.group(1)) <= len(order):
            body = m.group(2)
            if mid[0] == "A":
                n = re.match(r"(-?\d+(?:\.\d+)?)", body.strip())
                if n: out[order[int(m.group(1)) - 1]] = float(n.group(1))
            else:
                d = dict(re.findall(r"(p10|p25|p50|p75|p90|mean)\s*=\s*(-?\d+(?:\.\d+)?)", body))
                if "p50" in d: out[order[int(m.group(1)) - 1]] = {a: float(b) for a, b in d.items()}
        for tag in ("KNOWN", "HOW", "TOOLS"):
            if line.startswith(tag + ":"): meta[tag] = line[len(tag) + 1:].strip()
    return out, meta

def iqr(v):
    q = st.quantiles(v, n=4, method="inclusive"); return q[2] - q[0]

def ranks(v):
    s = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and v[s[j + 1]] == v[s[i]]: j += 1
        for x in range(i, j + 1): r[s[x]] = (i + j) / 2 + 1
        i = j + 1
    return r

def spearman(a, b):
    ra, rb = ranks(a), ranks(b); ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    return num / (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5

rooms = {mid: parse(mid) for mid in plan["makers"]}
A = {mid: rooms[mid][0] for mid in rooms if mid[0] == "A"}
keys = sorted(people)
fam = {k: st.median([A[m][k] for m in A if k in A[m]]) for k in keys}
P = {k: people[k]["median"] for k in keys}

def arm_p50(arm):
    return {mid: {k: v["p50"] for k, v in rooms[mid][0].items()} for mid in rooms if mid[0] == arm}

scored = [k for k in keys if k not in ANCH]
far = [k for k in scored if abs(P[k] - fam[k]) >= 1.5]
split = [k for k in scored if fam[k] == int(fam[k]) and (P[k] - fam[k]) * (MID - fam[k]) < 0]

def tether(arm):
    pl = [(m, k, p[k]) for m, p in arm_p50(arm).items() for k in far if k in p]
    beyond = [x for x in pl if abs(x[2] - fam[x[1]]) > 1.05]
    share = len(beyond) / len(pl) if pl else None
    verdict = "void" if len(far) < 8 else ("falsified" if share > 0.25 else "held")
    return {"far_keys": len(far), "placements": len(pl), "beyond": len(beyond), "share": share, "verdict": verdict}

def side(arm):
    dep = [(m, k, p[k]) for m, p in arm_p50(arm).items() for k in split if k in p and abs(p[k] - fam[k]) >= 0.05]
    tow = [x for x in dep if (x[2] - fam[x[1]]) * (P[x[1]] - fam[x[1]]) > 0]
    share = len(tow) / len(dep) if dep else None
    verdict = "void" if len(split) < 5 or len(dep) < 10 else ("falsified" if share < 0.80 else "held")
    return {"split_keys": len(split), "departures": len(dep), "toward_people": len(tow), "share": share, "verdict": verdict}

def mae(arm, ks):
    v = [abs(p[k] - P[k]) for p in arm_p50(arm).values() for k in ks if k in p]
    return st.mean(v) if v else None

res = {"family_median": fam, "far": far, "split": split, "anchors": sorted(ANCH)}
res["TETHER_D"], res["TETHER_C"] = tether("D"), tether("C")
res["SIDE_D"], res["SIDE_C"] = side("D"), side("C")
dshare, cshare = res["TETHER_D"]["share"], res["TETHER_C"]["share"]
mD, mC = mae("D", far), mae("C", far)
res["N"] = {"beyond_share_D": dshare, "beyond_share_C": cshare, "mae_far_D": mD, "mae_far_C": mC,
            "verdict": "held" if (cshare is not None and dshare is not None and cshare - dshare >= 0.15 and mC <= 0.9 * mD) else "failed"}
nI = sum(1 for k in keys if iqr([A[m][k] for m in A if k in A[m]]) < iqr(people[k]["ratings"]))
res["I"] = {"narrower": nI, "of": len(keys), "verdict": "held" if nI >= 44 else "failed"}
L = [people[k]["LASmax"] for k in keys]
rf, rp = spearman([fam[k] for k in keys], L), spearman([P[k] for k in keys], L)
res["L"] = {"rho_family_LASmax": rf, "rho_people_LASmax": rp, "verdict": "held" if rf - rp >= 0.10 else "failed"}
known = {mid: rooms[mid][1].get("KNOWN", "") for mid in rooms if mid[0] in "DC"}
res["K"] = {"known": known, "verdict": "failed" if any(v.lower().startswith("yes") for v in known.values()) else "held"}
res["parsed"] = {mid: len(rooms[mid][0]) for mid in rooms}
res["meta"] = {mid: rooms[mid][1] for mid in rooms}
res["mae_all_scored"] = {"D": mae("D", scored), "C": mae("C", scored), "family_as_people": st.mean(abs(fam[k] - P[k]) for k in scored)}
json.dump(res, open(HERE / "results.json", "w"), indent=1)
for t in ("TETHER_D", "TETHER_C", "SIDE_D", "SIDE_C", "N", "I", "L"):
    print(t, res[t])
print("K", res["K"]["verdict"], "| parsed", res["parsed"])
print("MAE on all scored keys", res["mae_all_scored"])
