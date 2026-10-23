"""Post hoc, written after score.py's result (H2 failed): where in the people's list does the
makers' one word stand? Writes posthoc.json. Nothing here was predicted.

usage: python3 posthoc.py
"""
import json
import statistics

plan = json.load(open("plan.json"))
r = json.load(open("results.json"))
rows = []
for k in plan["keys"]["S"]:
    c = r["cells"][k["id"]]
    people = [w for w, _ in k["people"]]
    share = {w: n / k["G"] for w, n in k["people"]}
    m = c["modal"]
    n = r["cells"]["N" + k["id"][1:]]
    rows.append({
        "id": k["id"], "cue": k["cue"], "stratum": k["stratum"],
        "makers_word": m, "makers_n_of_6": c["modal_n"],
        "people_top": people[0], "people_top_share": round(share[people[0]], 3),
        "makers_word_rank_in_people": people.index(m) + 1 if m in people else None,
        "makers_word_share_in_people": round(share.get(m, 0), 3),
        "N_word": n["modal"], "N_n_of_6": n["modal_n"], "N_unanimous": n["unanimous"],
        "N_word_equals_S_word": n["modal"] == m,
    })
on = [x for x in rows if x["makers_word"] == x["people_top"]]
off = [x for x in rows if x["makers_word"] != x["people_top"]]
summary = {
    "makers_word_is_people_top": len(on),
    "ranks_when_not_top": sorted([x["makers_word_rank_in_people"] for x in off],
                                 key=lambda v: (v is None, v)),
    "median_share_people_gave_makers_word": statistics.median(
        x["makers_word_share_in_people"] for x in rows),
    "median_share_people_gave_their_top": statistics.median(x["people_top_share"] for x in rows),
    "by_stratum_on_top": {s: sum(1 for x in on if x["stratum"] == s) for s in ("low", "mid", "high")},
    "N_unanimous_when_S_on_top": sum(x["N_unanimous"] for x in on),
    "N_unanimous_when_S_off_top": sum(x["N_unanimous"] for x in off),
    "N_same_word_as_S_when_off_top": sum(x["N_word_equals_S_word"] for x in off),
}
json.dump({"summary": summary, "rows": rows}, open("posthoc.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
for x in rows:
    print(x["cue"], x["stratum"], x["people_top"], x["people_top_share"], "|", x["makers_word"],
          x["makers_n_of_6"], x["makers_word_rank_in_people"], x["makers_word_share_in_people"],
          "| N:", x["N_word"], x["N_n_of_6"])
