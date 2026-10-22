"""Score experiment 35 by the rules fixed in PREDICTIONS.md. Writes results.json."""
import json, os, re, statistics
from prepare import srgb_to_lab, de, load_crowd

HERE = os.path.dirname(os.path.abspath(__file__))


def norm(s):
    s = s.strip().lower().replace("-", " ")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\bgray\b", "grey", s)
    return s


def parse(path):
    names, how, tools = {}, "", ""
    for line in open(path, encoding="utf8"):
        m = re.match(r"\s*(\d+)\s*:\s*(.+?)\s*$", line)
        if m and line.strip()[0].isdigit():
            names[int(m.group(1))] = m.group(2)
        elif line.startswith("HOW:"):
            how = line[4:].strip()
        elif line.startswith("TOOLS:"):
            tools = line[6:].strip()
    return names, how, tools


def pct(a, b):
    return round(100 * a / b, 1) if b else None


def main():
    plan = json.load(open(os.path.join(HERE, "plan.json")))
    crowd = {norm(n): h for n, h in load_crowd()}
    chips = {c["id"]: c for c in plan["chips"]}
    rows, makers = [], {}
    for m, d in plan["deal"].items():
        names, how, tools = parse(os.path.join(HERE, "rooms", m, "REPLY.txt"))
        makers[m] = {"condition": d["condition"], "how": how, "tools": tools, "answered": len(names)}
        for s in d["chips"]:
            c = chips[s["chip"]]
            raw = names.get(s["slot"], "")
            n = norm(raw)
            cn = norm(c["crowd_name"])
            inv = n in crowd
            rows.append({"maker": m, "cond": d["condition"], "side": s["side"], "chip": c["id"], "hex": s["hex"],
                         "crowd_name": c["crowd_name"], "name": raw, "exact": n == cn, "in_vocab": inv,
                         "head": bool(n) and n.split()[-1] == cn.split()[-1],
                         "dist": round(de(srgb_to_lab(s["hex"]), srgb_to_lab(crowd[n])), 2) if inv else None})
    cells = {}
    for cond in "NS":
        for side in ("on", "off", "all"):
            rs = [r for r in rows if r["cond"] == cond and (side == "all" or r["side"] == side)]
            ds = [r["dist"] for r in rs if r["dist"] is not None]
            cells[f"{cond}_{side}"] = {"n": len(rs), "exact": sum(r["exact"] for r in rs),
                                      "exact_pct": pct(sum(r["exact"] for r in rs), len(rs)),
                                      "in_vocab_pct": pct(sum(r["in_vocab"] for r in rs), len(rs)),
                                      "head_pct": pct(sum(r["head"] for r in rs), len(rs)),
                                      "median_dist": round(statistics.median(ds), 2) if ds else None, "n_dist": len(ds)}
    C = cells
    preds = {
        "P1": {"claim": "N on EXACT >= N off EXACT + 15 pp", "value": [C["N_on"]["exact_pct"], C["N_off"]["exact_pct"]],
               "held": C["N_on"]["exact_pct"] >= C["N_off"]["exact_pct"] + 15},
        "P2": {"claim": "|S on - S off| EXACT < 10 pp", "value": [C["S_on"]["exact_pct"], C["S_off"]["exact_pct"]],
               "held": abs(C["S_on"]["exact_pct"] - C["S_off"]["exact_pct"]) < 10},
        "P3": {"claim": "S EXACT < N on EXACT", "value": [C["S_all"]["exact_pct"], C["N_on"]["exact_pct"]],
               "held": C["S_all"]["exact_pct"] < C["N_on"]["exact_pct"]},
        "P4": {"claim": "N IN-VOCAB > S IN-VOCAB", "value": [C["N_all"]["in_vocab_pct"], C["S_all"]["in_vocab_pct"]],
               "held": C["N_all"]["in_vocab_pct"] > C["S_all"]["in_vocab_pct"]},
        "P5": {"claim": "median DIST N on < N off", "value": [C["N_on"]["median_dist"], C["N_off"]["median_dist"]],
               "held": C["N_on"]["median_dist"] is not None and C["N_off"]["median_dist"] is not None and C["N_on"]["median_dist"] < C["N_off"]["median_dist"]},
    }
    # per chip: does the same maker family give the crowd name on-list and lose it as a twin?
    per_chip = []
    for cid, c in chips.items():
        e = {}
        for cond in "NS":
            for side in ("on", "off"):
                rs = [r for r in rows if r["chip"] == cid and r["cond"] == cond and r["side"] == side]
                e[f"{cond}_{side}"] = [r["name"] for r in rs]
                e[f"{cond}_{side}_exact"] = sum(r["exact"] for r in rs)
        per_chip.append({"chip": cid, "crowd_name": c["crowd_name"], "on": c["on"], "off": c["off"], **e})
    out = {"cells": cells, "predictions": preds, "makers": makers, "per_chip": per_chip, "rows": rows}
    json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    for k, v in cells.items():
        print(k, v)
    for k, v in preds.items():
        print(k, v)


if __name__ == "__main__":
    main()
