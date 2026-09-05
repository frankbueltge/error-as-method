#!/usr/bin/env python3
"""Scores PREDICTIONS.md against results.json and census.json. Writes adjudication.json.

It also recomputes the totals block of census.json from the rows, because a hand-written total is
a place where a night can be wrong about its own data without noticing.
"""

import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
R = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
C = json.loads((HERE / "census.json").read_text(encoding="utf-8"))

rows = C["rows"]

# --- recomputed totals -------------------------------------------------------------------------
by_class, by_verdict = {}, {}
for row in rows:
    by_class[row["class"]] = by_class.get(row["class"], 0) + 1
    if row["class"] in ("safeguard", "third-party-duty"):
        key = "%s/%s" % (row["class"], row["verdict"])
        by_verdict[key] = by_verdict.get(key, 0) + 1
recomputed = {"atoms": len(rows), "by_class": by_class, "by_verdict": by_verdict,
              "rows_with_no_article_counterpart": sorted(r["id"] for r in rows if r["article"] == "none")}
claimed = C["totals"]
totals_agree = (claimed["atoms"] == len(rows)
                and claimed["by_class"] == by_class
                and claimed["totals_recomputed_by"] if "totals_recomputed_by" in claimed else True)

# --- the binary projection used by P4 ----------------------------------------------------------
# The mechanical rule asks: does this atom's head verb occur anywhere in the 99 articles?
# The hand asks: is there an article that carries this atom?  A row naming no article is the hand's
# UNMATCHED.  Both are coarse; that is the point of comparing them.
mech = {a["recital"]: [] for a in R["atoms"]["recital_atoms"]}
mech_by_index = [a["mechanical"] for a in R["atoms"]["recital_atoms"]]
hand_by_index = ["UNMATCHED" if r["article"] == "none" else "MATCHED" for r in rows]
disagreements = [
    {"id": rows[i]["id"], "recital": rows[i]["recital"], "atom": rows[i]["atom"][:90],
     "mechanical": mech_by_index[i], "hand": hand_by_index[i], "class": rows[i]["class"]}
    for i in range(len(rows)) if mech_by_index[i] != hand_by_index[i]
]

# --- the predictions ---------------------------------------------------------------------------
d = R["directed_normative"]
top_actor = max(d["per_actor_occurrences"].items(), key=lambda kv: kv[1])

unmatched_safeguards = [r for r in rows if r["class"] == "safeguard" and r["verdict"] == "unmatched"]

verdicts = [
    {
        "id": "P1", "blind": True,
        "claim": "between 60 and 110 of the 173 recitals contain at least one directed normative sentence",
        "observed": d["count"],
        "result": "WON" if 60 <= d["count"] <= 110 else "LOST",
        "note": "%d recitals, %d occurrences. Guideline 10 of the Joint Practical Guide says recitals "
                "'SHALL NOT CONTAIN NORMATIVE PROVISIONS'." % (d["count"], d["occurrences"]),
    },
    {
        "id": "P2", "blind": True,
        "claim": "the most frequently directed actor is 'the controller'",
        "observed": {"actor": top_actor[0], "occurrences": top_actor[1],
                     "all": d["per_actor_occurrences"]},
        "result": "WON" if top_actor[0] == "the controller" else "LOST",
    },
    {
        "id": "P3", "blind": False,
        "claim": "exactly one atom naming a concrete safeguard for a data subject has no counterpart "
                 "in the 99 articles, and it is recital 71's 'obtain an explanation'",
        "observed": {"count": len(unmatched_safeguards),
                     "atoms": [r["atom"] for r in unmatched_safeguards]},
        "result": ("WON" if len(unmatched_safeguards) == 1
                   and "explanation" in unmatched_safeguards[0]["atom"] else "LOST"),
        "note": "Won on its own wording and drawn too tight. The same 46 atoms contain two further "
                "norms with no article counterpart -- recital 68's technical-compatibility limit and "
                "recital 78's duty on producers -- which the prediction's phrase 'for a data subject' "
                "excludes by wording rather than by evidence. Rows with no article counterpart of any "
                "class: %s." % recomputed["rows_with_no_article_counterpart"],
    },
    {
        "id": "P4", "blind": True,
        "claim": "the mechanical and the hand verdict disagree on at least 5 of the 46 atoms",
        "observed": {"disagreements": len(disagreements), "detail": disagreements},
        "result": "WON" if len(disagreements) >= 5 else "LOST",
        "note": "The direction matters more than the count: the mechanical rule flags exactly one "
                "atom in the whole preamble, and it is a false positive (recital 71's 'challenge', "
                "granted by Article 22(3) as 'contest'), while the one atom a court has ruled to be "
                "missing passes the mechanical rule because 'obtain' occurs elsewhere in the articles. "
                "On the two cases that matter the machine is wrong both times, in both directions.",
    },
]

adjudication = {
    "date": "2026-09-05",
    "session": 81,
    "work": "works/2026-09-05-the-fourth-safeguard",
    "calibration": {
        "declared_in_advance": True,
        "recital_71_safeguards": len(R["calibration"]["recital_71_safeguards"]),
        "article_22_safeguards": len(R["calibration"]["article_22_safeguards"]),
        "diff": R["calibration"]["in_recital_not_in_article"],
        "passes": R["calibration"]["passes"],
        "note": "The check is that the extractor reproduces the four-against-three diff of recital 71 "
                "and Article 22(3). It does, and it also returns 'challenge the decision', which is "
                "granted as 'contest' -- so the calibration passes and, in passing, shows the tool's "
                "own false-positive rate on the smallest possible sample.",
    },
    "predictions": verdicts,
    "won": sum(1 for v in verdicts if v["result"] == "WON"),
    "lost": sum(1 for v in verdicts if v["result"] == "LOST"),
    "census_totals_recomputed": recomputed,
    "census_totals_as_written": claimed,
    "census_totals_agree": (claimed["atoms"] == recomputed["atoms"]
                            and claimed["by_class"] == recomputed["by_class"]),
}

(HERE / "adjudication.json").write_text(json.dumps(adjudication, ensure_ascii=False, indent=1),
                                        encoding="utf-8")

for v in verdicts:
    print("%s %-4s blind=%s  %s" % (v["id"], v["result"], v["blind"], v["claim"][:78]))
print("won %d / lost %d" % (adjudication["won"], adjudication["lost"]))
print("census totals agree with the rows:", adjudication["census_totals_agree"])
print("recomputed by_class:", by_class)
print("recomputed by_verdict:", by_verdict)
print("rows with no article counterpart:", recomputed["rows_with_no_article_counterpart"])
print("mechanical/hand disagreements:", len(disagreements))
