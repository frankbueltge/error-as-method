"""Session 161: score experiment 42 exactly as PREDICTIONS.md defines it. Committed before any maker ran.
Run: python3 score.py   (reads plan.json, people.json, rooms/; writes results.json)
"""
import json, re, statistics as st
from pathlib import Path
HERE = Path(__file__).parent
plan = json.load(open(HERE / "plan.json"))
people = json.load(open(HERE / "people.json"))
KEYS = [k["key"] for k in plan["keys"]]
STEPS = [100 * i / 6 for i in range(7)]           # the people's seven steps on the 0-100 scale

def parse(mid):
    t = (HERE / "rooms" / f"{mid}.txt").read_text()
    order = plan["orders"][mid]
    out, meta = {}, {}
    for line in t.splitlines():
        m = re.match(r"\s*(\d+)\s*:\s*(.*)$", line)
        if m and 1 <= int(m.group(1)) <= 32:
            key = order[int(m.group(1)) - 1]
            if mid[0] == "A":
                n = re.search(r"(-?\d+(?:\.\d+)?)\s*$", m.group(2))
                if n: out[key] = float(n.group(1))
            else:
                d = dict((a, float(b)) for a, b in re.findall(r"(p10|p25|p50|p75|p90|mean)\s*=\s*(-?\d+(?:\.\d+)?)", m.group(2)))
                if "p50" in d: out[key] = d
        for tag in ("KNOWN", "HOW", "TOOLS"):
            if line.startswith(tag + ":"): meta[tag] = line[len(tag) + 1:].strip()
    return out, meta

def to7(v): return 1 + 6 * v / 100
def iqr(v):
    v = sorted(v); n = len(v)
    def q(p):
        i = (n - 1) * p; lo = int(i); hi = min(lo + 1, n - 1); return v[lo] + (v[hi] - v[lo]) * (i - lo)
    return q(.75) - q(.25)

makers = sorted(p.stem for p in (HERE / "rooms").glob("*.txt"))
data = {m: parse(m) for m in makers}
A = {k: st.median([data[m][0][k] for m in makers if m[0] == "A" and k in data[m][0]]) for k in KEYS}
A_mean = {k: st.mean([data[m][0][k] for m in makers if m[0] == "A" and k in data[m][0]]) for k in KEYS}
ppl = {k: people[k]["median"] for k in KEYS}
div = [k for k in KEYS if abs(A[k] - ppl[k]) >= 0.3]

def arm(letter):
    ms = [m for m in makers if m[0] == letter]
    conv = (lambda v: to7(v)) if letter == "F" else (lambda v: v)
    p50 = {m: {k: conv(data[m][0][k]["p50"]) for k in KEYS if k in data[m][0]} for m in ms}
    mean = {m: {k: conv(data[m][0][k]["mean"]) for k in KEYS if k in data[m][0] and "mean" in data[m][0][k]} for m in ms}
    places = []
    for m in ms:
        for k in div:
            if k in p50[m]:
                places.append({"maker": m, "key": k, "s": (p50[m][k] - A[k]) / (ppl[k] - A[k])})
    def kind(s):
        if abs(s) <= 0.1: return "family"
        if 0.1 < s < 0.9: return "between"
        if 0.9 <= s <= 1.1: return "people"
        return "beyond" if s > 1.1 else "wrong way"
    counts = {}
    for p in places:
        p["kind"] = kind(p["s"]); counts[p["kind"]] = counts.get(p["kind"], 0) + 1
    P = {k: st.mean([p50[m][k] for m in ms if k in p50[m]]) for k in KEYS}
    def mae(f): return st.mean(abs(A[k] + f * (P[k] - A[k]) - ppl[k]) for k in div)
    grid = [round(0.05 * i, 2) for i in range(51)]
    best = min(grid, key=mae)
    # the mean as a second target: s on the stated mean against the raters' mean and the people's mean
    mplaces = [(mean[m][k] - A_mean[k]) / (people[k]["mean"] - A_mean[k]) for m in ms for k in KEYS
               if k in mean[m] and abs(A_mean[k] - people[k]["mean"]) >= 0.3]
    res = {"makers": ms, "placements": len(places), "kinds": counts,
           "between_share": counts.get("between", 0) / len(places) if places else None,
           "mean_s": st.mean(p["s"] for p in places) if places else None,
           "P": P, "mae_f1": mae(1), "best_f": best, "mae_best": mae(best),
           "gain_best": 1 - mae(best) / mae(1) if mae(1) else None,
           "mae_all_keys": st.mean(abs(P[k] - ppl[k]) for k in KEYS),
           "mean_target": {"placements": len(mplaces),
                           "between_share": sum(1 for s in mplaces if 0.1 < s < 0.9) / len(mplaces) if mplaces else None},
           "place_list": places}
    if letter == "F":
        raw = [v for m in ms for k in KEYS if k in data[m][0] for v in data[m][0][k].values()]
        raw50 = [data[m][0][k]["p50"] for m in ms for k in KEYS if k in data[m][0]]
        res["F_numbers"] = len(raw)
        res["F_mult5_share"] = sum(1 for v in raw if abs(v / 5 - round(v / 5)) < 1e-9) / len(raw)
        res["F_mult10_share"] = sum(1 for v in raw if abs(v / 10 - round(v / 10)) < 1e-9) / len(raw)
        res["F_p50_on_step_share"] = sum(1 for v in raw50 if min(abs(v - s) for s in STEPS) <= 2) / len(raw50)
        res["F_p50_values"] = sorted(raw50)
    return res

S, F = arm("S"), arm("F")
iq = sum(1 for k in KEYS if iqr([data[m][0][k] for m in makers if m[0] == "A"]) < iqr(people[k]["ratings"]))
known = {m: data[m][1].get("KNOWN", "") for m in makers if m[0] != "A"}
pred = {
    "G_S": "held" if (S["between_share"] <= 0.30 and S["gain_best"] <= 0.15) else "falsified",
    "G_F": "falls" if (F["between_share"] > 0.30 or F["gain_best"] > 0.15) else "holds",
    "E": "held" if F["mae_f1"] >= 0.90 * S["mae_f1"] else "falsified",
    "R": "held" if F["F_mult5_share"] >= 0.80 else "falsified",
    "T": "held" if F["F_p50_on_step_share"] < 0.50 else "falsified",
    "I": "held" if iq >= 24 else "falsified",
    "K": "held" if not any(v.lower().startswith("yes") for v in known.values()) else "falsified",
}
void = len(div) < 8
out = {"diverging": div, "n_diverging": len(div), "void": void, "A": A, "A_mean": A_mean, "people_median": ppl,
       "S": S, "F": F, "iqr_narrower": iq, "known": known,
       "how": {m: data[m][1].get("HOW", "") for m in makers}, "tools": {m: data[m][1].get("TOOLS", "") for m in makers},
       "answered": {m: len(data[m][0]) for m in makers}, "predictions": pred}
json.dump(out, open(HERE / "results.json", "w"), indent=1)
for k, v in pred.items(): print(k, v)
print("diverging", len(div), "| S between", round(S["between_share"], 3), S["kinds"], "| F between", round(F["between_share"], 3), F["kinds"])
print("MAE S", round(S["mae_f1"], 3), "F", round(F["mae_f1"], 3), "| best f S", S["best_f"], round(S["gain_best"], 3), "F", F["best_f"], round(F["gain_best"], 3))
print("F mult5", round(F["F_mult5_share"], 3), "mult10", round(F["F_mult10_share"], 3), "p50 on step", round(F["F_p50_on_step_share"], 3))
print("mean target between: S", S["mean_target"], "F", F["mean_target"], "| IQR narrower", iq)
