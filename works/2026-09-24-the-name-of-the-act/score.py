#!/usr/bin/env python3
"""score.py -- the count, its grade, and the six predictions, scored mechanically.

Reads PREDICTIONS.md's fixed terms as constants here (quoted, not re-decided), `sheet.json`,
`verdicts.json`, `census.json`, `power.json` and `inspection.json`.  Writes `results.json`.
"""
import json
import re
from pathlib import Path

from power import clopper_pearson, pmf

HERE = Path(__file__).resolve().parent
BAR = 10
ACT_NAME = re.compile(r"\b(Commission|Council)\s+(Delegated\s+|Implementing\s+)?"
                      r"(Regulation|Directive|Decision)\b|of the European Parliament and of the Council")


def grade(k):
    """PREDICTIONS.md section 2, the four grades."""
    if k >= 15:
        return "falsified, and the sample can see it"
    if k >= 11:
        return "falsified by the row's bar, inside the coin band"
    if k >= 6:
        return "survives by the row's bar, inside the coin band"
    return "survives, and the sample can see it"


def main():
    sheet = json.load(open(HERE / "sheet.json"))
    ver = {v["n"]: v for v in json.load(open(HERE / "verdicts.json"))["verdicts"]}
    census = json.load(open(HERE / "census.json"))
    ins = json.load(open(HERE / "inspection.json"))
    assert sorted(ver) == list(range(1, 21))
    yes = sum(v["verdict"] == "YES" for v in ver.values())
    no = sum(v["verdict"] == "NO" for v in ver.values())
    und = sum(v["verdict"] == "UNDECIDED" for v in ver.values())
    k_strict, k_generous = yes, yes + und
    settled = (k_strict > BAR) == (k_generous > BAR)
    # RN1, the opposite reading of row 2
    k_rn1 = yes - (1 if ver[2]["verdict"] == "YES" else 0)
    top = sheet["top_carrier"]
    no_rows = [n for n, v in ver.items() if v["verdict"] == "NO"]
    def near_span(n, pad=60):
        ctx = sheet["rows"][n - 1]["context"]
        return ctx[max(0, ctx.index("[[") - pad):ctx.index("]]") + pad].replace("[[", "").replace("]]", "")

    act_name_no = [n for n in no_rows if ACT_NAME.search(near_span(n))]
    preds = {
        "P1 top carrier is 'member states' or 'commission'": top in ("member states", "commission"),
        "P2 top carrier is 'member states'": top == "member states",
        "P3 the row is falsified: YES > 10": k_strict > BAR and settled,
        "P4 k >= 15": k_strict >= 15,
        "P5 at least one NO is an act-name": bool(act_name_no),
        "P6 UNDECIDED at most 2": und <= 2,
    }
    lo, hi = clopper_pearson(k_strict, 20)
    res = {
        "top_carrier": top,
        "top_carrier_share_of_frame": round(census["carriers_casefolded"][top]
                                            / census["frame_block_window_0"], 4),
        "yes": yes, "no": no, "undecided": und,
        "k_strict": k_strict, "k_undecided_as_yes": k_generous, "settled": settled,
        "k_under_rn1_opposite_reading": k_rn1,
        "grade": grade(k_strict), "grade_under_rn1_opposite": grade(k_rn1),
        "clopper_pearson_95": [round(lo, 4), round(hi, 4)],
        "chance_of_k_or_more_if_true_share_were_one_half":
            round(sum(pmf(i, 20, 0.5) for i in range(k_strict, 21)), 8),
        "no_rows": no_rows, "act_name_no_rows": act_name_no,
        "S95.NOTPARTY": ("FALSIFIED" if k_strict > BAR and settled else
                         "SURVIVES" if settled else "NOT SETTLED"),
        "predictions": {k: ("HELD" if v else "FAILED") for k, v in preds.items()},
        "formula_rows_on_sheet": ins["formula"]["sheet_formula_rows"],
        "carrier_inside_obligation_sentence_on_sheet":
            ins["sheet_rows_whose_carrier_is_inside_the_obligation_sentence"],
    }
    (HERE / "results.json").write_text(json.dumps(res, indent=1) + "\n")
    for k, v in res.items():
        print("%-48s %s" % (k, v))


if __name__ == "__main__":
    main()
