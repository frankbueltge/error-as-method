"""Experiment 39, Asked Three Ways: the measure and the scoring, written before any maker ran.

Reads rooms/*.txt (verbatim replies), sources/*.csv (the people) and plan.json. Writes results.json.
The scale: points (0-100) for probability phrases; log10 of the number for number phrases, values clipped at 0.01.
A distribution is held as five quantiles Q(.10), Q(.25), Q(.50), Q(.75), Q(.90).
  - people and arm A: empirical quantiles (linear interpolation, numpy's default);
  - arms P and O: each maker's five stated values, averaged quantile by quantile across the arm's makers
    (on the scale above), after sorting each maker's five values.
d(X, Y) = mean over the five quantiles of |Q_X - Q_Y|.  IQR = Q(.75) - Q(.25).
"""
import csv, json, math, re
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
QS = [0.10, 0.25, 0.50, 0.75, 0.90]
plan = json.loads((HERE / "plan.json").read_text())
keys = plan["keys"]
NEG = ["We Doubt", "Improbable", "Unlikely", "Probably Not", "Little Chance", "Almost No Chance",
       "Highly Unlikely", "Chances Are Slight"]

def scale(kind, v):
    return math.log10(max(v, 0.01)) if kind == "number" else float(v)

def unscale(kind, v):
    return 10 ** v if kind == "number" else v

def people():
    out = {}
    for f in ["probly.csv", "numberly.csv"]:
        rows = list(csv.reader(open(HERE / "sources" / f)))
        for j, h in enumerate(rows[0]):
            out[h.strip()] = [float(r[j]) for r in rows[1:]]
    return out

NUM = r"-?\d+(?:\.\d+)?"

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
        body = m.group(2).replace(",", "")
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

def main():
    P = people()
    rooms = sorted(p.stem for p in (HERE / "rooms").glob("*.txt"))
    parsed = {m: parse_room(m) for m in rooms}
    res = {"keys": [], "rooms": {m: {"parsed": len(g), "unparsed_items": b, **t} for m, (g, b, t) in parsed.items()}}
    for k, key in enumerate(keys):
        kind, ph = key["kind"], key["phrase"]
        ppl = np.array([scale(kind, v) for v in P[ph]])
        A = np.array([scale(kind, parsed[m][0][k]) for m in rooms if m[0] == "A" and k in parsed[m][0]])
        row = {"phrase": ph, "kind": kind,
               "people_raw": P[ph], "A_raw": [parsed[m][0].get(k) for m in rooms if m[0] == "A"]}
        Q = {"people": np.quantile(ppl, QS), "A": np.quantile(A, QS)}
        for arm in "PO":
            st = [sorted(scale(kind, v) for v in parsed[m][0][k]) for m in rooms if m[0] == arm and k in parsed[m][0]]
            row[f"{arm}_raw"] = [parsed[m][0].get(k) for m in rooms if m[0] == arm]
            Q[arm] = np.mean(np.array(st), axis=0)
        d = lambda x, y: float(np.mean(np.abs(Q[x] - Q[y])))
        row["Q"] = {a: [round(unscale(kind, v), 4) for v in q] for a, q in Q.items()}
        row["IQR"] = {a: float(q[3] - q[1]) for a, q in Q.items()}
        row["d"] = {"P_people": d("P", "people"), "A_people": d("A", "people"),
                    "O_people": d("O", "people"), "O_A": d("O", "A"), "P_A": d("P", "A")}
        row["median"] = {a: float(q[2]) for a, q in Q.items()}
        res["keys"].append(row)
    K = res["keys"]
    neg = [r for r in K if r["phrase"] in NEG]
    res["predictions"] = {
        "P1 d(P,people) < d(A,people), need >=18/27": sum(r["d"]["P_people"] < r["d"]["A_people"] for r in K),
        "P2 IQR(A) < IQR(people), need >=20/27": sum(r["IQR"]["A"] < r["IQR"]["people"] for r in K),
        "P3 IQR(O) > IQR(A), need >=18/27": sum(r["IQR"]["O"] > r["IQR"]["A"] for r in K),
        "P4 d(O,people) < d(O,A), need >=14/27": sum(r["d"]["O_people"] < r["d"]["O_A"] for r in K),
        "P5 median(A) > median(people) on negative phrases, need >=5/8": sum(r["median"]["A"] > r["median"]["people"] for r in neg),
    }
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    for k, v in res["predictions"].items():
        print(v, "|", k)

if __name__ == "__main__":
    main()
