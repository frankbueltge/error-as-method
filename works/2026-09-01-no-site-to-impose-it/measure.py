"""measure.py -- the population. PostgreSQL 18.6's error-code vocabulary against the
tree that publishes it.

Written after PREDICTIONS.md closed. Computes exactly the quantities P1-P6 name and
nothing that would have changed them.

Usage:  python3 measure.py <18.6-tree-root> <out.json>
"""

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import instrument  # noqa: E402


def main(root, out):
    res = instrument.measure(root)
    rows = res["rows"]
    n = len(rows)

    buckets = collections.Counter(r["bucket"] for r in rows)

    # P1 -- codes with zero occurrences in any implementation file
    siteless = [r for r in rows if r["sites_b"] == 0]
    p1 = len(siteless)

    # P2 -- of those, the share carrying a condition name
    with_condition = [r for r in siteless if r["condition"]]
    p2 = (len(with_condition) / p1) if p1 else 0.0

    # P3 -- named in implementation, never inside errcode( ... )
    named_not_raised = [r for r in rows if r["sites_b"] > 0 and r["sites_a"] == 0]
    p3 = len(named_not_raised)

    # P4 -- concentration of the siteless codes by SQLSTATE class
    by_class = collections.Counter(r["klass"] for r in siteless)
    top_class, top_n = (by_class.most_common(1)[0] if by_class else (None, 0))
    p4 = (top_n / p1) if p1 else 0.0

    # P5b -- rule A never exceeds rule B
    p5b = [r["macro"] for r in rows if r["sites_a"] > r["sites_b"]]

    # P6 -- macros the implementation names that the vocabulary lacks
    p6 = sorted(res["unknown_macros"])

    # context the argument needs, none of it a prediction
    raised = [r for r in rows if r["sites_a"] > 0]
    kinds = collections.Counter(r["kind"] for r in rows)
    siteless_kinds = collections.Counter(r["kind"] for r in siteless)
    no_condition = [r for r in rows if not r["condition"]]
    # of the codes that ARE raised, how many carry no condition name --
    # a norm the system imposes and the user cannot catch by name
    raised_no_condition = [r for r in raised if not r["condition"]]
    class_sections = {}
    for r in rows:
        class_sections.setdefault(r["klass"], r["section"])
    class_totals = collections.Counter(r["klass"] for r in rows)

    payload = {
        "tree": res["root"],
        "vocabulary_file": res["vocabulary_file"],
        "n_codes": n,
        "n_classes": len(class_totals),
        "file_classes": res["file_classes"],
        "buckets": dict(sorted(buckets.items())),
        "predictions": {
            "P1": {"quantity": "codes with zero occurrences in any implementation file",
                   "value": p1, "bar": 10, "won": p1 >= 10,
                   "of": n},
            "P2": {"quantity": "share of the P1 codes carrying a condition name",
                   "value": round(p2, 4), "bar": 0.5, "won": p2 >= 0.5,
                   "numerator": len(with_condition), "denominator": p1},
            "P3": {"quantity": "codes named in an implementation file but never inside "
                               "errcode( ... )",
                   "value": p3, "bar": 3, "won": p3 >= 3},
            "P4": {"quantity": "share of the P1 codes in the single largest SQLSTATE class",
                   "value": round(p4, 4), "bar": 0.25, "won": p4 >= 0.25,
                   "class": top_class, "class_section": class_sections.get(top_class),
                   "numerator": top_n, "denominator": p1},
            "P5b": {"quantity": "codes with sites_a > sites_b",
                    "value": len(p5b), "bar": 0, "won": not p5b, "members": p5b},
            "P6": {"quantity": "macro names in implementation files absent from the "
                               "vocabulary (DECLARED NOT BLIND)",
                   "value": p6,
                   "expected": ["ERRCODE_APPNAME_UNKNOWN", "ERRCODE_IS_CATEGORY",
                                "ERRCODE_TO_CATEGORY"],
                   "won": p6 == ["ERRCODE_APPNAME_UNKNOWN", "ERRCODE_IS_CATEGORY",
                                 "ERRCODE_TO_CATEGORY"],
                   "blind": False},
        },
        "siteless": [
            {"sqlstate": r["sqlstate"], "kind": r["kind"], "macro": r["macro"],
             "condition": r["condition"], "klass": r["klass"], "section": r["section"],
             "doc": r["doc"], "translation": r["translation"], "bucket": r["bucket"]}
            for r in siteless
        ],
        "siteless_by_class": [
            {"klass": k, "section": class_sections[k], "siteless": v,
             "class_total": class_totals[k]}
            for k, v in sorted(by_class.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        "named_not_raised": [
            {"sqlstate": r["sqlstate"], "kind": r["kind"], "macro": r["macro"],
             "condition": r["condition"], "section": r["section"],
             "sites_b": r["sites_b"], "files": r["files"]}
            for r in named_not_raised
        ],
        "context": {
            "kinds_all": dict(sorted(kinds.items())),
            "kinds_siteless": dict(sorted(siteless_kinds.items())),
            "codes_without_condition_name": len(no_condition),
            "raised_without_condition_name": len(raised_no_condition),
            "raised_without_condition_list": [
                {"sqlstate": r["sqlstate"], "macro": r["macro"],
                 "sites_a": r["sites_a"]} for r in raised_no_condition],
            "total_rule_a_sites": sum(r["sites_a"] for r in rows),
            "total_rule_b_sites": sum(r["sites_b"] for r in rows),
            "most_raised": [
                {"sqlstate": r["sqlstate"], "macro": r["macro"], "sites_a": r["sites_a"]}
                for r in sorted(rows, key=lambda r: -r["sites_a"])[:10]],
            "class_totals": dict(sorted(class_totals.items())),
            "class_sections": class_sections,
        },
        "rows": rows,
    }

    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True)

    p = payload["predictions"]
    print("%s -- %d codes in %d classes" % (res["root"], n, len(class_totals)))
    print("buckets: %s" % json.dumps(payload["buckets"]))
    for k in ("P1", "P2", "P3", "P4", "P5b", "P6"):
        print("  %-4s %-4s value=%s bar=%s"
              % (k, "WON" if p[k]["won"] else "LOST", p[k]["value"], p[k].get("bar")))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
