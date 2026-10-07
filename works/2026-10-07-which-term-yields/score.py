"""Score the census of bearers against PREDICTIONS.md, and the two fresh readers against the practice.

Run from the repository root:  python3 works/2026-10-07-which-term-yields/score.py
Writes results.json beside this file. Standard library only.
"""
import collections, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
census = json.load(open(os.path.join(HERE, "census.json")))["rows"]
P = {r["id"]: r["wrong"] for r in census}
readers = {}
for name in ("A", "B"):
    path = os.path.join(HERE, "readers", f"reader-{name}.json")
    if os.path.exists(path):
        readers[name] = {r["id"]: r["wrong"] for r in json.load(open(path))}

def kappa(a, b, ids):
    n = len(ids)
    po = sum(a[i] == b[i] for i in ids) / n
    ca, cb = collections.Counter(a[i] for i in ids), collections.Counter(b[i] for i in ids)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / n / n
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None, round(po, 3)

ids = [r["id"] for r in census]
count = collections.Counter(P.values())
by_changed = collections.defaultdict(collections.Counter)
for r in census:
    by_changed[r["changed"]][r["wrong"]] += 1

# P2: the same reference with opposite bearers. Pairs are named by hand in PAIRS and checked here.
PAIRS = [("F-182", "F-181", "the ear of experiment 5, held byte-identical (perceive.py)")]
p2 = [{"pair": p[:2], "reference": p[2], "wrong": [P[p[0]], P[p[1]]]} for p in PAIRS]

out = {
    "n": len(ids),
    "practice": dict(count),
    "by_changed": {k: dict(v) for k, v in by_changed.items()},
    "P1": {"rule": "R >= 10 of 29", "R": count["R"], "holds": count["R"] >= 10},
    "P2": {"rule": "one pair, same reference, opposite bearers", "pairs": p2,
           "holds": any(sorted(x["wrong"]) == ["J", "R"] for x in p2)},
    "P3": {"rule": "X <= 3", "X": count["X"], "holds": count["X"] <= 3},
    "readers": {},
}
for name, rd in readers.items():
    k, po = kappa(P, rd, ids)
    c = collections.Counter(rd.values())
    out["readers"][name] = {
        "counts": dict(c), "agreement_with_practice": po, "kappa_with_practice": k,
        "P1_under_this_reader": c["R"] >= 10,
        "disagreements": {i: {"practice": P[i], "reader": rd[i]} for i in ids if P[i] != rd[i]},
    }
if len(readers) == 2:
    k, po = kappa(readers["A"], readers["B"], ids)
    out["readers_with_each_other"] = {"agreement": po, "kappa": k}
    out["R_by_all_three"] = [i for i in ids if P[i] == readers["A"][i] == readers["B"][i] == "R"]
    out["J_by_all_three"] = [i for i in ids if P[i] == readers["A"][i] == readers["B"][i] == "J"]
# Post hoc, added after the readers answered (not in PREDICTIONS.md): the reference implicated, R or B.
coders = {"practice": P, **readers}
out["posthoc_reference_implicated"] = {k: sum(v[i] in ("R", "B") for i in ids) for k, v in coders.items()}
if len(readers) == 2:
    out["posthoc_reference_implicated_by_all_three"] = [i for i in ids if all(v[i] in ("R", "B") for v in coders.values())]
    out["posthoc_seam"] = [i for i in ids if P[i] == "R" and readers["A"][i] == "J" and readers["B"][i] == "J"]
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
