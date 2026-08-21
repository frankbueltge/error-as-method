#!/usr/bin/env python3
"""Object-side classification of the corpus, for Session 64's title decision.

This does NOT decide anything. The decision is the signed hand-classification in
adjudication.json; this script only (1) proves the signed file covers every dated work
directory and no other, so nothing is silently dropped or invented — the fault Sessions 58
and 59 caught in this line's own instruments — and (2) computes the counts, including a
sensitivity check that flips every borderline row at once.

    python3 classify.py            # writes results.json beside this file
    python3 classify.py --check    # exits non-zero if adjudication != the works on disk

Stdlib only, deterministic, offline. Run from anywhere; paths resolve to the repo root.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
WORKS = os.path.join(ROOT, "works")
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-")


def dated_work_dirs():
    return sorted(
        d for d in os.listdir(WORKS)
        if DATED.match(d) and os.path.isdir(os.path.join(WORKS, d))
    )


def load_adjudication():
    with open(os.path.join(HERE, "adjudication.json"), encoding="utf-8") as fh:
        return json.load(fh)["works"]


def reconcile(adj, on_disk):
    """Every dated work is adjudicated, and every adjudicated slug exists. Both directions."""
    disk = set(on_disk)
    judged = set(adj)
    # This work is dated tonight; it is not part of the corpus it measures.
    judged_missing = disk - judged - {"2026-08-21-two-names-for-one-difference"}
    ghost = judged - disk
    return sorted(judged_missing), sorted(ghost)


def tally(adj, flip_borderline=False):
    by_class = {"W": 0, "N": 0, "M": 0}
    by_track_concrete = {}  # track -> {"W": n, "N": n}
    flip = {"W": "N", "N": "W"}
    for slug, row in adj.items():
        cls = row["class"]
        if flip_borderline and row.get("borderline") and cls in flip:
            cls = flip[cls]
        by_class[cls] += 1
        if cls in ("W", "N"):
            t = row["track"]
            by_track_concrete.setdefault(t, {"W": 0, "N": 0})
            by_track_concrete[t][cls] += 1
    return by_class, by_track_concrete


def main():
    adj = load_adjudication()
    on_disk = dated_work_dirs()
    missing, ghost = reconcile(adj, on_disk)

    if missing or ghost:
        for m in missing:
            print(f"FAIL unadjudicated work on disk: {m}", file=sys.stderr)
        for g in ghost:
            print(f"FAIL adjudicated slug not on disk: {g}", file=sys.stderr)
        return 1
    if "--check" in sys.argv:
        print(f"OK: {len(adj)} works, adjudication reconciles with disk exactly")
        return 0

    base_class, base_track = tally(adj)
    flip_class, flip_track = tally(adj, flip_borderline=True)
    borderline = sorted(s for s, r in adj.items() if r.get("borderline"))
    concrete = base_class["W"] + base_class["N"]

    results = {
        "corpus_dated_works": len(adj),
        "criterion": "sign of the object's difference from a norm: W wrong-result (present, wrong) / N non-arrival (expected, absent) / M meta (no located difference).",
        "by_class": base_class,
        "concrete_works_W_plus_N": concrete,
        "share_of_concrete": {
            "W": round(base_class["W"] / concrete, 3),
            "N": round(base_class["N"] / concrete, 3),
        },
        "by_track_concrete_only": base_track,
        "track_C_is_all_non_arrival": base_track.get("C", {}).get("W", 0) == 0,
        "borderline_rows": borderline,
        "sensitivity_flip_all_borderline": {
            "by_class": flip_class,
            "by_track_concrete_only": flip_track,
            "track_C_still_all_non_arrival": flip_track.get("C", {}).get("W", 0) == 0,
        },
        "_signed": "counts computed from adjudication.json; the classification is Ulysses', Session 64.",
    }
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
