#!/usr/bin/env python3
"""Join the hand verdicts to the drawn sample and score P6.  Session 86, 2026-09-10.

Scores BEARER only, as pre-registered.  VOICE and SUBJECT are reported because the scheme asked for
them; the `note` column is post-hoc and scores nothing, which verdicts.py says at the top.
"""

import json
from collections import Counter
from pathlib import Path

from verdicts import V

HERE = Path(__file__).resolve().parent


def main():
    sample = json.load(open(HERE / "audit-sample.json"))
    rows = sample["rows"]
    assert len(rows) == 80 and set(V) == {r["id"] for r in rows}, "sample and verdicts disagree"

    out = []
    for r in rows:
        voice, subject, bearer, note = V[r["id"]]
        out.append({"id": r["id"], "arm": r["case"], "rfc": r["rfc"], "modal": r["modal"],
                    "slot_token": r["slot_token"], "sentence": r["sentence"],
                    "voice": voice, "subject": subject, "bearer": bearer, "note": note})

    def tal(arm):
        rs = [o for o in out if o["arm"] == arm] if arm else out
        return {"n": len(rs),
                "voice": dict(Counter(o["voice"] for o in rs).most_common()),
                "subject": dict(Counter(o["subject"] for o in rs).most_common()),
                "bearer": dict(Counter(o["bearer"] for o in rs).most_common()),
                "notes": sum(1 for o in rs if o["note"])}

    deleted = sum(1 for o in out if o["bearer"] == "DELETED")
    result = {
        "session": 86, "date": "2026-09-10",
        "scheme": "PREDICTIONS.md §3, fixed before the draw",
        "seed": sample["seed"], "population": sample["population"],
        "whole": tal(None), "UPPER": tal("UPPER"), "LOWER": tal("LOWER"),
        "P6": {"bar": "at least 40 of 80 rows BEARER=DELETED",
               "observed": deleted,
               "verdict": "WON" if deleted >= 40 else "LOST"},
        "post_hoc_not_scored": {
            "note": "added while reading the rows; the scheme has no bucket for it and P6 is scored "
                    "on BEARER alone. Counts of rows whose modal is not a norm addressed to anybody "
                    "in this document, or is not prose at all.",
            "not_deontic": [o["id"] for o in out if o["note"] and "NOT DEONTIC" in o["note"]],
            "not_prose": [o["id"] for o in out if o["note"] and "NOT PROSE" in o["note"]],
        },
        "rows": out,
    }
    (HERE / "adjudication.json").write_text(json.dumps(result, indent=1) + "\n")

    print("P6: %d of 80 rows BEARER=DELETED -> %s" % (deleted, result["P6"]["verdict"]))
    for arm in ("UPPER", "LOWER"):
        t = result[arm]
        print("  %-6s bearer %s | voice %s | subject %s"
              % (arm, t["bearer"], t["voice"], t["subject"]))
    ph = result["post_hoc_not_scored"]
    print("post hoc, scoring nothing: not-deontic %s ; not-prose %s"
          % (ph["not_deontic"], ph["not_prose"]))


if __name__ == "__main__":
    main()
