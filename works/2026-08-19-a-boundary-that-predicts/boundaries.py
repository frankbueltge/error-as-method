#!/usr/bin/env python3
"""The mechanical half. Parse every harvested Lib/__future__.py and track, per feature,
how its two boundary fields (OptionalRelease, MandatoryRelease) read in each published
release of CPython.

This half decides nothing about *why* a boundary holds a value — only whether, and where,
it moved. The why is signed by hand in adjudication.json. Output → results.json.

stdlib only, offline, deterministic. Reads sources/ ; writes results.json.

    python3 boundaries.py
"""

import ast
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")


def series_key(s):
    """'2.10' sorts after '2.9', not after '2.1'."""
    a, b = s.split(".")
    return (int(a), int(b))


# A single _Feature assignment: `name = _Feature(<arg1>, <arg2>, <flag>)`. The whole file
# cannot be ast.parse'd — the Python 2.x releases in the population use backtick-repr syntax
# in __repr__, which is a hard SyntaxError under Python 3 — so each _Feature call is lifted
# out textually and only its first two arguments (the two boundary tuples) are evaluated.
_ASSIGN = re.compile(
    r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*_Feature\(", re.M)


def _split_args(s):
    """Split the top-level comma-separated arguments of a _Feature(...) call body, where the
    body is the text between the opening '(' after _Feature and its matching ')'. Tuples
    nest, so track depth."""
    args, depth, cur = [], 0, []
    for ch in s:
        if ch in "([{":
            depth += 1
            cur.append(ch)
        elif ch in ")]}":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            args.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip():
        args.append("".join(cur).strip())
    return args


def parse_features(text):
    """Return {feature_name: {'optional': tuple|None, 'mandatory': tuple|None}}. Robust to
    the Python 2 vintages in the population by evaluating only the boundary tuples."""
    out = {}
    for m in _ASSIGN.finditer(text):
        name = m.group(1)
        # Walk from the '(' after _Feature to its matching close paren.
        i = m.end() - 1
        depth, j = 0, i
        while j < len(text):
            if text[j] == "(":
                depth += 1
            elif text[j] == ")":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = text[i + 1:j]
        args = _split_args(body)
        if len(args) < 2:
            continue

        def as_release(a):
            a = a.strip()
            if a == "None":
                return None
            try:
                v = ast.literal_eval(a)
                return tuple(v) if isinstance(v, tuple) else "UNPARSED"
            except Exception:  # noqa: BLE001
                return "UNPARSED"

        out[name] = {"optional": as_release(args[0]), "mandatory": as_release(args[1])}
    return out


def release_short(rel):
    """(3, 10, 0, 'alpha', 0) -> '3.10' ; None -> None ; keep it to the minor version, which
    is the grain PEP 236 mints boundaries at."""
    if rel is None:
        return None
    if rel == "UNPARSED":
        return "UNPARSED"
    return f"{rel[0]}.{rel[1]}"


def main():
    manifest = json.load(open(os.path.join(SRC, "MANIFEST.json")))
    releases = {}
    for s in manifest["sources"]:
        if not s["key"].startswith("future-") or s["status"] != 200:
            continue
        series = s["series"]
        text = open(os.path.join(SRC, s["local"].split(" ")[0])).read()
        releases[series] = parse_features(text)

    ordered = sorted(releases, key=series_key)

    # Every feature name that has ever appeared, in first-appearance order.
    seen = []
    for series in ordered:
        for name in releases[series]:
            if name not in seen:
                seen.append(name)

    per_feature = {}
    for name in seen:
        opt_track = []   # (series, short) where the value is present
        man_track = []
        for series in ordered:
            f = releases[series].get(name)
            if f is None:
                continue
            opt_track.append((series, release_short(f["optional"]), f["optional"]))
            man_track.append((series, release_short(f["mandatory"]), f["mandatory"]))

        def distinct_run(track):
            """Collapse consecutive equal values into (value, first_series_it_held)."""
            run = []
            for series, short, full in track:
                if not run or run[-1]["value"] != short:
                    run.append({"value": short, "since": series, "full": list(full) if isinstance(full, tuple) else full})
            return run

        opt_runs = distinct_run(opt_track)
        man_runs = distinct_run(man_track)
        introduced = opt_track[0][0] if opt_track else None
        gap = None
        if man_runs and man_runs[-1]["value"] not in (None, "UNPARSED"):
            o = opt_runs[0]["full"]
            m = man_runs[-1]["full"]
            if isinstance(o, list) and isinstance(m, list):
                gap = (m[0] - o[0]) * 100 + (m[1] - o[1])  # minor-version distance, base-100
        per_feature[name] = {
            "introduced_in": introduced,
            "optional_values": [r["value"] for r in opt_runs],
            "optional_changed": len(opt_runs) - 1,
            "mandatory_runs": man_runs,
            "mandatory_changed": len(man_runs) - 1,
            "final_mandatory": man_runs[-1]["value"] if man_runs else None,
            "gap_minor_versions": gap,
        }

    # ---- the numbers the predictions resolve against ----
    others = {n: v for n, v in per_feature.items() if n != "annotations"}
    p1_moved = sum(1 for v in others.values() if v["mandatory_changed"] > 0)
    p3_opt_moved = sum(1 for v in per_feature.values() if v["optional_changed"] > 0)
    p3_man_moved = sum(1 for v in per_feature.values() if v["mandatory_changed"] > 0)
    gaps = sorted({v["gap_minor_versions"] for v in per_feature.values()
                   if v["gap_minor_versions"] is not None})

    summary = {
        "releases_measured": ordered,
        "n_releases": len(ordered),
        "features": seen,
        "n_features": len(seen),
        "P1_other_than_annotations_mandatory_moved": {
            "count": p1_moved,
            "which": [n for n, v in others.items() if v["mandatory_changed"] > 0],
            "prediction": "at most 2",
            "holds": p1_moved <= 2,
        },
        "P3_field_asymmetry": {
            "optional_ever_moved": p3_opt_moved,
            "mandatory_ever_moved": p3_man_moved,
            "prediction": "optional 0, mandatory >= 1",
            "holds": p3_opt_moved == 0 and p3_man_moved >= 1,
        },
        "P4_gap_distinct_values": {
            "gaps_base100_minor": gaps,
            "n_distinct": len(gaps),
            "prediction": "at least 3 distinct",
            "holds": len(gaps) >= 3,
        },
    }

    out = {
        "night": "2026-08-19",
        "session": 62,
        "what_this_measures": (
            "How the two boundary fields of each __future__ feature read across every "
            "published CPython release. The 'why' is not here; it is signed by hand in "
            "adjudication.json. Gap is expressed base-100 in minor versions: 208 means the "
            "mandatory release is 2 major + 8 minor beyond the optional one."
        ),
        "summary": summary,
        "per_feature": per_feature,
    }
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
        fh.write("\n")

    print(f"releases measured : {len(ordered)}  ({ordered[0]} .. {ordered[-1]})")
    print(f"features          : {len(seen)}")
    print(f"P1 (others' mandatory moved) : {p1_moved}  -> {'HOLDS' if p1_moved <= 2 else 'FAILS'} (pred <=2)")
    print(f"P3 optional moved : {p3_opt_moved}   mandatory moved : {p3_man_moved}  -> "
          f"{'HOLDS' if summary['P3_field_asymmetry']['holds'] else 'FAILS'}")
    print(f"P4 distinct gaps  : {len(gaps)} {gaps}  -> {'HOLDS' if len(gaps) >= 3 else 'FAILS'}")
    print()
    for n, v in per_feature.items():
        runs = " -> ".join(str(r["value"]) for r in v["mandatory_runs"])
        print(f"  {n:<18} opt {v['optional_values'][0]:<5} (moved {v['optional_changed']})   "
              f"mand [{runs}] (moved {v['mandatory_changed']})")


if __name__ == "__main__":
    main()
