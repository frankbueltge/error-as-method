"""score.py -- M1 mechanically from makers/*/NOTE.md, M2/M3 from coder/ratings.json via coder/key.json,
M4 from open.json (my coding, after M1-M3); scores P1-P8 as fixed in PREDICTIONS.md -> results.json."""
import json, os, re, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
J = lambda *p: json.load(open(os.path.join(HERE, *p)))
arm = {p["maker"]: p["arm"] for p in J("plan.json")}
STOP = {"a", "an", "the", "of", "on", "by", "in", "to", "and", "for", "at", "with", "from", "s",
        "moon", "moons", "lunar", "wikipedia", "views", "view", "page", "2025"}


def title(m):
    note = open(os.path.join(HERE, "makers", m, "NOTE.md"), encoding="utf-8").read()
    return re.search(r"^#+\s*(.+)$", note, re.M).group(1).strip(), note


def words(t):
    out = set()
    for w in re.findall(r"[a-z0-9]+", t.lower().replace("’", "'").replace("'", " ")):
        w = w[:-1] if w.endswith("s") and len(w) > 3 else w
        if w not in STOP:
            out.add(w)
    return out


R = [m for m in sorted(arm) if arm[m] == "R"]
r_words = set().union(*(words(title(m)[0]) for m in R))
key, rat, openc = J("coder", "key.json"), J("coder", "ratings.json"), J("open.json")
by_m = {v["maker"]: p for p, v in key.items()}
group_of = {}
for g in rat["groups_p"]:
    for p in g["members"]:
        group_of[key[p]["maker"]] = g["name"]

rows = {}
for m in sorted(arm):
    t, note = title(m)
    row = {"arm": arm[m], "title": t, "M1_overlap": sorted(words(t) & r_words) if arm[m] != "R" else None}
    if m in by_m:
        p = by_m[m]
        row.update({"picture": p, "M2_rating": rat["p"][p]["rating"], "M2_nearest": rat["p"][p]["nearest"],
                    "M2_words": rat["p"][p]["words"], "M3_group": group_of[m]})
    if m in openc:
        row["M4"] = openc[m]
    if arm[m] == "C":
        row["P7_mechanical_words"] = sorted(set(re.findall(r"\b(not|instead|unlike|none|rather than)\b", note.lower())))
    rows[m] = row

arms = {a: [m for m in rows if rows[m]["arm"] == a] for a in "DBC"}
mean = {a: sum(rows[m]["M2_rating"] for m in arms[a]) / 4 for a in "DBC"}
pair = {a: sum(rows[x]["M3_group"] == rows[y]["M3_group"] for x, y in itertools.combinations(arms[a], 2)) / 6 for a in "DBC"}
overlap = {a: sum(bool(rows[m]["M1_overlap"]) for m in arms[a]) for a in "DBC"}
r_groups = rat["groups_r"]
r_shared = sum(1 for x, y in itertools.combinations(R, 2) if words(rows[x]["title"]) & words(rows[y]["title"]))

P = {
 "P1": {"held": max(len(g["members"]) for g in r_groups) >= 4 or r_shared >= 1,
        "why": f"coder put r1-r6 in {len(r_groups)} group(s); {r_shared} round-1 title pairs share a content word"},
 "P2": {"held": mean["D"] >= 2.0 and overlap["D"] >= 2, "why": f"D mean {mean['D']:.2f}, {overlap['D']}/4 titles overlap"},
 "P3": {"held": mean["D"] - mean["B"] >= 1.0 and overlap["B"] <= 1,
        "why": f"D-B = {mean['D'] - mean['B']:.2f}, {overlap['B']}/4 B titles overlap"},
 "P4": {"held": mean["C"] < min(mean["B"], mean["D"]), "why": f"means D {mean['D']:.2f} B {mean['B']:.2f} C {mean['C']:.2f}"},
 "P5": {"held": pair["C"] > pair["D"], "why": f"within-arm pair rate D {pair['D']:.2f} B {pair['B']:.2f} C {pair['C']:.2f}"},
 "P6": {"held": all(rows[m]["M4"]["others"] for m in arms["B"] + arms["C"])
               and sum("AGAINST" in rows[m]["M4"]["stance"] for m in arms["B"]) >= 3,
        "why": f"{sum('AGAINST' in rows[m]['M4']['stance'] for m in arms['B'])}/4 B code AGAINST; all 8 mention others/"},
 "P7": {"held": sum(rows[m]["M4"]["negation_note"] for m in arms["C"]) >= 2,
        "why": f"{sum(rows[m]['M4']['negation_note'] for m in arms['C'])}/4 C notes coded as negation; mechanical word hits: "
               + ", ".join(f"{m} {rows[m]['P7_mechanical_words']}" for m in arms["C"])},
 "P8": {"held": True, "why": "all six round-1 works name 7 Sep 2025 on the picture (read off shots/m01-m06.png; see reports/)"},
}
out = {"rows": rows, "means": mean, "pair_rate": pair, "title_overlap": overlap, "round1_title_words": sorted(r_words),
       "predictions": P, "held": [k for k in P if P[k]["held"]], "failed": [k for k in P if not P[k]["held"]]}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1, ensure_ascii=False)
for k, v in P.items():
    print(k, "HELD" if v["held"] else "FAILED", "-", v["why"])
