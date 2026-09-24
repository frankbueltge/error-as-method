#!/usr/bin/env python3
"""draw.py -- the census of carriers in the EU frame, and twenty occurrences of the top one.

Fixed in PREDICTIONS.md §3 before this file was written.  Nothing is reimplemented: the population
is Session 94's port.eu(), the vocabulary Session 88's base terms plus Session 94's EU_OWN, the
carrier Session 91's nearest_in_block -- all imported by path and called.

Writes `census.json` (every carrier in the frame, counted) and `sheet.json` (twenty rows, each with
sixty words either side of the carrier span, the span marked with [[ ]]).  It writes no verdict and
runs no rule.
"""
import importlib.util
import json
import random
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKS = HERE.parent
S91 = WORKS / "2026-09-17-the-second-instrument"
S94 = WORKS / "2026-09-21-three-other-offices"

SEED = 96
SAMPLE = 20
SIDE = 60                                  # words either side of the carrier span
WORD = re.compile(r"\S+")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V = _load(S91 / "validate.py", "s91_validate")
P = _load(S94 / "port.py", "s94_port")


def window(block_text, s, e):
    """Sixty words either side of the carrier span, the span marked [[ ]]."""
    before = block_text[:s].split()
    after = block_text[e:].split()
    return (("... " if len(before) > SIDE else "") + " ".join(before[-SIDE:]) + " [["
            + block_text[s:e] + "]] " + " ".join(after[:SIDE]) + (" ..." if len(after) > SIDE else ""))


def main():
    docs, rows = P.eu()
    party = re.compile(V.term_pattern(V.base_terms() + P.EU_OWN), re.IGNORECASE)
    frame = []
    for r in rows:
        block_text = docs[r["doc"]][r["block"]]
        pos = V.modal_pos_in_block(block_text, r["sentence"], r["offset"])
        got = V.nearest_in_block(party, block_text, pos)
        if got is None:
            continue
        frame.append({"celex": r["doc"], "block": r["block"], "offset": r["offset"],
                      "sentence": r["sentence"], "carrier": got["carrier"],
                      "start": got["start"], "end": got["end"],
                      "context": window(block_text, got["start"], got["end"])})
    census = Counter(f["carrier"].casefold() for f in frame)
    ranked = sorted(census.items(), key=lambda kv: (-kv[1], kv[0]))   # ties alphabetical, §3
    top = ranked[0][0]
    (HERE / "census.json").write_text(json.dumps({
        "population_b_form_agentless_articles": len(rows),
        "frame_block_window_0": len(frame),
        "carriers_casefolded": dict(ranked),
    }, indent=1, ensure_ascii=False) + "\n")
    pool = sorted((f for f in frame if f["carrier"].casefold() == top),
                  key=lambda f: (f["celex"], f["block"], f["offset"], f["sentence"]))
    random.seed(SEED)
    picked = random.sample(pool, SAMPLE)
    sheet = {
        "note": "Twenty occurrences of the top carrier, drawn with random.seed(96) before any "
                "verdict was written. The reader answers per PREDICTIONS.md section 4: is the "
                "marked span, in this occurrence, a party? YES / NO / UNDECIDED.",
        "top_carrier": top, "occurrences_of_top_in_frame": len(pool),
        "seed": SEED, "sampled": SAMPLE,
        "rows": [dict(n=i + 1, **{k: f[k] for k in ("celex", "block", "offset", "carrier",
                                                   "start", "end", "sentence", "context")})
                 for i, f in enumerate(picked)],
    }
    (HERE / "sheet.json").write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + "\n")
    print("EU B-FORM/AGENTLESS/articles population : %d" % len(rows))
    print("of them, block window 0 under NARROW    : %d" % len(frame))
    print("distinct carriers (case-folded)          : %d" % len(census))
    for t, c in ranked[:8]:
        print("   %-22s %5d  %.2f %%" % (t, c, 100 * c / len(frame)))
    print("top carrier: %r, %d occurrences; drew %d with seed %d" % (top, len(pool), SAMPLE, SEED))


if __name__ == "__main__":
    main()
