#!/usr/bin/env python3
"""inspect.py -- RN2, measured after the verdicts were committed.

Session 91's modal_pos_in_block() finds the obligation sentence inside its block with str.find and,
when it is not there, silently places the modal at `offset` characters from the start of the block:

    i = block_text.find(sentence)
    return (0 if i < 0 else i) + offset

Every carrier Session 91, 94, 95 and tonight computed was the party term nearest THAT position.
This file counts, in each tradition this line has run the rule over, how many rows' sentences are
not found verbatim in the block they were assigned -- the rows whose carrier was measured from a
position the obligation does not occupy.  It changes nothing; it counts.

Writes `inspection.json`.

OUTCOME, written after the first run and kept in the docstring so the file does not read as a
live accusation: zero rows in four traditions.  RN2's suspicion was wrong.  Rows 6, 14 and 15 of
the sheet show contexts without their sentence because their carrier stands 176, 197 and 95 words
from the modal -- outside the sixty-word window, not outside the block.  The second half of this
file measures that instead, and the formula the reading kept meeting.
"""
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKS = HERE.parent
S91 = WORKS / "2026-09-17-the-second-instrument"
S94 = WORKS / "2026-09-21-three-other-offices"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V = _load(S91 / "validate.py", "s91_validate")
P = _load(S94 / "port.py", "s94_port")


def lost(docs, rows):
    miss = [r for r in rows if docs[r["doc"]][r["block"]].find(r["sentence"]) < 0]
    anywhere = 0
    for r in miss:
        if any(r["sentence"] in b for b in docs[r["doc"]]):
            anywhere += 1
    return len(rows), len(miss), anywhere


def main():
    out = {}
    for name, build in (("EU acts", P.eu), ("RFCs", P.rfc), ("WHATWG standards", P.whatwg),
                        ("UK Acts (calibration)", P.uk)):
        docs, rows = build()
        n, m, elsewhere = lost(docs, rows)
        out[name] = {"rows": n, "sentence_not_in_its_block": m,
                     "share": round(m / n, 4) if n else None,
                     "of_those_found_in_another_block_of_same_document": elsewhere}
        print("%-22s rows %5d   not in own block %5d  (%.2f %%)   found elsewhere in doc %d"
              % (name, n, m, 100 * m / n if n else 0, elsewhere))
    sheet = json.load(open(HERE / "sheet.json"))
    docs, _ = P.eu()
    out["tonight's sheet"] = [r["n"] for r in sheet["rows"]
                              if docs[r["celex"]][r["block"]].find(r["sentence"]) < 0]
    print("sheet rows whose sentence is not in their block:", out["tonight's sheet"])
    # --- the distance, which is what RN2 was actually seeing
    party = re.compile(V.term_pattern(V.base_terms() + P.EU_OWN), re.IGNORECASE)
    docs, rows = P.eu()
    dist, in_sentence = {}, []
    for r in sheet["rows"]:
        b = docs[r["celex"]][r["block"]]
        g = V.nearest_in_block(party, b, V.modal_pos_in_block(b, r["sentence"], r["offset"]))
        assert (g["start"], g["end"]) == (r["start"], r["end"]), r["n"]   # the sheet's span is the rule's
        dist[r["n"]] = [g["word_distance"], g["direction"]]
        si = b.find(r["sentence"])
        if si <= g["start"] < si + len(r["sentence"]):
            in_sentence.append(r["n"])
    out["sheet_word_distance"] = dist
    out["sheet_rows_whose_carrier_is_inside_the_obligation_sentence"] = in_sentence
    beyond = [n for n, (d, _) in dist.items() if d > 60]
    out["sheet_rows_carrier_beyond_the_sixty_word_window"] = beyond
    print("carrier inside the obligation sentence on", len(in_sentence), "of 20:", in_sentence)
    print("carrier more than 60 words from the modal:", beyond)
    # --- the comitology formula
    formula = re.compile(r"\bimplementing acts shall be adopted in accordance with the "
                         r"(examination|advisory) procedure", re.IGNORECASE)
    top = sheet["top_carrier"]
    frame = []
    for r in rows:
        b = docs[r["doc"]][r["block"]]
        g = V.nearest_in_block(party, b, V.modal_pos_in_block(b, r["sentence"], r["offset"]))
        if g is not None:
            frame.append((r, g["carrier"].casefold()))
    f_all = [bool(formula.search(r["sentence"])) for r in rows]
    f_top = [bool(formula.search(r["sentence"])) for r, c in frame if c == top]
    by_carrier = Counter(c for r, c in frame if formula.search(r["sentence"]))
    out["formula"] = {
        "pattern": formula.pattern,
        "population_rows": len(rows), "population_formula_rows": sum(f_all),
        "top_carrier_rows": len(f_top), "top_carrier_formula_rows": sum(f_top),
        "formula_rows_by_carrier": dict(by_carrier.most_common()),
        "sheet_formula_rows": [r["n"] for r in sheet["rows"] if formula.search(r["sentence"])],
    }
    print("formula rows: %d of %d in the population; %d of %d where the carrier is %r"
          % (sum(f_all), len(rows), sum(f_top), len(f_top), top))
    print("formula rows by carrier:", by_carrier.most_common(6))
    print("sheet formula rows:", out["formula"]["sheet_formula_rows"])
    (HERE / "inspection.json").write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
