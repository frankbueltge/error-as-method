#!/usr/bin/env python3
"""The decomposition.  Session 86, 2026-09-10.

NOT PRE-REGISTERED.  It scores no prediction and is marked post-hoc wherever it is used.  It exists
because the pre-registered numbers, once printed, made a structural fact visible that neither this
night nor Session 84 had looked for.

Session 84's measure is

    bearer_deletion_rate = AGENTLESS / all occurrences of the three modals

and AGENTLESS is a B-FORM with no "by" in the window.  So the rate is a product of two things:

    rate  =  P(the modal is followed by "be ___")   x   P(no "by" | it is)
             ------------- the B-FORM share -------     ---- the agent test ----

This file computes both factors, in every cell of tonight's corpus and in the four cells of Session
84's, and asks which of them carries the variation the two nights have been reporting.

Session 84's occurrences are read from `works/2026-09-08-no-one-to-bear-it/occurrences.json.gz`, a
frozen artefact of a landed night.  Nothing there is re-measured; the rows are re-tallied.
"""

import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
S84 = HERE.parent / "2026-09-08-no-one-to-bear-it"


def cell(rows, label):
    n = len(rows)
    b = [r for r in rows if r["form"] == "B-FORM"]
    al = [r for r in b if r["agent"] == "AGENTLESS"]
    return {
        "cell": label,
        "occurrences": n,
        "b_form": len(b),
        "b_form_share": round(len(b) / n, 4) if n else None,
        "agentless": len(al),
        "no_by_given_b_form": round(len(al) / len(b), 4) if b else None,
        "rate": round(len(al) / n, 4) if n else None,
    }


def spread(cells, key):
    vals = [c[key] for c in cells if c[key] is not None and c["occurrences"] >= 100]
    if not vals:
        return None
    return {"min": min(vals), "max": max(vals), "spread_points": round(100 * (max(vals) - min(vals)), 1)}


def main():
    rfc = json.load(gzip.open(HERE / "occurrences.json.gz", "rt"))
    eu = json.load(gzip.open(S84 / "occurrences.json.gz", "rt"))

    rfc_cells = [cell(rfc, "RFC · all")]
    for c in ("UPPER", "LOWER"):
        rfc_cells.append(cell([r for r in rfc if r["case"] == c], "RFC · %s" % c))
    for w in ("must", "should"):
        for c in ("UPPER", "LOWER"):
            rfc_cells.append(cell([r for r in rfc if r["modal"] == w and r["case"] == c],
                                  "RFC · %s %s" % (w, c)))

    eu_cells = [cell(eu, "EU · all")]
    for p in ("recitals", "articles"):
        eu_cells.append(cell([r for r in eu if r["part"] == p], "EU · %s" % p))
    for w in ("shall", "should"):
        for p in ("recitals", "articles"):
            eu_cells.append(cell([r for r in eu if r["modal"] == w and r["part"] == p],
                                 "EU · %s %s" % (w, p)))

    allc = rfc_cells + eu_cells

    # The counterfactual: throw the agent test away and replace it with its corpus-wide average.
    # If the reported rates survive that, the agent test was not carrying them.
    const = {"RFC": rfc_cells[0]["no_by_given_b_form"], "EU": eu_cells[0]["no_by_given_b_form"]}
    counterfactual = []
    for c in allc:
        if c["occurrences"] < 100:
            continue
        k = "RFC" if c["cell"].startswith("RFC") else "EU"
        pred = round(c["b_form_share"] * const[k], 4)
        counterfactual.append({"cell": c["cell"], "reported_rate": c["rate"],
                               "rate_with_the_agent_test_replaced_by_its_corpus_average": pred,
                               "difference_points": round(100 * abs(pred - c["rate"]), 2)})

    out = {
        "session": 86, "date": "2026-09-10", "status": "post hoc; scores no prediction",
        "identity": "rate = b_form_share x no_by_given_b_form",
        "rfc": rfc_cells, "eu": eu_cells,
        "spread_over_cells_with_100_or_more_occurrences": {
            "b_form_share": spread(allc, "b_form_share"),
            "no_by_given_b_form": spread(allc, "no_by_given_b_form"),
            "rate": spread(allc, "rate"),
        },
        "agent_test_constants": const,
        "counterfactual": counterfactual,
    }
    (HERE / "decomposition.json").write_text(json.dumps(out, indent=1) + "\n")

    print("%-22s %7s %10s %12s %8s" % ("cell", "occ", "B-FORM", "no 'by'|B", "rate"))
    for c in allc:
        if c["occurrences"] < 100:
            continue
        print("%-22s %7d %10.4f %12.4f %8.4f"
              % (c["cell"], c["occurrences"], c["b_form_share"], c["no_by_given_b_form"], c["rate"]))
    print()
    for k, v in out["spread_over_cells_with_100_or_more_occurrences"].items():
        print("%-20s spread across those cells: %5.1f points  (%.4f .. %.4f)"
              % (k, v["spread_points"], v["min"], v["max"]))
    print("\nthe agent test replaced by its corpus-wide average (%s):" % const)
    print("%-22s %10s %10s %8s" % ("cell", "reported", "rebuilt", "diff pts"))
    for c in counterfactual:
        print("%-22s %10.4f %10.4f %8.2f"
              % (c["cell"], c["reported_rate"],
                 c["rate_with_the_agent_test_replaced_by_its_corpus_average"],
                 c["difference_points"]))


if __name__ == "__main__":
    main()
