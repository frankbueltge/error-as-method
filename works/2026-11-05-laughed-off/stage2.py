"""Session 170, stage 2: arm V's briefs, built from the six A rooms by the rule fixed in PREDICTIONS.md before any maker ran.

Arm V (the fitting lie): the 24 true contact means, unchanged as a set, dealt to the 24 contact jokes in the family's own order.
The family's order on a contact joke is the median of the six A makers' own ratings; ties are broken by their mean, then by
key id. The joke the family ranks lowest gets the lowest true value, and so on up. Writes briefs/V1..V6.txt and adds
plan.json["V"] (the dealing and its Spearman rho with the true means).
Run: python3 stage2.py <download dir>   (after rooms/A1..A6.txt exist)
"""
import json, re, statistics as st, sys
from pathlib import Path
import prepare as P

HERE = Path(__file__).parent
plan = json.loads((HERE / "plan.json").read_text())


def read_a(mid):
    txt = (HERE / "rooms" / f"{mid}.txt").read_text()
    vals = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s*(\d+)\s*:\s*([0-9.]+)", txt, re.M)}
    order = P.arr_all[(int(mid[1]) - 1) % 3]
    assert sorted(vals) == list(range(1, 73)), mid
    return {order[i - 1]: v for i, v in vals.items()}


A = [read_a(f"A{i}") for i in range(1, 7)]
fam = {f: (st.median(a[f] for a in A), st.mean(a[f] for a in A), P.kid[f]) for f in P.contact}
by_family = sorted(P.contact, key=lambda f: fam[f])
values = sorted(P.meta[f]["mean"] for f in P.contact)
dealt = {f: v for f, v in zip(by_family, values)}  # joke -> value told


# contact_block expects tm: joke -> joke whose mean is told; find for each joke the contact joke carrying the dealt value
carrier = {}
for f in P.contact:
    carrier[f] = next(g for g in P.contact if P.meta[g]["mean"] == dealt[f] and g not in carrier.values())
rho = P.spearman([P.meta[f]["mean"] for f in P.contact], [dealt[f] for f in P.contact])
for i in range(1, 7):
    mid = f"V{i}"
    (HERE / "briefs" / f"{mid}.txt").write_text(P.brief(mid, "V", (i - 1) % 3, (i - 1) % 2, carrier))
    plan["makers"][mid] = {"arrangement": (i - 1) % 3 + 1, "contact_arrangement": (i - 1) % 2 + 1}
plan["V"] = {"rule": __doc__.split("\n\n")[1].strip(), "rho_with_true_means": round(rho, 4),
             "family_order_on_contact": [P.kid[f] for f in by_family],
             "told_V": {P.kid[f]: round(dealt[f], 4) for f in P.contact}}
(HERE / "plan.json").write_text(json.dumps(plan, indent=1))
print("V dealt; rho with true means", round(rho, 3))
