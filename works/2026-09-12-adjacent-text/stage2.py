#!/usr/bin/env python3
"""stage2.py -- assemble the context window for each sampled row.

Not run until stage1-verdicts.json exists.  The window is fixed in PREDICTIONS.md §3 and is:

  * the enclosing heading chain -- walking back from the sentence's block, the nearest h6, then the
    nearest h5 above that, and so on up to h2, plus the document title;
  * the five blocks immediately preceding the sentence's own block;
  * the sentence's own block, whole.

Five is arbitrary.  It is declared as arbitrary in the pre-registration and it is not tuned here.
"""

import gzip
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "2026-09-11-eleven-sentences"
BACK = 5
HEADINGS = ("h2", "h3", "h4", "h5", "h6")


def heading_chain(blocks, index):
    """Nearest enclosing heading of each level, outermost first."""
    chain = []
    deepest = 7
    for j in range(index, -1, -1):
        g = blocks[j].get("g")
        if g in HEADINGS:
            level = int(g[1])
            if level < deepest:
                chain.append({"block": j, "tag": g, "text": blocks[j]["t"]})
                deepest = level
                if level == 2:
                    break
    return list(reversed(chain))


def main():
    if not (HERE / "stage1-verdicts.json").exists():
        raise SystemExit("stage1-verdicts.json does not exist -- stage 1 is not finished")

    corpus = json.load(gzip.open(SRC / "corpus.json.gz"))
    sample = json.load(open(HERE / "sample.json"))

    out = []
    for r in sample["rows"]:
        doc = corpus[r["doc"]]
        blocks = doc["blocks"]
        i = r["block"]
        out.append({
            "id": r["id"],
            "doc": r["doc"],
            "doc_title": doc["title"],
            "doc_url": doc["url"],
            "block": i,
            "headings": heading_chain(blocks, i),
            "before": [{"block": j, "tag": blocks[j].get("g"), "text": blocks[j]["t"]}
                       for j in range(max(0, i - BACK), i)],
            "own_block": blocks[i]["t"],
            "sentence": r["sentence"],
        })

    (HERE / "context.json").write_text(json.dumps(
        {"back": BACK, "rows": out}, indent=1) + "\n")

    with open(HERE / "stage2.txt", "w") as fh:
        fh.write("# Stage 2 -- heading chain, %d preceding blocks, own block.\n\n" % BACK)
        for r in out:
            fh.write("=" * 100 + "\n%s   [%s]\n" % (r["id"], r["doc_title"]))
            for h in r["headings"]:
                fh.write("  HEADING %-3s b%-6d %s\n" % (h["tag"], h["block"], h["text"]))
            for b in r["before"]:
                fh.write("  -%-2d %-4s %s\n"
                         % (r["block"] - b["block"], b["tag"] or "", b["text"][:600]))
            fh.write("  >>> OWN BLOCK b%d: %s\n" % (r["block"], r["own_block"][:1400]))
            fh.write("  *** SENTENCE: %s\n\n" % r["sentence"])

    print("wrote context.json and stage2.txt for %d rows" % len(out))


if __name__ == "__main__":
    main()
