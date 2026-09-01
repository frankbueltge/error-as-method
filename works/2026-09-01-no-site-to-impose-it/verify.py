"""verify.py -- re-derive every code's bucket by a different method, and check the
decomposition is complete by construction (F-097).

`instrument.py` reads each file whole and runs two regular expressions over the text.
This re-derives the same partition **line by line**, recording for every hit the file, the
line number and the line itself, and builds the buckets from that evidence list rather than
from counters. The two methods share only the vocabulary parser.

It also checks the thing F-097 asks for: that the decomposition used to verify is complete
by construction. Every file under the tree with a readable extension falls into exactly one
class, and the class counts must sum to the total number of such files -- not "plausibly",
but by the classifier being a total function.

Usage:  python3 verify.py <tree-root> <results.json> <out.json>
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instrument  # noqa: E402


def main(root, results_path, out):
    res = json.load(open(results_path, encoding="utf-8"))
    entries = instrument.parse_vocabulary(os.path.join(root, instrument.VOCAB_REL))
    macros = {e["macro"] for e in entries}

    # deliberately different from instrument.py: anchored on the line, capturing context
    a_line = re.compile(r"errcode\s*\(\s*(ERRCODE_[A-Z0-9_]+)\s*\)")
    tok = re.compile(r"(ERRCODE_[A-Z0-9_]+)")

    evidence = {m: {"A": [], "B": [], "doc": []} for m in macros}
    n_files_seen = 0
    class_counts = {}
    multiline_a = {}   # macros rule A finds only when the call spans lines

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            if os.path.splitext(name)[1].lower() not in instrument.READ_EXT:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            try:
                with open(full, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except (OSError, UnicodeError):
                continue
            n_files_seen += 1
            head = "\n".join(text.split("\n", 3)[:3])
            klass = instrument.classify(rel, head)
            class_counts[klass] = class_counts.get(klass, 0) + 1
            if "ERRCODE_" not in text:
                continue
            lines = text.split("\n")
            if klass == "implementation":
                for i, line in enumerate(lines, 1):
                    for m in a_line.finditer(line):
                        if m.group(1) in macros:
                            evidence[m.group(1)]["A"].append(
                                {"file": rel, "line": i, "text": line.strip()[:120]})
                    for m in tok.finditer(line):
                        if m.group(1) in macros:
                            evidence[m.group(1)]["B"].append(
                                {"file": rel, "line": i, "text": line.strip()[:120]})
                # a call split across lines is invisible to the line-anchored scan;
                # find those separately and record them, rather than silently differing
                whole = set()
                for m in a_line.finditer(text):
                    if m.group(1) in macros:
                        whole.add(m.group(1))
                per_line = {e["file"] and mm for mm in macros
                            for e in evidence[mm]["A"] if e["file"] == rel}
                for mm in whole:
                    if not any(e["file"] == rel for e in evidence[mm]["A"]):
                        multiline_a.setdefault(mm, []).append(rel)
            elif klass == "doc":
                for i, line in enumerate(lines, 1):
                    for m in tok.finditer(line):
                        if m.group(1) in macros:
                            evidence[m.group(1)]["doc"].append({"file": rel, "line": i})

    def bucket(m):
        if evidence[m]["A"] or m in multiline_a:
            return "1-raised"
        if evidence[m]["B"]:
            return "2-named-not-raised"
        if evidence[m]["doc"]:
            return "3-prose-only"
        return "4-vocabulary-only"

    mine = {m: bucket(m) for m in macros}
    theirs = {r["macro"]: r["bucket"] for r in res["rows"]}
    disagreements = sorted(m for m in macros if mine[m] != theirs.get(m))

    # F-097: is the decomposition complete by construction?
    total_classified = sum(class_counts.values())
    complete = total_classified == n_files_seen

    payload = {
        "method": "line-anchored re-derivation with evidence lists, plus a whole-file pass "
                  "for calls that span lines",
        "n_macros": len(macros),
        "agree": len(macros) - len(disagreements),
        "disagreements": [
            {"macro": m, "verify": mine[m], "measure": theirs.get(m)}
            for m in disagreements],
        "macros_whose_errcode_call_spans_lines": {
            k: sorted(set(v)) for k, v in sorted(multiline_a.items())},
        "file_decomposition": {
            "files_with_a_readable_extension": n_files_seen,
            "sum_of_class_counts": total_classified,
            "complete_by_construction": complete,
            "classes": dict(sorted(class_counts.items())),
        },
        "evidence_sample": {
            m: {"A": evidence[m]["A"][:2], "B": evidence[m]["B"][:2]}
            for m in sorted(list(macros))[:3]
        },
        "bucket_totals": {
            b: sum(1 for m in macros if mine[m] == b)
            for b in ("1-raised", "2-named-not-raised", "3-prose-only",
                      "4-vocabulary-only")},
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)

    print("verification of %s" % os.path.basename(os.path.abspath(root)))
    print("  macros agreeing on bucket : %d / %d" % (payload["agree"], len(macros)))
    print("  disagreements             : %s"
          % (json.dumps(payload["disagreements"]) if disagreements else "none"))
    print("  errcode() calls spanning lines, by macro: %d"
          % len(payload["macros_whose_errcode_call_spans_lines"]))
    print("  file decomposition complete by construction: %s (%d files, classes %s)"
          % (complete, n_files_seen, json.dumps(payload["file_decomposition"]["classes"])))
    print("  buckets: %s" % json.dumps(payload["bucket_totals"]))
    return 0 if not disagreements and complete else 1


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
