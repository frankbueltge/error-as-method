"""Experiment 40, Without a Tongue: the measure and the scoring, written before any maker ran.

Reads rooms/*.txt (verbatim replies), sources/people.csv (the 59 people) and plan.json. Writes results.json.
Scale: the 9-point liking scale as given, no transform. Missing ratings are dropped, never imputed.
A distribution is held as five quantiles Q(.10), Q(.25), Q(.50), Q(.75), Q(.90):
  - people and arm A: empirical quantiles (linear interpolation, numpy's default);
  - arms P and O: each maker's five stated values, sorted, then averaged quantile by quantile across the arm.
d(X, Y) = mean over the five quantiles of |Q_X - Q_Y|.  IQR = Q(.75) - Q(.25).
S158.CENTRE (as fixed in PREDICTIONS.md): keys where |median(A) - median(people)| >= 0.5 'diverge';
on each, is median(P) nearer median(people), nearer median(A), or tied?  Also reported at >= 1.0.
"""
import csv, json, re
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
QS = [0.10, 0.25, 0.50, 0.75, 0.90]
plan = json.loads((HERE / "plan.json").read_text())
keys = plan["keys"]
NUM = r"-?\d+(?:\.\d+)?"

def people():
    rows = list(csv.reader(open(HERE / "sources" / "people.csv")))
    head = rows[0]
    out = {}
    for j, food in enumerate(head[3:], start=3):
        out[food] = {"all": [], "CT": [], "NW": []}
        for r in rows[1:]:
            if r[j].strip() in ("", "None"):
                continue
            v = float(r[j])
            out[food]["all"].append(v)
            out[food][r[1]].append(v)
    return out

def parse_room(mid):
    text = (HERE / "rooms" / f"{mid}.txt").read_text()
    order = plan["orders"][mid]
    got, bad = {}, []
    for line in text.splitlines():
        m = re.match(r"\s*(\d+)\s*:\s*(.*)$", line)
        if not m:
            continue
        j = int(m.group(1)) - 1
        if not 0 <= j < len(order):
            continue
        k = order[j]
        body = m.group(2)
        if "=" in body:  # the reply echoes the food's name before '='; a name that does not match is recorded
            name, body = body.split("=", 1)
            if name.strip().lower() != keys[k]["food"].lower():
                bad.append(f"{j + 1}: name '{name.strip()}' is not '{keys[k]['food']}'")
        if mid[0] == "A":
            nums = re.findall(NUM, body)
            if len(nums) == 1:
                got[k] = float(nums[0])
            else:
                bad.append(j + 1)
        else:
            vals = [re.search(rf"p{q}\s*=\s*({NUM})", body) for q in ("10", "25", "50", "75", "90")]
            if all(vals):
                got[k] = [float(v.group(1)) for v in vals]
            else:
                bad.append(j + 1)
    tail = {t: (re.search(rf"^{t}:\s*(.*)$", text, re.M) or [None, None])[1] for t in ("HOW", "TOOLS", "KNOWN")}
    return got, bad, tail

def side(x, a, p):
    da, dp = abs(x - a), abs(x - p)
    return "people" if dp < da else ("A" if da < dp else "tie")

def main():
    PP = people()
    rooms = sorted((p.stem for p in (HERE / "rooms").glob("*.txt")), key=lambda s: (s[0], int(s[1:])))
    parsed = {m: parse_room(m) for m in rooms}
    res = {"keys": [], "rooms": {m: {"parsed": len(g), "unparsed_items": b, **t} for m, (g, b, t) in parsed.items()}}
    for k, key in enumerate(keys):
        food = key["food"]
        ppl = np.array(PP[food]["all"])
        A = np.array([parsed[m][0][k] for m in rooms if m[0] == "A" and k in parsed[m][0]])
        row = {"food": food, "people_raw": PP[food]["all"], "A_raw": [parsed[m][0].get(k) for m in rooms if m[0] == "A"],
               "people_median_CT": float(np.median(PP[food]["CT"])), "people_median_NW": float(np.median(PP[food]["NW"]))}
        Q = {"people": np.quantile(ppl, QS), "A": np.quantile(A, QS)}
        for arm in "PO":
            st = [sorted(parsed[m][0][k]) for m in rooms if m[0] == arm and k in parsed[m][0]]
            row[f"{arm}_raw"] = [parsed[m][0].get(k) for m in rooms if m[0] == arm]
            Q[arm] = np.mean(np.array(st), axis=0)
        d = lambda x, y: float(np.mean(np.abs(Q[x] - Q[y])))
        row["Q"] = {a: [round(float(v), 4) for v in q] for a, q in Q.items()}
        row["IQR"] = {a: float(q[3] - q[1]) for a, q in Q.items()}
        row["d"] = {"P_people": d("P", "people"), "A_people": d("A", "people"),
                    "O_people": d("O", "people"), "O_A": d("O", "A"), "P_A": d("P", "A")}
        row["median"] = {a: float(q[2]) for a, q in Q.items()}
        res["keys"].append(row)
    K = res["keys"]
    centre = {}
    for tol in (0.5, 1.0):
        div = [r for r in K if abs(r["median"]["A"] - r["median"]["people"]) >= tol]
        rows = [{"food": r["food"], "people": r["median"]["people"], "A": r["median"]["A"], "P": round(r["median"]["P"], 3),
                 "O": round(r["median"]["O"], 3),
                 "P_nearer": side(r["median"]["P"], r["median"]["A"], r["median"]["people"]),
                 "O_nearer": side(r["median"]["O"], r["median"]["A"], r["median"]["people"])} for r in div]
        centre[str(tol)] = {"n_diverging": len(rows),
                            "P_nearer_people": sum(x["P_nearer"] == "people" for x in rows),
                            "P_nearer_A": sum(x["P_nearer"] == "A" for x in rows),
                            "P_tie": sum(x["P_nearer"] == "tie" for x in rows),
                            "O_nearer_A": sum(x["O_nearer"] == "A" for x in rows),
                            "rows": rows}
    res["centre"] = centre
    c = centre["0.5"]
    verdict = ("void (fewer than six keys diverge)" if c["n_diverging"] < 6 else
               ("falsified" if c["P_nearer_people"] * 2 >= c["n_diverging"] else "holds"))
    n = len(K)
    res["predictions"] = {
        f"P1 d(P,people) < d(A,people), need >=45/{n}": sum(r["d"]["P_people"] < r["d"]["A_people"] for r in K),
        f"P2 IQR(A) < IQR(people), need >=50/{n}": sum(r["IQR"]["A"] < r["IQR"]["people"] for r in K),
        f"P3 IQR(O) > IQR(A), need >=45/{n}": sum(r["IQR"]["O"] > r["IQR"]["A"] for r in K),
        f"P4 d(O,A) < d(O,people), need >=34/{n}": sum(r["d"]["O_A"] < r["d"]["O_people"] for r in K),
        "C  S158.CENTRE at tol 0.5": f"{verdict}: P nearer people on {c['P_nearer_people']}, nearer A on {c['P_nearer_A']}, tied {c['P_tie']}, of {c['n_diverging']}",
    }
    res["unanimous_A"] = [r["food"] for r in K if len(set(v for v in r["A_raw"] if v is not None)) == 1]
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    for k, v in res["predictions"].items():
        print(v, "|", k)
    print("A unanimous on", len(res["unanimous_A"]), "of", n)

if __name__ == "__main__":
    main()
