"""Session 168, experiment 47 (Without a Nose): score the hand-backs against PREDICTIONS.md. Committed before any maker ran.

Reads plan.json, people.json and rooms/*.txt; writes results.json. Every definition is the one in PREDICTIONS.md.
Adapted from experiment 46's score.py: the scale is 1-9, and the row due tonight is S166.PERCEPT.
Run: python3 score.py
"""
import json, re, statistics as st
from pathlib import Path

HERE = Path(__file__).parent
NUM = r"(-?\d+(?:\.\d+)?)"


def parse_ratings(text, ids):
    got = dict(re.findall(r"^\s*(\d+)\s*:\s*([1-9])\s*$", text, re.M))
    assert len(got) == len(ids), f"ratings: {len(got)} of {len(ids)}"
    return {k: int(got[str(i + 1)]) for i, k in enumerate(ids)}


def parse_desc(text, ids):
    got = dict(re.findall(rf"^\s*(\d+)\s*:\s*mean\s*{NUM}\s*$", text, re.M | re.I))
    assert len(got) == len(ids), f"descriptions: {len(got)} of {len(ids)}"
    return {k: float(got[str(i + 1)]) for i, k in enumerate(ids)}


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
    plan = json.load(open(HERE / "plan.json")); P = {k: v for k, v in json.load(open(HERE / "people.json")).items() if not k.startswith("_")}
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
    acc = lambda arms: {k: st.mean(R[m][k] for a in arms for m in makers(a)) for k in S}
    out = {"scored_keys": len(S), "family_median_sd": round(st.pstdev(fam.values()), 3),
           "people_mean_sd": round(st.pstdev(pm), 3)}
    r0 = spearman([fam[k] for k in S], pm)
    fsd = st.pstdev(fam.values())
    out["P0_PREMISE"] = {"rho_family_people": round(r0, 3), "family_median_sd": round(fsd, 3), "holds": fsd >= 1.0 and r0 >= 0.5}
    arms = {}
    for a in "DBS":
        ac = acc(a)
        arms[a] = {"rho_people": spearman([ac[k] for k in S], pm), "rho_family": spearman([ac[k] for k in S], [fam[k] for k in S]),
                   "mae": st.mean(abs(R[m][k] - P[k]["mean"]) for m in makers(a) for k in S),
                   "level": st.mean(ac.values()) - st.mean(pm),
                   "maker_sd": st.mean(st.pstdev([R[m][k] for k in S]) for m in makers(a))}
    out["arms"] = {a: {x: round(v, 3) for x, v in d.items()} for a, d in arms.items()}
    out["per_maker"] = {m: {"rho_people": round(spearman([R[m][k] for k in S], pm), 3),
                            "rho_family": round(spearman([R[m][k] for k in S], [fam[k] for k in S]), 3),
                            "sd": round(st.pstdev([R[m][k] for k in S]), 3)} for a in "DBS" for m in makers(a)}
    out["per_maker"].update({m: {"rho_people": round(spearman([A[m][k] for k in S], pm), 3)} for m in A})
    D, B, Sh = arms["D"], arms["B"], arms["S"]
    out["P1_OWN"] = {"holds": D["rho_family"] > D["rho_people"]}
    out["P2_CONTACT"] = {"gain": round(B["rho_people"] - D["rho_people"], 3), "holds": B["rho_people"] >= D["rho_people"] + 0.05}
    out["P3_PAIRS"] = {"gain": round(B["rho_people"] - Sh["rho_people"], 3), "holds": B["rho_people"] >= Sh["rho_people"] + 0.05}
    out["P4_LEVEL"] = {"mae": {a: round(arms[a]["mae"], 3) for a in "DBS"}, "holds": B["mae"] <= 0.8 * D["mae"]}
    out["P5_NOTICED_S"] = {"S_how": {m: field(room(m), "HOW") for m in makers("S")},
                           "note": "coded by hand in the journal against the rule in PREDICTIONS.md"}
    out["P6_NOTICED_B"] = {"B_how": {m: field(room(m), "HOW") for m in makers("B")},
                           "note": "coded by hand in the journal against the rule in PREDICTIONS.md"}
    out["P7_NERVE"] = {"maker_sd": {a: round(arms[a]["maker_sd"], 3) for a in "DBS"}, "holds": Sh["maker_sd"] < D["maker_sd"]}
    known = {m: field(room(m), "KNOWN") for a in "DBS" for m in makers(a)}
    yes = [m for m, v in known.items() if v and v.lower().startswith("yes")]
    out["P8_K"] = {"known": known, "yes": yes, "holds": not yes}

    # S166.PERCEPT by its letter (its second clause is the hand coding of P5: at least two of six S makers)
    void = r0 >= 0.5
    out["S166_PERCEPT"] = {"void": void, "rho_family_people": round(r0, 3),
                           "clause1_gain_B_over_D": round(B["rho_people"] - D["rho_people"], 3),
                           "clause1_falsifies": B["rho_people"] - D["rho_people"] < 0.10,
                           "clause2": "hand coding, see journal (falsifies at 2 of 6)"}
    out["how"] = {m: field(room(m), "HOW") for m in list(A) + list(R)}
    out["per_key"] = {k: {"name": P[k]["name"], "people_n": P[k]["people"], "scored_words": P[k]["scored_words"], "people_mean": P[k]["mean"], "people_sd": P[k]["sd"],
                          "fam": fam[k], "A": [A[m][k] for m in A], **{a: [R[m][k] for m in makers(a)] for a in "DBS"}} for k in S}
    (HERE / "results.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for k in ("P0_PREMISE", "arms", "P1_OWN", "P2_CONTACT", "P3_PAIRS", "P4_LEVEL", "P7_NERVE", "P8_K", "S166_PERCEPT",
              "family_median_sd", "people_mean_sd"):
        print(k, out[k])
