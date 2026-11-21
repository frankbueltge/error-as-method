"""Session 183 (2026-11-21), the seventh night: the type held.

POST HOC. Reads only files committed by experiments 53, 55, 56 and 57 and prints, for each, where the makers
departed from what people had made (the token) and where they kept it (the type). Nothing is re-scored; every
number below is a count over committed results. Run from the repository root:

    python3 docs/research-notes/machine-practice/audits/2026-11-21-the-type-held/audit.py
"""
import json
import os
import sys

ROOT = os.getcwd()
W = os.path.join(ROOT, "works")


def load(*parts):
    with open(os.path.join(W, *parts), encoding="utf-8") as f:
        return json.load(f)


out = {}

# --- experiment 53, Carried On: the ending of each song (type) against the distance from the song (token) ----
ph = load("2026-11-15-carried-on", "posthoc.json")
rows = []
for s in ph["songs"]:
    e = s["endings_semitones_above_tonic"]
    people = e["people"]
    n_people = sum(people.values())
    people_tonic = people.get("0", 0)
    rows.append({
        "song": s["song"],
        "source_ending_above_tonic": e["source"],
        "people_on_tonic": [people_tonic, n_people],
        "parallel_on_tonic": [sum(1 for x in e["parallel"] if x == 0), len(e["parallel"])],
        "chain_on_tonic": [sum(1 for x in e["chain"] if x == 0), len(e["chain"])],
        "distance_median_people": s["tonic_rel_median"]["people"],
        "distance_median_parallel": s["tonic_rel_median"]["parallel"],
        "distance_link5_chain": s["tonic_rel"]["chain"][-1],
    })
out["53"] = rows

# --- experiment 56, Heard on Paper: the people's words (token) against their count and metre (type) ----------
hp = load("2026-11-19-heard-on-paper", "results.json")
hand = load("2026-11-19-heard-on-paper", "coding_hand.json")
p5 = hp["results"]["P5"]["per_song"]
out["56"] = {
    "named_arm_hand_coding": hand["tally"]["N"],
    "unnamed_arm_hand_coding": hand["tally"]["U"],
    "named_lines_with_canon_words_committed_rule": [hp["results"]["P3"]["canon"], hp["results"]["P3"]["of"]],
    "songs_where_named_counts_nearer_canon_syllables": [p5_n := sum(1 for v in p5.values() if v["N_nearer"]),
                                                       len(p5)],
}

# --- experiment 57, Four Cats, Twelve Drops: subject (type) against arrangement (token) ------------------------
sp = load("2026-11-20-seven-pieces", "results.json")
items = sp["items"]
w_items = [i for i in items if i["arm"] == "W"]
c_post = load("2026-11-20-seven-pieces", "posthoc.json")["items"]
w_cat_makers = sorted({i["maker"] for i in w_items if "cat" in i["name"].lower()})
out["57"] = {
    "word_first_makers_with_a_cat": [len(w_cat_makers), len({i["maker"] for i in w_items})],
    "word_first_names_on_people_shelf": [sp["predictions"]["P3"]["W_on_shelf"], sp["predictions"]["P3"]["of"]],
    "word_first_invalid_figures": sum(sp["predictions"]["P7"]["not_valid_per_maker"].values()),
    "drop_first_figures_whose_subject_turned": [sum(1 for i in c_post if i.get("turned")),
                                                sum(1 for i in c_post if i["maker"].startswith("c"))],
    "drop_first_names_on_people_shelf": [sp["predictions"]["P4"]["C_on_shelf"], sp["predictions"]["P4"]["of"]],
}

# --- experiment 55, The Record Names: a told record (the told case, Session 176's gloss) ---------------------
rn = load("2026-11-18-the-record-names", "results.json")
out["55"] = {k: rn[k] for k in ("P3", "P4", "P5")}

json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
print()

print("\n--- summary ---", file=sys.stderr)
for r in out["53"]:
    print(f"53 song {r['song']}: source ends {r['source_ending_above_tonic']} semitones above tonic; "
          f"people on tonic {r['people_on_tonic'][0]}/{r['people_on_tonic'][1]}, makers alone "
          f"{r['parallel_on_tonic'][0]}/{r['parallel_on_tonic'][1]}, chain {r['chain_on_tonic'][0]}/"
          f"{r['chain_on_tonic'][1]}; distance people {r['distance_median_people']}, alone "
          f"{r['distance_median_parallel']}, chain link 5 {r['distance_link5_chain']}", file=sys.stderr)
print("56", json.dumps(out["56"]), file=sys.stderr)
print("57", json.dumps(out["57"]), file=sys.stderr)
