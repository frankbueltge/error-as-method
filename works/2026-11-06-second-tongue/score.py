"""Session 171 (experiment 49, A Second Tongue): scores the rooms against PREDICTIONS.md and writes results.json.

Needs no download: reads people.json, plan.json, rooms/*.txt, coding/mine.json (my noticing codes, written before the blind
coder ran) and coding/key.json + coding/answer.txt (the blind coder's). Prints each prediction's text beside its verdict.
Run: python3 score.py
"""
import json, re, statistics as st
from pathlib import Path

HERE = Path(__file__).parent
people = json.loads((HERE / "people.json").read_text())
plan = json.loads((HERE / "plan.json").read_text())
scored = [k["id"] for k in plan["keys"] if k["role"] == "scored"]
l2 = {k: people[k]["l2"] for k in scored}
nat = {k: people[k]["native"] for k in scored}
RANGE = 6


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
    d = (sum((p - mx) ** 2 for p in x) * sum((q - my) ** 2 for q in y)) ** 0.5
    return sum((p - mx) * (q - my) for p, q in zip(x, y)) / d if d else 0.0


def room(mid):
    txt = (HERE / "rooms" / f"{mid}.txt").read_text()
    vals = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s*(\d+)\s*:\s*(?:mean\s*)?([0-9.]+)", txt, re.M)}
    arm = mid[0]; a = plan["makers"][mid]["arrangement"] - 1
    order = plan["arrangements_all"][a] if arm == "A" else plan["arrangements_scored"][a]
    assert sorted(vals) == list(range(1, len(order) + 1)), (mid, len(vals))
    how = re.search(r"^HOW:\s*(.*)$", txt, re.M); known = re.search(r"^KNOWN:\s*(.*)$", txt, re.M)
    return dict(values={order[i - 1]: v for i, v in vals.items()}, how=how.group(1).strip() if how else "",
                known=known.group(1).strip() if known else None, text=txt)


R = {f"{arm}{i}": room(f"{arm}{i}") for arm in "ADBSR" for i in range(1, 7) if (HERE / "rooms" / f"{arm}{i}.txt").exists()}
arms = [x for x in "ADBSR" if all(f"{x}{i}" in R for i in range(1, 7))]
acc = {arm: {k: st.median(R[f"{arm}{i}"]["values"][k] for i in range(1, 7)) for k in scored} for arm in arms}
res = {"arms": {}, "makers": {}}
for arm in arms:
    res["arms"][arm] = dict(rho_l2=round(rho(acc[arm], l2), 4), rho_native=round(rho(acc[arm], nat), 4),
                            rho_family=round(rho(acc[arm], acc["A"]), 4) if arm != "A" else None,
                            sd_medians=round(st.pstdev(acc[arm].values()), 4), mean_medians=round(st.mean(acc[arm].values()), 4),
                            mae_l2=round(st.mean(abs(acc[arm][k] - l2[k]) for k in scored), 4))
for m, r in R.items():
    if m[0] not in arms: continue
    res["makers"][m] = dict(rho_l2=round(rho(r["values"], l2), 4), rho_native=round(rho(r["values"], nat), 4),
                            rho_family=round(rho(r["values"], acc["A"]), 4), sd=round(st.pstdev(r["values"][k] for k in scored), 4),
                            mean=round(st.mean(r["values"][k] for k in scored), 4), how=r["how"], known=r["known"])
res["maker_means"] = {arm: {f: round(st.mean(res["makers"][f"{arm}{i}"][f] for i in range(1, 7)), 4)
                            for f in ("rho_l2", "rho_native", "rho_family", "sd")} for arm in arms}
res["publics"] = dict(l2_sd=round(st.pstdev(l2.values()), 4), native_sd=round(st.pstdev(nat.values()), 4),
                      rho_l2_native=round(rho(l2, nat), 4))
res["accounts"] = {arm: acc[arm] for arm in arms}

mine = json.loads((HERE / "coding" / "mine.json").read_text()) if (HERE / "coding" / "mine.json").exists() else {}
blind = {}
if (HERE / "coding" / "answer.txt").exists():
    key = json.loads((HERE / "coding" / "key.json").read_text())
    for m in re.finditer(r"(C\d\d)\s*:\s*(YES|NO)", (HERE / "coding" / "answer.txt").read_text()):
        blind[key[m.group(1)]] = m.group(2) == "YES"
told = [x for x in "BSR" if x in arms]
noticed = {arm: sum(1 for i in range(1, 7) if mine.get(f"{arm}{i}")) for arm in told}
noticed_blind = {arm: sum(1 for i in range(1, 7) if blind.get(f"{arm}{i}")) for arm in told}
res["noticed_mine"], res["noticed_blind"] = noticed, noticed_blind
res["coder_agreement"] = sum(1 for m in blind if blind[m] == bool(mine.get(m))) if blind else None

a = res["arms"]; mm = res["maker_means"]
spread = a["A"]["sd_medians"] / RANGE
P = [("P0 PREMISE", "SD of A medians >= 0.75 and rho(A, L2) < 0.5",
      a["A"]["sd_medians"] >= 0.75 and a["A"]["rho_l2"] < 0.5, f"SD {a['A']['sd_medians']}, rho {a['A']['rho_l2']}"),
     ("P0N WHOSE ORDER", "rho(A, native) >= rho(A, L2) + 0.3", a["A"]["rho_native"] >= a["A"]["rho_l2"] + 0.3,
      f"{a['A']['rho_native']} vs {a['A']['rho_l2']}")]
if "D" in arms:
    P.append(("P1 THE PUBLIC MODELLED", "rho(D, L2) >= rho(A, L2) + 0.2", a["D"]["rho_l2"] >= a["A"]["rho_l2"] + 0.2,
              f"{a['D']['rho_l2']} vs {a['A']['rho_l2']}"))
if all(x in arms for x in "DBSR") and mine:
    told_mean = st.mean(res["makers"][f"{x}{i}"]["rho_family"] for x in "BSR" for i in range(1, 7))
    P += [("P2 TRUTH REFUSED", "at least two of six B makers name a misfit (S168.ORDER clause 1)", noticed["B"] >= 2,
           f"{noticed['B']} of 6 (blind {noticed_blind['B']})"),
          ("P3 TRUTH NOT TAUGHT", "rho(B, L2) - rho(D, L2) < 0.10 (S168.ORDER clause 2)", a["B"]["rho_l2"] - a["D"]["rho_l2"] < 0.10,
           f"{a['B']['rho_l2']} - {a['D']['rho_l2']}"),
          ("P4 THE CHECK RAN", "at least three of six S makers name a misfit (S168.ORDER void clause)", noticed["S"] >= 3,
           f"{noticed['S']} of 6 (blind {noticed_blind['S']})"),
          ("P5 S170.SPREAD", "spread >= 0.20 -> S >= 3; spread < 0.20 -> S <= 2", (noticed["S"] >= 3) == (spread >= 0.20),
           f"spread {spread:.3f}, S {noticed['S']}"),
          ("P6 REVERSED REFUSED", "#R naming >= #S naming", noticed["R"] >= noticed["S"], f"R {noticed['R']}, S {noticed['S']}"),
          ("P7 S170.SILENT", "told makers' mean per-maker rho with A exceeds D's by >= 0.05 (void if D's > 0.9)",
           told_mean - mm["D"]["rho_family"] >= 0.05, f"told {told_mean:.4f} vs D {mm['D']['rho_family']}"),
          ("P8 K", "no D, B, S or R KNOWN line begins with yes",
           not any((R[m]["known"] or "").lower().startswith("yes") for m in R if m[0] != "A"),
           "; ".join(sorted({(R[m]['known'] or '')[:20] for m in R if m[0] != 'A'})))]
res["spread"] = round(spread, 4)
res["predictions"] = [dict(id=p, claim=c, holds=h, numbers=n) for p, c, h, n in P]
(HERE / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
for arm in arms: print(arm, a[arm], "| maker means", mm[arm])
print("publics", res["publics"], "spread", round(spread, 3))
for p, c, h, n in P: print(f"{p:24s} {'HELD' if h else 'FAILED':6s} | {c} | {n}")
