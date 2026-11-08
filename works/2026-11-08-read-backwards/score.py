"""Session 173, Read Backwards: score the 24 rooms against the true October 2026 views (log10, Spearman)."""
import json, os, re, math, statistics as st

# rank code copied from prepare.py (importing it would rewrite the briefs)
def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den



HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, "plan.json")))
scored, true = plan["scored"], plan["true"]
T = [math.log10(true[e]) for e in scored]


def read_room(rid):
    s = open(os.path.join(HERE, "rooms", rid + ".txt")).read()
    vals = {}
    for m in re.finditer(r"^\s*(\d+)\s*:\s*views\s*([\d,\.]+)", s, re.M):
        vals[int(m.group(1))] = float(m.group(2).replace(",", ""))
    assert sorted(vals) == list(range(1, 33)), (rid, sorted(vals))
    how = re.search(r"^HOW:\s*(.*)$", s, re.M)
    known = re.search(r"^KNOWN:\s*(.*)$", s, re.M)
    return [math.log10(max(vals[k], 1)) for k in range(1, 33)], (how.group(1) if how else ""), (known.group(1) if known else "")


out = {"arms": {}, "makers": {}}
med = {}
for arm in "UBHR":
    rows = []
    for n in range(1, 7):
        rid = f"{arm}{n}"
        v, how, known = read_room(rid)
        rows.append(v)
        out["makers"][rid] = {"rho": round(spearman(v, T), 3), "how": how, "known": known,
                              "log10": [round(x, 3) for x in v]}
    m = [st.median(col) for col in zip(*rows)]
    med[arm] = m
    lvl = st.median(abs(a - b) for a, b in zip(m, T))
    out["arms"][arm] = {"rho_truth": round(spearman(m, T), 3), "sd_log10_medians": round(st.stdev(m), 3),
                        "level_error_log10": round(lvl, 3), "mean_log10": round(st.mean(m), 3),
                        "maker_rhos": [out["makers"][f"{arm}{n}"]["rho"] for n in range(1, 7)],
                        "medians_log10": [round(x, 3) for x in m]}
for arm in "BHR":
    out["arms"][arm]["rho_with_U"] = round(spearman(med[arm], med["U"]), 3)
out["truth_log10"] = [round(x, 3) for x in T]
out["truth_mean_log10"] = round(st.mean(T), 3)
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
for arm, a in out["arms"].items():
    print(arm, {k: v for k, v in a.items() if k != "medians_log10"})
for rid, r in out["makers"].items():
    print(rid, r["rho"], r["known"], "|", r["how"][:200])
