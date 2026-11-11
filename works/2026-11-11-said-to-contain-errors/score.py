"""Scores experiment 52 against PREDICTIONS.md. Reads rooms/, plan.json; writes results.json."""
import json, math, re, statistics as st, glob, os
plan = json.load(open("plan.json"))
scored = plan["scored"]; truth = [math.log10(plan["true_cfs"][s]) for s in scored]
def rank(x):
    o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0]*len(x); i = 0
    while i < len(o):
        j = i
        while j+1 < len(o) and x[o[j+1]] == x[o[i]]: j += 1
        for k in range(i, j+1): r[o[k]] = (i+j)/2 + 1
        i = j+1
    return r
def rho(a, b):
    ra, rb = rank(a), rank(b); ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x-ma)*(y-mb) for x, y in zip(ra, rb))
    return num / math.sqrt(sum((x-ma)**2 for x in ra) * sum((y-mb)**2 for y in rb))
rooms = {}
for f in sorted(glob.glob("rooms/*.txt")):
    t = open(f).read(); m = os.path.basename(f)[:-4]
    v = {int(a): max(int(b), 1) for a, b in re.findall(r"^(\d+):\s*cfs\s*([\d,]+)", t.replace(",", ""), re.M)}
    assert len(v) == 32, (m, len(v))
    rooms[m] = {"log": [math.log10(v[i+1]) for i in range(32)],
                "how": re.search(r"^HOW:\s*(.*)$", t, re.M).group(1).strip(),
                "known": re.search(r"^KNOWN:\s*(\S+)", t, re.M).group(1).strip(" -").lower()}
res = {"arms": {}, "makers": {}}
acc = {}
for arm in "URDT":
    ms = [m for m in rooms if m[0] == arm]
    med = [st.median(rooms[m]["log"][i] for m in ms) for i in range(32)]
    acc[arm] = med
    res["arms"][arm] = {"n": len(ms), "rho_truth": round(rho(med, truth), 3),
        "level_error": round(st.median(abs(a-b) for a, b in zip(med, truth)), 3),
        "sd_log": round(st.pstdev(med), 3), "median_log": [round(x, 3) for x in med]}
for m, r in rooms.items():
    res["makers"][m] = {"rho_truth": round(rho(r["log"], truth), 3),
        "level_error": round(st.median(abs(a-b) for a, b in zip(r["log"], truth)), 3),
        "mean_abs_from_U": round(st.mean(abs(a-b) for a, b in zip(r["log"], acc["U"])), 3),
        "follows": rho(r["log"], truth) < 0, "how": r["how"], "known": r["known"]}
for arm in "RDT":
    res["arms"][arm]["rho_with_U"] = round(rho(acc[arm], acc["U"]), 3)
res["truth_sd_log"] = round(st.pstdev(truth), 3)
json.dump(res, open("results.json", "w"), indent=1)
for a, v in res["arms"].items(): print(a, {k: v[k] for k in v if k != "median_log"})
for m in sorted(res["makers"]): x = res["makers"][m]; print(m, x["rho_truth"], x["level_error"], x["mean_abs_from_U"], x["known"])
