"""Scores the six readings against home.json and against the forecast in PREDICTIONS.md.
The answers below are transcribed from readings/R-*.md (committed before home.py ran);
'-' = cannot say. 'by' = the channel the reading named as deciding.

  python3 score.py  ->  results.json
"""
import json
ORDER = ["A1", "A3", "A6", "A2", "A5", "A4"]
READ = {  # R1, R2, R3, R4, R5
    "A1": (("yes", "S+N"), ("May", "wave"), ("yes", "wave"), ("yes", "wave"), ("-", "")),
    "A3": (("yes", "wave"), ("May", "wave"), ("yes", "wave"), ("yes", "wave"), ("-", "")),
    "A6": (("yes", "wave"), ("-", ""), ("-", ""), ("yes", "wave"), ("-", "")),
    "A2": (("yes", "wave"), ("May", "wave"), ("yes", "wave"), ("yes", "wave"), ("-", "")),
    "A5": (("yes", "S+N"), ("-", ""), ("-", ""), ("no", "wave"), ("-", "")),
    "A4": (("yes", "S+N"), ("-", ""), ("-", ""), ("yes", "wave"), ("-", "")),
}
FORECAST = {  # PREDICTIONS.md table; 'month' = any definite month
    "A1": ("yes", "month", "yes", "-", "-"), "A2": ("yes", "month", "yes", "-", "-"),
    "A3": ("yes", "month", "yes", "-", "-"), "A4": ("yes", "-", "-", "-", "-"),
    "A5": ("yes", "-", "-", "yes", "-"), "A6": ("yes", "-", "-", "-", "-"),
}
Q = ["R1_day", "R2_season", "R3_coupling", "R4_irregular", "R5_peak_hour"]
home = json.load(open("home.json")); truth = [str(home[k]["answer"]) for k in Q]

cells, right, wrong, undecided, hits, channels = {}, 0, 0, 0, 0, {}
for a in ORDER:
    for i, (ans, by) in enumerate(READ[a]):
        f = FORECAST[a][i]
        hit = (f == ans) or (f == "month" and ans not in ("-", "yes", "no"))
        hits += hit
        if ans == "-":
            verdict = "silent"
        elif truth[i] == "undecided":
            verdict = "undecided"; undecided += 1
        else:
            verdict = "right" if ans == truth[i] else "wrong"
            right += verdict == "right"; wrong += verdict == "wrong"
        if by:
            channels[by] = channels.get(by, 0) + 1
        cells[f"{a}.{Q[i]}"] = {"answer": ans, "by": by, "home": truth[i], "verdict": verdict,
                                "forecast": f, "forecast_hit": bool(hit)}

per_q = {}
for i, k in enumerate(Q):
    answers = [READ[a][i][0] for a in ORDER]
    definite = [x for x in answers if x != "-"]
    per_q[k] = {"definite": len(definite), "silent": answers.count("-"),
                "contradictory": len(set(definite)) > 1}
mixed = sum(1 for v in per_q.values() if v["definite"] and v["silent"])
contra = [k for k, v in per_q.items() if v["contradictory"]]
r1_all = all(READ[a][0][0] == "yes" for a in ORDER)
r2_set = sorted(a for a in ORDER if READ[a][1][0] != "-")
out = {
    "home": dict(zip(Q, truth)), "cells": cells, "per_question": per_q,
    "definite": right + wrong + undecided, "right": right, "wrong": wrong,
    "forecast_hits": hits, "deciding_channel_counts": channels,
    "P1_mixed_questions": mixed, "P1_holds": mixed >= 3,
    "P2_contradictory_questions": contra, "P2_holds": not contra,
    "P3_holds": hits >= 21,
    "P4_share_right": round(right / (right + wrong), 3), "P4_holds": right / (right + wrong) >= 0.8,
    "P5_day_passes_all": r1_all, "P5_month_passes": r2_set,
    "P5_holds": r1_all and r2_set == ["A1", "A2", "A3"],
}
json.dump(out, open("results.json", "w"), indent=1)
for k in ("definite", "right", "wrong", "forecast_hits", "deciding_channel_counts", "P1_mixed_questions",
          "P1_holds", "P2_contradictory_questions", "P2_holds", "P3_holds", "P4_share_right", "P4_holds",
          "P5_month_passes", "P5_holds"):
    print(k, out[k])
print({k: [c["verdict"] for kk, c in cells.items() if kk.endswith(k)] for k in Q})
