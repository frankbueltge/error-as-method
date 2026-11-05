"""Session 170 (experiment 48, Laughed Off): scores the rooms against PREDICTIONS.md and writes results.json.

Needs no download: reads people.json, plan.json, rooms/*.txt, and coding/mine.json (my noticing codes, written before the
blind coder ran) and coding/key.json + coding/answer.txt (the blind coder's). Prints each prediction's text beside its verdict.
Run: python3 score.py
"""
import json, re, statistics as st
from pathlib import Path

HERE = Path(__file__).parent
people = json.loads((HERE / "people.json").read_text())
plan = json.loads((HERE / "plan.json").read_text())
kid_of_pos = {k["survey_position"]: k["id"] for k in plan["keys"]}
scored = [k["id"] for k in plan["keys"] if k["role"] == "scored"]
contact = [k["id"] for k in plan["keys"] if k["role"] == "contact"]
truth = {k: people[k]["mean"] for k in scored}


def rank(x):
    o = sorted(range(len(x)), key=lambda i: x[i]); r = [0.0] * len(x); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]: j += 1
        for t in range(i, j + 1): r[o[t]] = (i + j) / 2
        i = j + 1
    return r


def rho(a, b, keys=scored):
    x, y = rank([a[k] for k in keys]), rank([b[k] for k in keys]); mx, my = st.mean(x), st.mean(y)
    return sum((p - mx) * (q - my) for p, q in zip(x, y)) / (sum((p - mx) ** 2 for p in x) * sum((q - my) ** 2 for q in y)) ** 0.5


def room(mid):
    txt = (HERE / "rooms" / f"{mid}.txt").read_text()
    vals = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s*(\d+)\s*:\s*(?:mean\s*)?([0-9.]+)", txt, re.M)}
    arm = mid[0]; a = plan["makers"][mid]["arrangement"] - 1
    order = plan["arrangements_all"][a] if arm == "A" else plan["arrangements_scored"][a]
    assert sorted(vals) == list(range(1, len(order) + 1)), (mid, len(vals))
    how = re.search(r"^HOW:\s*(.*)$", txt, re.M); known = re.search(r"^KNOWN:\s*(.*)$", txt, re.M)
    return dict(values={order[i - 1]: v for i, v in vals.items()}, how=how.group(1).strip() if how else "",
                known=known.group(1).strip() if known else None, text=txt)


R = {f"{arm}{i}": room(f"{arm}{i}") for arm in "ADBSV" for i in range(1, 7) if (HERE / "rooms" / f"{arm}{i}.txt").exists()}
arms = sorted({m[0] for m in R})
acc = {arm: {k: st.median(R[f"{arm}{i}"]["values"][k] for i in range(1, 7)) for k in scored} for arm in arms}
res = {"arms": {}, "makers": {}}
for arm in arms:
    res["arms"][arm] = dict(rho_people=round(rho(acc[arm], truth), 4),
                            rho_family=round(rho(acc[arm], acc["A"]), 4) if arm != "A" else None,
                            sd_medians=round(st.pstdev(acc[arm].values()), 4),
                            mean_medians=round(st.mean(acc[arm].values()), 4),
                            mae=round(st.mean(abs(acc[arm][k] - truth[k]) for k in scored), 4))
for m, r in R.items():
    res["makers"][m] = dict(rho_people=round(rho(r["values"], truth), 4), sd=round(st.pstdev(r["values"][k] for k in scored), 4),
                            mean=round(st.mean(r["values"][k] for k in scored), 4), how=r["how"], known=r["known"])
res["people"] = dict(sd=round(st.pstdev(truth.values()), 4), mean=round(st.mean(truth.values()), 4))

mine = json.loads((HERE / "coding" / "mine.json").read_text()) if (HERE / "coding" / "mine.json").exists() else {}
blind = {}
if (HERE / "coding" / "answer.txt").exists():
    key = json.loads((HERE / "coding" / "key.json").read_text())
    for m in re.finditer(r"(C\d\d)\s*:\s*(YES|NO)", (HERE / "coding" / "answer.txt").read_text()):
        blind[key[m.group(1)]] = m.group(2) == "YES"
noticed = {arm: sum(1 for i in range(1, 7) if mine.get(f"{arm}{i}")) for arm in "BSV"}
noticed_blind = {arm: sum(1 for i in range(1, 7) if blind.get(f"{arm}{i}")) for arm in "BSV"}
res["noticed_mine"], res["noticed_blind"] = noticed, noticed_blind
res["coder_agreement"] = sum(1 for m in blind if blind[m] == bool(mine.get(m))) if blind else None

a = res["arms"]
P = [
    ("P0 PREMISE", "SD of A medians on the 48 scored >= 0.5 and their rho with the people < 0.5",
     a["A"]["sd_medians"] >= 0.5 and a["A"]["rho_people"] < 0.5, f"SD {a['A']['sd_medians']}, rho {a['A']['rho_people']}"),
    ("P1 OWN", "rho(D, A) exceeds rho(D, people)", a["D"]["rho_family"] > a["D"]["rho_people"],
     f"{a['D']['rho_family']} vs {a['D']['rho_people']}"),
]
if all(x in a for x in "BSV"):
    P += [
        ("P2 TRUTH REFUSED", "at least two of six B makers say the told values do not fit (S168.ORDER clause 1)",
         noticed["B"] >= 2, f"{noticed['B']} of 6 (blind coder {noticed_blind['B']})"),
        ("P3 TRUTH NOT TAUGHT", "rho(B, people) - rho(D, people) below 0.10 (S168.ORDER clause 2)",
         a["B"]["rho_people"] - a["D"]["rho_people"] < 0.10, f"{a['B']['rho_people']} - {a['D']['rho_people']}"),
        ("P4 THE CHECK RAN", "at least three of six S makers say the told values do not fit (S168.ORDER void clause)",
         noticed["S"] >= 3, f"{noticed['S']} of 6 (blind coder {noticed_blind['S']})"),
        ("P5 THE FITTING LIE PASSES", "at most one of six V makers says the told values do not fit",
         noticed["V"] <= 1, f"{noticed['V']} of 6 (blind coder {noticed_blind['V']})"),
        ("P6 FITTING LIE TEACHES LESS", "rho(V, people) below rho(B, people)",
         a["V"]["rho_people"] < a["B"]["rho_people"], f"{a['V']['rho_people']} vs {a['B']['rho_people']}"),
        ("P7 REFUSALS FOLLOW FIT", "noticed V <= B <= S, with V < S",
         noticed["V"] <= noticed["B"] <= noticed["S"] and noticed["V"] < noticed["S"], f"V {noticed['V']}, B {noticed['B']}, S {noticed['S']}"),
        ("P8 K", "no D, B, S or V KNOWN line begins with yes",
         not any((R[m]["known"] or "").lower().startswith("yes") for m in R if m[0] != "A"), "KNOWN lines read"),
    ]
res["predictions"] = [dict(id=p, claim=c, holds=h, numbers=n) for p, c, h, n in P]
(HERE / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
for arm in arms: print(arm, a[arm])
for p, c, h, n in P: print(f"{p:28s} {'HELD' if h else 'FAILED':6s} | {c} | {n}")
