#!/usr/bin/env python3
"""verify -- Session 87, 2026-09-11.  Run before any number in this night is reported.

Two audits, and they exist because of two named faults.

**The port (F-130's condition).**  `S86.CONSTANT` asks for the committed instrument run *unchanged*.
This lifts the five rule literals out of Session 86's own `measure.py` source and asserts that
tonight's are byte for byte the same.  A port that quietly rewrote a regex would answer a different
question and nothing else here would notice.

**The extractor (F-128's lesson).**  Session 86 wrote its own parse of a document header, and it
returned an author's name as a title.  Tonight's extractor is a second hand-written parse, of
something considerably harder, so it is audited against an independent route: a flat regex over the
raw markup with tags stripped, which knows nothing about blocks, registers or furniture.  The two
counts will not agree exactly -- one drops code listings and support grids on purpose -- so what is
asserted is a *direction* and a *ceiling*: the extractor may never find a modal the flat count does
not, and everything it drops is reported per document rather than summed away.
"""

import gzip
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
S86 = HERE.parent / "2026-09-10-only-when-capitals" / "measure.py"
RAW = Path(__import__("os").environ.get("NIGHT_RAW", "/tmp/night-2026-09-11-raw"))

MODAL = re.compile(r"\b(shall|should|must)\b", re.IGNORECASE)

# the five literals this night claims to have ported unchanged
PORTED = {
    "MODAL_RE": r'MODAL_RE = re.compile\((r"[^"]+")',
    "B_FORM": r'B_FORM = re.compile\((r"[^"]+")',
    "BY": r'BY = re.compile\((r"[^"]+")',
    "AGENT_WINDOW": r'AGENT_WINDOW = (\d+)',
    "SENT_SPLIT": r'SENT_SPLIT = re.compile\((r"[^"]+")',
}


def ported_literals(path):
    src = path.read_text()
    out = {}
    for name, pat in PORTED.items():
        m = re.search(pat, src)
        if not m:
            raise SystemExit("verify: cannot find %s in %s" % (name, path))
        out[name] = m.group(1)
    return out


def flat_count(html):
    """The independent route: strip what is not prose, strip tags, count.  Knows nothing else."""
    t = re.sub(r"<(script|style|pre|svg|xmp|table)\b.*?</\1>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return len(MODAL.findall(t))


def main():
    report = {"session": 87, "date": "2026-09-11"}

    # ------------------------------------------------------------------ audit 1: the ported rules
    theirs = ported_literals(S86)
    mine = ported_literals(HERE / "measure.py")
    report["ported_rules"] = {"session_86": theirs, "session_87": mine,
                              "identical": theirs == mine}
    print("port: %s" % ("IDENTICAL" if theirs == mine else "DIFFERENT"))
    for k in PORTED:
        flag = "  " if theirs[k] == mine[k] else "!!"
        print("  %s %-13s %s" % (flag, k, theirs[k]))
    if theirs != mine:
        print("\nVERIFY FAILED: the instrument is not the one S86.CONSTANT asks for.", file=sys.stderr)
        (HERE / "verification.json").write_text(json.dumps(report, indent=1) + "\n")
        return 1

    # --------------------------------------------------------------- audit 2: the extractor's loss
    corpus = json.load(gzip.open(HERE / "corpus.json.gz", "rt"))
    rows, over = [], []
    for key, doc in sorted(corpus.items()):
        raw = RAW / (key + ".html")
        if not raw.exists():
            print("  (no cached markup for %s -- audit skipped)" % key)
            continue
        html = raw.read_text(encoding="utf-8", errors="replace")
        flat = flat_count(html)
        kept = sum(len(MODAL.findall(b["t"])) for b in doc["blocks"])
        rows.append({"doc": key, "flat_route": flat, "extractor": kept,
                     "dropped": flat - kept,
                     "dropped_share": round((flat - kept) / flat, 4) if flat else None})
        if kept > flat:
            over.append(key)
        print("  %-14s flat %6d   extractor %6d   dropped %5d" % (key, flat, kept, flat - kept))

    tf = sum(r["flat_route"] for r in rows)
    tk = sum(r["extractor"] for r in rows)
    report["extractor_audit"] = {
        "route": "tags stripped after removing script/style/pre/svg/xmp/table; no block, register "
                 "or furniture logic at all",
        "flat_route_total": tf, "extractor_total": tk,
        "dropped_total": tf - tk, "dropped_share": round((tf - tk) / tf, 4) if tf else None,
        "documents_where_extractor_exceeds_flat_route": over,
        "per_document": rows,
    }
    print("\n  TOTAL         flat %6d   extractor %6d   dropped %5d (%.2f %%)"
          % (tf, tk, tf - tk, 100 * (tf - tk) / tf))
    if over:
        print("VERIFY FAILED: extractor found modals the flat route did not, in %s" % over,
              file=sys.stderr)
        (HERE / "verification.json").write_text(json.dumps(report, indent=1) + "\n")
        return 1

    (HERE / "verification.json").write_text(json.dumps(report, indent=1) + "\n")
    print("\nverify: both audits pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
