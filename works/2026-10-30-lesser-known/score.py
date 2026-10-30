"""Session 164, experiment 44 (Lesser Known): score the hand-backs against PREDICTIONS.md. Committed before any maker ran.

Reads plan.json, people.json and rooms/*.txt; writes results.json. Every definition is the one in PREDICTIONS.md.
Run: python3 score.py
"""
import json, re, statistics as st
from pathlib import Path

HERE = Path(__file__).parent

def parse_ratings(text, ids):
    got = dict(re.findall(r"^\s*(\d+)\s*:\s*([1-6])\s*$", text, re.M))
    assert len(got) == len(ids), f"ratings: {len(got)} of {len(ids)}"
    return {k: int(got[str(i + 1)]) for i, k in enumerate(ids)}

NUM = r"(-?\d+(?:\.\d+)?)"
def parse_spreads(text, ids):
    rows = re.findall(rf"^\s*(\d+)\s*:\s*p25\s*=\s*{NUM}\s+p50\s*=\s*{NUM}\s+p75\s*=\s*{NUM}\s+mean\s*=\s*{NUM}\s*$",
                      text, re.M)
    got = {r[0]: tuple(float(x) for x in r[1:]) for r in rows}
    assert len(got) == len(ids), f"spreads: {len(got)} of {len(ids)}"
    return {k: dict(zip(("p25", "p50", "p75", "mean"), got[str(i + 1)])) for i, k in enumerate(ids)}

def field(text, name):
    m = re.search(rf"^{name}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else None

def q(v, p):
    return float(st.quantiles(v, n=100, method="inclusive")[p - 1])

def ranks(x):
    o = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]:
            j += 1
        for t in range(i, j + 1):
            r[o[t]] = (i + j) / 2 + 1
        i = j + 1
    return r

def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else None

if __name__ == "__main__":
    plan = json.load(open(HERE / "plan.json"))
    P = json.load(open(HERE / "people.json"))
    keys = [k["id"] for k in plan["keys"]]
    TRUE = {k["id"]: k["true"] for k in plan["keys"]}
    anchors = set(plan["M_anchors"]) | set(plan["U_anchors"])
    S = [k for k in keys if k not in anchors]
    room = lambda m: (HERE / "rooms" / f"{m}.txt").read_text()
    A = {f"A{j}": parse_ratings(room(f"A{j}"), plan["shown"][f"A{j}"]) for j in range(1, 7)}
    R = {}
    for arm in "DMU":
        for j in range(1, 7):
            m = f"{arm}{j}"
            R[m] = parse_spreads(room(m), plan["shown"][m])
    known = {m: field(room(m), "KNOWN") for m in R}
    how = {m: field(room(m), "HOW") for m in list(A) + list(R)}

    fam = {k: st.median([A[m][k] for m in A]) for k in keys}
    aiqr = {k: q([A[m][k] for m in A], 75) - q([A[m][k] for m in A], 25) for k in keys}
    makers = lambda arm: [f"{arm}{j}" for j in range(1, 7)]

    def gap(arm):
        t = st.mean(R[m][k]["mean"] for m in makers(arm) for k in S if TRUE[k])
        f = st.mean(R[m][k]["mean"] for m in makers(arm) for k in S if not TRUE[k])
        return t - f
    def mae(arm, ks=S, stat="mean", pstat="mean"):
        return st.mean(abs(R[m][k][stat] - P[k][pstat]) for m in makers(arm) for k in ks)
    def armmean(arm, k):
        return st.mean(R[m][k]["mean"] for m in makers(arm))

    people_gap = st.mean(P[k]["mean"] for k in S if TRUE[k]) - st.mean(P[k]["mean"] for k in S if not TRUE[k])
    fam_gap = st.mean(fam[k] for k in S if TRUE[k]) - st.mean(fam[k] for k in S if not TRUE[k])
    G = {a: gap(a) for a in "DMU"}
    E = {a: mae(a) for a in "DMU"}
    out = {"scored_keys": len(S), "M_anchors": plan["M_anchors"], "U_anchors": plan["U_anchors"],
           "people_gap_true_minus_false": round(people_gap, 3), "family_gap": round(fam_gap, 3),
           "gap": {a: round(G[a], 3) for a in G}, "mae_mean": {a: round(E[a], 3) for a in E}}

    out["P1_KNOW"] = {"D_gap_minus_people_gap": round(G["D"] - people_gap, 3),
                      "holds": G["D"] - people_gap >= 1.0}
    out["P2_MIDDLE"] = {"gap_ratio_M_over_D": round(G["M"] / G["D"], 3) if G["D"] else None,
                        "mae_ratio_M_over_D": round(E["M"] / E["D"], 3),
                        "holds": (G["D"] > 0 and G["M"] <= 0.5 * G["D"]) and E["M"] <= 0.6 * E["D"]}
    nz = sum(1 for k in S if aiqr[k] > 0)
    rho3 = spearman([aiqr[k] for k in S], [abs(P[k]["median"] - fam[k]) for k in S])
    out["P3_UNSURE"] = {"keys_with_family_iqr_above_0": nz, "rho": None if rho3 is None else round(rho3, 3),
                        "void": nz < 6, "holds": (nz >= 6) and rho3 is not None and rho3 <= -0.2}
    out["P4_SPENT"] = {"mae_U": round(E["U"], 3), "mae_M": round(E["M"], 3), "holds": E["U"] >= E["M"]}
    rho5 = {a: spearman([armmean(a, k) for k in S], [P[k]["mean"] for k in S]) for a in "DMU"}
    out["P5_ORDER"] = {"rho": {a: None if v is None else round(v, 3) for a, v in rho5.items()},
                       "holds": all(v is None or v < 0.3 for v in rho5.values())}
    narrower = sum(1 for k in S if aiqr[k] < P[k]["p75"] - P[k]["p25"])
    out["P6_I"] = {"narrower": narrower, "of": len(S), "holds": narrower >= 42}
    yes = [m for m, v in known.items() if v and v.lower().startswith("yes")]
    out["P7_K"] = {"known": known, "yes": yes, "holds": not yes}

    # S163.ANCHOR by its letter, the anchored arm being M (declared in PREDICTIONS.md)
    far = [k for k in S if abs(P[k]["median"] - fam[k]) >= 1.5]
    def is_split(k):
        f, p = fam[k], P[k]["median"]
        return f == int(f) and ((p > f and 3.5 < f) or (p < f and 3.5 > f))
    split = [k for k in S if is_split(k)]
    dep = [(m, k) for m in makers("M") for k in split if abs(R[m][k]["p50"] - fam[k]) >= 0.05]
    toward = [d for d in dep if (R[d[0]][d[1]]["p50"] - fam[d[1]]) * (P[d[1]]["median"] - fam[d[1]]) > 0]
    mae_far = {a: (st.mean(abs(R[m][k]["p50"] - P[k]["median"]) for m in makers(a) for k in far) if far else None)
               for a in "DMU"}
    out["S163_ANCHOR"] = {"far_keys": len(far), "split_keys": len(split), "void": len(far) < 8 or len(split) < 5,
                          "mae_far_p50": {a: None if v is None else round(v, 3) for a, v in mae_far.items()},
                          "ratio_M_over_D": round(mae_far["M"] / mae_far["D"], 3) if far else None,
                          "split_departures": len(dep), "toward_people": len(toward)}
    beyond = {a: sum(1 for m in makers(a) for k in far if abs(R[m][k]["p50"] - fam[k]) > 1.05) for a in "DMU"}
    out["far_placements_beyond_one_step"] = {a: [beyond[a], 6 * len(far)] for a in "DMU"}
    out["how"] = how
    out["per_key"] = {k: {"true": TRUE[k], "people_median": P[k]["median"], "people_mean": P[k]["mean"],
                          "fam": fam[k], "fam_iqr": aiqr[k], "A": [A[m][k] for m in A],
                          **{a: [R[m][k] if k in R[m] else None for m in makers(a)] for a in "DMU"}}
                      for k in keys}
    json.dump(out, open(HERE / "results.json", "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in out.items() if k not in ("how", "per_key", "P7_K")}, indent=1))
    print("K yes:", yes)
