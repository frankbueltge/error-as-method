"""Session 165, experiment 45 (Paired): score the hand-backs against PREDICTIONS.md. Committed before any maker ran.

Reads plan.json, people.json and rooms/*.txt; writes results.json. Every definition is the one in PREDICTIONS.md.
Spearman and the parsers follow experiment 44's score.py.
Run: python3 score.py
"""
import json, re, statistics as st
from pathlib import Path

HERE = Path(__file__).parent
NUM = r"(-?\d+(?:\.\d+)?)"
MIDDLE = 5  # the middle of the people's 1-9 scale


def parse_ratings(text, ids):
    got = dict(re.findall(r"^\s*(\d+)\s*:\s*([1-9])\s*$", text, re.M))
    assert len(got) == len(ids), f"ratings: {len(got)} of {len(ids)}"
    return {k: int(got[str(i + 1)]) for i, k in enumerate(ids)}


def parse_desc(text, ids):
    rows = re.findall(rf"^\s*(\d+)\s*:\s*median\s*{NUM}\s*,\s*mean\s*{NUM}\s*$", text, re.M | re.I)
    got = {r[0]: (float(r[1]), float(r[2])) for r in rows}
    assert len(got) == len(ids), f"descriptions: {len(got)} of {len(ids)}"
    return {k: {"p50": got[str(i + 1)][0], "mean": got[str(i + 1)][1]} for i, k in enumerate(ids)}


def field(text, name):
    m = re.search(rf"^{name}:\s*(.+)$", text, re.M)
    return m.group(1).strip() if m else None


def ranks(x):
    o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]: j += 1
        for t in range(i, j + 1): r[o[t]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b); ma, mb = st.mean(ra), st.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else None


def load():
    plan = json.load(open(HERE / "plan.json")); P = json.load(open(HERE / "people.json"))
    S = [k["id"] for k in plan["keys"] if k["role"] == "scored"]
    room = lambda m: (HERE / "rooms" / f"{m}.txt").read_text()
    order = lambda m: plan["arrangements_scored"][plan["makers"][m]["scored_arrangement"] - 1]
    A = {f"A{j}": parse_ratings(room(f"A{j}"), order(f"A{j}")) for j in range(1, 7)}
    R = {f"{a}{j}": parse_desc(room(f"{a}{j}"), order(f"{a}{j}")) for a in "DBS" for j in range(1, 7)}
    return plan, P, S, A, R, room


if __name__ == "__main__":
    plan, P, S, A, R, room = load()
    makers = lambda a: [f"{a}{j}" for j in range(1, 7)]
    fam = {k: st.median(A[m][k] for m in A) for k in S}
    pm = [P[k]["mean"] for k in S]
    acc = lambda arms: {k: st.mean(R[m][k]["mean"] for a in arms for m in makers(a)) for k in S}
    out = {"scored_keys": len(S), "family_median_sd": round(st.pstdev(fam.values()), 3),
           "rho_family_people": round(spearman([fam[k] for k in S], pm), 3)}
    arms = {}
    for a in "DBS":
        ac = acc(a)
        arms[a] = {"rho_people": spearman([ac[k] for k in S], pm), "rho_family": spearman([ac[k] for k in S], [fam[k] for k in S]),
                   "mae": st.mean(abs(R[m][k]["mean"] - P[k]["mean"]) for m in makers(a) for k in S),
                   "level": st.mean(ac.values()) - st.mean(pm)}
    out["arms"] = {a: {x: round(v, 3) for x, v in d.items()} for a, d in arms.items()}
    D, B, Sh = arms["D"], arms["B"], arms["S"]
    out["P1_OWN"] = {"holds": D["rho_family"] > D["rho_people"]}
    out["P2_BREADTH"] = {"gain": round(B["rho_people"] - D["rho_people"], 3), "holds": B["rho_people"] >= D["rho_people"] + 0.05}
    out["P3_PAIRS"] = {"gain": round(B["rho_people"] - Sh["rho_people"], 3), "holds": B["rho_people"] >= Sh["rho_people"] + 0.05}
    out["P4_LEVEL"] = {"ratio_S_over_D": round(Sh["mae"] / D["mae"], 3), "holds": Sh["mae"] <= 0.8 * D["mae"]}
    lean = {a: arms[a]["rho_family"] - arms[a]["rho_people"] for a in "DB"}
    out["P5_LEAVES"] = {"lean_D": round(lean["D"], 3), "lean_B": round(lean["B"], 3), "holds": lean["B"] < lean["D"]}
    out["P6_UNNOTICED"] = {"S_how": {m: field(room(m), "HOW") for m in makers("S")},
                           "note": "coded by hand in results.md against the rule in PREDICTIONS.md"}
    known = {m: field(room(m), "KNOWN") for a in "DBS" for m in makers(a)}
    yes = [m for m, v in known.items() if v and v.lower().startswith("yes")]
    out["P7_K"] = {"known": known, "yes": yes, "holds": not yes}
    narrower = sum(1 for k in S if st.pstdev([A[m][k] for m in A]) < P[k]["sd"])
    out["P8_I"] = {"keys_family_narrower": narrower, "of": len(S), "holds": narrower >= 36}

    # S164.SHAPE by its letter: the account of all describers (D, B and S)
    al = acc("DBS")
    r_p, r_f = spearman([al[k] for k in S], pm), spearman([al[k] for k in S], [fam[k] for k in S])
    void = len(S) < 20 or st.pstdev(fam.values()) < 1.0
    out["S164_SHAPE"] = {"rho_people": round(r_p, 3), "rho_family": round(r_f, 3), "void": void,
                         "falsified": (not void) and r_p >= r_f}

    # S163.ANCHOR by its letter, the anchored arm being B (told the people's median and mean on 24 other keys), plain D
    far = [k for k in S if abs(P[k]["median"] - fam[k]) >= 1.5]
    def is_split(k):
        f, p = fam[k], P[k]["median"]
        return f == int(f) and ((p > f and MIDDLE < f) or (p < f and MIDDLE > f))
    split = [k for k in S if is_split(k)]
    dep = [(m, k) for m in makers("B") for k in split if abs(R[m][k]["p50"] - fam[k]) >= 0.05]
    toward = [d for d in dep if (R[d[0]][d[1]]["p50"] - fam[d[1]]) * (P[d[1]]["median"] - fam[d[1]]) > 0]
    mae_far = {a: (st.mean(abs(R[m][k]["p50"] - P[k]["median"]) for m in makers(a) for k in far) if far else None) for a in "DBS"}
    v163 = len(far) < 8 or len(split) < 5
    ratio = mae_far["B"] / mae_far["D"] if far else None
    out["S163_ANCHOR"] = {"far_keys": len(far), "split_keys": len(split), "void": v163,
                          "mae_far_p50": {a: None if v is None else round(v, 3) for a, v in mae_far.items()},
                          "ratio_B_over_D": None if ratio is None else round(ratio, 3),
                          "split_departures": len(dep), "toward_people": len(toward),
                          "falsified": (not v163) and (ratio > 0.6 or (len(dep) > 0 and len(toward) / len(dep) < 0.8))}
    out["far_placements_beyond_one_step"] = {a: [sum(1 for m in makers(a) for k in far if abs(R[m][k]["p50"] - fam[k]) > 1.05),
                                                 6 * len(far)] for a in "DBS"}
    out["how"] = {m: field(room(m), "HOW") for m in list(A) + list(R)}
    out["per_key"] = {k: {"file": P[k]["file"], "species": P[k]["species"], "people_mean": P[k]["mean"], "people_median": P[k]["median"],
                          "fam": fam[k], "A": [A[m][k] for m in A],
                          **{a: [R[m][k]["mean"] for m in makers(a)] for a in "DBS"}} for k in S}
    (HERE / "results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for k in ("arms", "P1_OWN", "P2_BREADTH", "P3_PAIRS", "P4_LEVEL", "P5_LEAVES", "P7_K", "P8_I", "S164_SHAPE", "S163_ANCHOR",
              "far_placements_beyond_one_step", "rho_family_people", "family_median_sd"):
        print(k, out[k])
