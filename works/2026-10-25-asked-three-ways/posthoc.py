"""POST-HOC, written after results.json was read (Session 158). Not a prediction.

Question: on the phrases where the family's own centre (median of arm A) differs from the people's median,
whose centre do the describers give? For each such phrase: is the median stated by arm P (describing the people)
and by arm O (describing itself) nearer to median(A) or to median(people)?
'Differs' = at least 2 points (probability) or at least 0.05 in log10 (number), fixed here before counting.
Also: how many of the 27 phrases did all twelve arm-A makers answer with the same number?
"""
import json
from pathlib import Path
HERE = Path(__file__).parent
r = json.loads((HERE / "results.json").read_text())
out = {"diverging": [], "unanimous_A": []}
for k in r["keys"]:
    m = k["median"]
    tol = 2 if k["kind"] == "probability" else 0.05
    vals = [v for v in k["A_raw"] if v is not None]
    if len(set(vals)) == 1:
        out["unanimous_A"].append(k["phrase"])
    if abs(m["A"] - m["people"]) >= tol:
        side = lambda x: "A" if abs(x - m["A"]) < abs(x - m["people"]) else ("people" if abs(x - m["A"]) > abs(x - m["people"]) else "tie")
        out["diverging"].append({"phrase": k["phrase"], "people": m["people"], "A": m["A"], "P": m["P"], "O": m["O"],
                                 "P_nearer": side(m["P"]), "O_nearer": side(m["O"])})
for arm in "PO":
    out[f"{arm}_nearer_A"] = sum(d[f"{arm}_nearer"] == "A" for d in out["diverging"])
out["n_diverging"] = len(out["diverging"])
out["n_unanimous_A"] = len(out["unanimous_A"])
(HERE / "posthoc.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({k: v for k, v in out.items() if k != "diverging"}, indent=1))
for d in out["diverging"]:
    print(d)
