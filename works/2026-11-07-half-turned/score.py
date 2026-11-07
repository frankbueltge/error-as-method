"""Scores Half Turned (Session 172). Reads rooms/, plan.json, people.json; writes results.json."""
import json, re, statistics as st
from pathlib import Path

HERE = Path(__file__).resolve().parent
plan = json.loads((HERE / "plan.json").read_text())
people = json.loads((HERE / "people.json").read_text())["occupations"]
scored, a_order = plan["scored"], plan["a_order"]
br = [people[o]["brazil"] for o in scored]
fr = [people[o]["france"] for o in scored]


def ranks(x):
    s = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and x[s[j + 1]] == x[s[i]]:
            j += 1
        for k in range(i, j + 1):
            r[s[k]] = (i + j) / 2
        i = j + 1
    return r


def rho(a, b):
    ra, rb = ranks(a), ranks(b)
    ma, mb = st.mean(ra), st.mean(rb)
    num = sum((p - ma) * (q - mb) for p, q in zip(ra, rb))
    den = (sum((p - ma) ** 2 for p in ra) * sum((q - mb) ** 2 for q in rb)) ** 0.5
    return num / den if den else float("nan")


def read(name, n):
    text = (HERE / "rooms" / f"{name}.txt").read_text()
    vals = {}
    for m in re.finditer(r"^(\d+):\s*(?:mean\s*)?(-?\d+(?:\.\d+)?)", text, re.M):
        vals[int(m.group(1))] = float(m.group(2))
    assert sorted(vals) == list(range(1, n + 1)), name
    how = re.search(r"^HOW:\s*(.*)$", text, re.M)
    known = re.search(r"^KNOWN:\s*(.*)$", text, re.M)
    return [vals[i] for i in range(1, n + 1)], how.group(1) if how else "", known.group(1) if known else None


res = {"arms": {}, "makers": {}}
# A: answering makers, re-indexed to the scored order
a_rows = []
for i in range(1, 7):
    v, how, _ = read(f"A{i}", 56)
    byocc = dict(zip(a_order, v))
    row = [byocc[o] for o in scored]
    a_rows.append(row)
    res["makers"][f"A{i}"] = {"rho_brazil": round(rho(row, br), 3), "how": how,
                              "all56": {o: byocc[o] for o in a_order}}
a_med = [st.median(c) for c in zip(*a_rows)]
res["family"] = {
    "medians_scored": dict(zip(scored, a_med)),
    "sd_medians": round(st.pstdev(a_med), 2),
    "spread_over_range": round(st.pstdev(a_med) / 100, 3),
    "rho_brazil": round(rho(a_med, br), 3), "rho_france": round(rho(a_med, fr), 3),
    "mean_medians": round(st.mean(a_med), 2), "mean_brazil": round(st.mean(br), 2),
    "level_departure": round(st.mean(br) - st.mean(a_med), 2),
}
for arm in "DBHR":
    rows = []
    for i in range(1, 7):
        v, how, known = read(f"{arm}{i}", 32)
        rows.append(v)
        res["makers"][f"{arm}{i}"] = {"rho_brazil": round(rho(v, br), 3), "rho_family": round(rho(v, a_med), 3),
                                      "sd": round(st.pstdev(v), 2), "mean": round(st.mean(v), 2),
                                      "how": how, "known": known}
    med = [st.median(c) for c in zip(*rows)]
    res["arms"][arm] = {"medians": dict(zip(scored, med)),
                        "rho_brazil": round(rho(med, br), 3), "rho_france": round(rho(med, fr), 3),
                        "rho_family": round(rho(med, a_med), 3), "sd_medians": round(st.pstdev(med), 2),
                        "mean_maker_rho_brazil": round(st.mean(res["makers"][f"{arm}{i}"]["rho_brazil"] for i in range(1, 7)), 3),
                        "mae_brazil": round(st.mean(abs(m - b) for m, b in zip(med, br)), 2)}
res["brazil_france_rho_scored"] = plan["rho_brazil_france_scored"]
(HERE / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
print(json.dumps({"family": {k: v for k, v in res["family"].items() if k != "medians_scored"},
                  "arms": {k: {kk: vv for kk, vv in v.items() if kk != "medians"} for k, v in res["arms"].items()}}, indent=1))
for k, v in res["makers"].items():
    if k[0] in "HR":
        print(k, v["rho_brazil"], v["sd"])
