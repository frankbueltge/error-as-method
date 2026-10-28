"""Session 160: score the twenty rooms against the people, as PREDICTIONS.md fixes. Committed before any maker ran.
Run: python3 score.py   (reads plan.json and rooms/*.txt, writes results.json)
"""
import json, re, statistics as st
from pathlib import Path

HERE = Path(__file__).parent
plan = json.load(open(HERE / "plan.json"))
items = plan["items"]
N = len(items)
QS = (0.10, 0.25, 0.50, 0.75, 0.90)

def quant(v, q):
    v = sorted(v); h = (len(v) - 1) * q; lo = int(h)
    return v[lo] + (v[min(lo + 1, len(v) - 1)] - v[lo]) * (h - lo)

def parse(mid):
    t = (HERE / "rooms" / f"{mid}.txt").read_text()
    out, order = {}, plan["orders"][mid]
    for line in t.splitlines():
        m = re.match(r"\s*(\d+)\s*:\s*(.*?)\s*=\s*(.*)$", line)
        if not m:
            continue
        k = int(m.group(1)) - 1
        if not 0 <= k < N:
            continue
        j = order[k]
        assert m.group(2).strip().lower() == items[j]["phrase"].lower(), (mid, k, m.group(2), items[j]["phrase"])
        if mid[0] == "A":
            out[j] = int(re.match(r"\d+", m.group(3)).group())
        else:
            out[j] = [float(x) for x in re.findall(r"p\d+=\s*([\d.]+)", m.group(3))]
    assert len(out) == N, (mid, len(out))
    lines = {k: (re.search(rf"^{k}:\s*(.*)$", t, re.M) or [None, None])[1] for k in ("KNOWN", "HOW", "TOOLS")}
    return out, lines

makers = {mid: parse(mid) for mid in plan["orders"] if (HERE / "rooms" / f"{mid}.txt").exists()}
A = [m for m in makers if m[0] == "A"]
P = [m for m in makers if m[0] == "P"]
T = [m for m in makers if m[0] == "T"]

rows = []
for j, it in enumerate(items):
    ppl = it["en"]
    a = [makers[m][0][j] for m in A]
    r = {"id": it["id"], "phrase": it["phrase"], "valence": it["valence"], "foundation": it["foundation"],
         "n_people": len(ppl), "people_q": [quant(ppl, q) for q in QS], "people_mean": st.mean(ppl),
         "people_zh_median": st.median(it["zh"]), "A": a, "A_q": [quant(a, q) for q in QS]}
    for arm, ids in (("P", P), ("T", T)):
        qs = [makers[m][0][j] for m in ids]
        r[arm + "_q"] = [st.mean(q[i] for q in qs) for i in range(5)]
        r[arm + "_p50s"] = [q[2] for q in qs]
    pm, am = r["people_q"][2], r["A_q"][2]
    r["diverges"] = abs(am - pm) >= 6 / 20
    for arm in ("P", "T"):
        x = r[arm + "_q"][2]
        r["s_" + arm] = (x - am) / (pm - am) if r["diverges"] else None
        r["err_" + arm] = abs(x - pm)
    r["X"] = am + 2 * (r["P_q"][2] - am)  # the arithmetic correction of P, fixed before the data
    r["err_X"] = abs(r["X"] - pm)
    r["iqr_A"] = r["A_q"][3] - r["A_q"][1]
    r["iqr_people"] = r["people_q"][3] - r["people_q"][1]
    rows.append(r)

D = [r for r in rows if r["diverges"]]
mean = lambda v: st.mean(v) if v else None
res = {
    "n_diverging": len(D),
    "HALFWAY_mean_s_P": mean([r["s_P"] for r in D]), "median_s_P": st.median([r["s_P"] for r in D]) if D else None,
    "mean_s_T": mean([r["s_T"] for r in D]), "median_s_T": st.median([r["s_T"] for r in D]) if D else None,
    "T_nearer_than_P": sum(r["err_T"] < r["err_P"] for r in D),
    "X_nearer_than_P": sum(r["err_X"] < r["err_P"] for r in D),
    "X_nearer_than_T": sum(r["err_X"] < r["err_T"] for r in D),
    "T_nearer_than_X": sum(r["err_T"] < r["err_X"] for r in D),
    "mean_err": {k: mean([r["err_" + k] for r in D]) for k in ("P", "T", "X")},
    "mean_err_A": mean([abs(r["A_q"][2] - r["people_q"][2]) for r in D]),
    "iqr_A_below_people": sum(r["iqr_A"] < r["iqr_people"] for r in rows),
    "refusals_A": [m for m in A if len(set(makers[m][0].values())) == 1],
    "known": {m: makers[m][1]["KNOWN"] for m in P + T},
    "how": {m: makers[m][1]["HOW"] for m in makers},
    "tools": {m: makers[m][1]["TOOLS"] for m in makers},
    "makers": {"A": A, "P": P, "T": T},
}
json.dump({"summary": res, "rows": rows}, open(HERE / "results.json", "w"), indent=1, ensure_ascii=False)
for k, v in res.items():
    if k not in ("how", "known", "tools"):
        print(k, v)
