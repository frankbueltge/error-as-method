#!/usr/bin/env python3
"""Score Session 70's four predictions against the three grids.

Reads grids.json (written by harvest.py), parses every state of
src/internal/godebugs/table.go into a set of entry tuples, and computes the
set differences the predictions in PREDICTIONS.md name.

Stdlib only, offline, deterministic. Every parse failure is counted and
listed; nothing is dropped silently.

Usage:  python3 measure.py
Writes: results.json
"""

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
FIELDS = ("Name", "Package", "Changed", "Old", "Opaque", "Immutable")


def entry_block(text):
    """Return the body of `All = []Info{ ... }`, or None."""
    m = re.search(r"All\s*=\s*\[\]Info\{", text)
    if not m:
        return None
    i, depth = m.end(), 1
    while i < len(text) and depth:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
        i += 1
    return text[m.end():i - 1] if depth == 0 else None


def groups(body):
    """Top-level `{...}` groups inside the table body."""
    out, depth, start = [], 0, None
    in_str = False
    i = 0
    while i < len(body):
        ch = body[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append(body[start:i])
        i += 1
    return out


def parse_entry(g):
    """One `{Name: "x", ...}` group -> a six-field tuple, or None."""
    d = {"Name": None, "Package": "", "Changed": 0, "Old": "",
         "Opaque": False, "Immutable": False}
    for f in FIELDS:
        m = re.search(r"\b%s\s*:\s*([^,}]+)" % f, g)
        if not m:
            continue
        v = m.group(1).strip()
        if f in ("Name", "Package", "Old"):
            s = re.match(r'"((?:[^"\\]|\\.)*)"', v)
            if not s:
                return None
            d[f] = s.group(1)
        elif f == "Changed":
            if not re.fullmatch(r"\d+", v):
                return None
            d[f] = int(v)
        else:
            if v not in ("true", "false"):
                return None
            d[f] = (v == "true")
    if d["Name"] is None:
        return None
    return tuple(d[f] for f in FIELDS)


def parse_state(text):
    body = entry_block(text)
    if body is None:
        return None, "no All = []Info{ ... } block"
    es, bad = [], 0
    for g in groups(body):
        if not g.strip():
            continue
        e = parse_entry(g)
        if e is None:
            bad += 1
        else:
            es.append(e)
    if bad:
        return None, "%d unparsable entry groups" % bad
    if not es:
        return None, "empty table"
    return es, None


def grid_sets(states, label, blobs):
    """Parse every state of one grid; return the union of its entry tuples."""
    tuples, names, pairs, failures, per_state = set(), set(), set(), [], []
    for s in states:
        es, err = parse_state(blobs[s["blob"]])
        if es is None:
            failures.append({"grid": label, "point": s.get("point"),
                             "change": s.get("change"), "patchset": s.get("patchset"),
                             "reason": err})
            continue
        per_state.append((s, es))
        for e in es:
            tuples.add(e)
            names.add(e[0])
            pairs.add((e[0], e[2]))
    return {"tuples": tuples, "names": names, "pairs": pairs,
            "failures": failures, "states": per_state}


def main():
    g = json.load(open(os.path.join(HERE, "grids.json")))
    blobs = g["blobs"]
    by_grid = {"release": [], "commit": [], "patchset": []}
    for p in g["points"]:
        by_grid[p["grid"]].append(p)
    release = grid_sets(by_grid["release"], "release", blobs)
    commit = grid_sets(by_grid["commit"], "commit", blobs)
    patchset = grid_sets(by_grid["patchset"], "patchset", blobs)

    # --- P1: names in a patchset that no commit carried -------------------
    p1_names = sorted(patchset["names"] - commit["names"])

    # --- P2: (Name, Changed) pairs, Changed != 0, in no commit ------------
    p2_pairs = sorted(p for p in (patchset["pairs"] - commit["pairs"]) if p[1] != 0)

    # --- P3: full tuples at a commit that no release carried --------------
    p3_tuples = sorted(commit["tuples"] - release["tuples"])
    p3_reduced_names = sorted(commit["names"] - release["names"])
    p3_reduced_pairs = sorted(commit["pairs"] - release["pairs"])

    # --- P4: provenance of every P2 pair ----------------------------------
    prov = {}
    for s, es in patchset["states"]:
        for e in es:
            key = (e[0], e[2])
            if key in set(p2_pairs):
                prov.setdefault("%s@%d" % key, []).append({
                    "change": s["change"], "patchset": s["patchset"],
                    "status": s["status"], "branch": s["branch"],
                    "subject": s["subject"], "created": s["created"],
                    "sha": s["point"], "ref": s["ref"],
                })
    p4_status = sorted({d["status"] for v in prov.values() for d in v})

    # the same, one level up, for the names P1 found
    prov_names = {}
    for s, es in patchset["states"]:
        for e in es:
            if e[0] in set(p1_names):
                prov_names.setdefault(e[0], []).append({
                    "change": s["change"], "patchset": s["patchset"],
                    "status": s["status"], "subject": s["subject"],
                    "created": s["created"], "tuple": list(e),
                })

    # --- the reverse direction: is commit a subset of patchset? -----------
    commit_only_names = sorted(commit["names"] - patchset["names"])
    commit_only_tuples_n = len(commit["tuples"] - patchset["tuples"])

    res = {
        "session": 70,
        "date": "2026-08-25",
        "path": g["path"],
        "population": g["population"],
        "grid_sizes": {
            "release": {"states": len(release["states"]), "tuples": len(release["tuples"]),
                        "names": len(release["names"]), "pairs": len(release["pairs"])},
            "commit": {"states": len(commit["states"]), "tuples": len(commit["tuples"]),
                       "names": len(commit["names"]), "pairs": len(commit["pairs"])},
            "patchset": {"states": len(patchset["states"]), "tuples": len(patchset["tuples"]),
                         "names": len(patchset["names"]), "pairs": len(patchset["pairs"])},
        },
        "parse_failures": release["failures"] + commit["failures"] + patchset["failures"],
        "P1": {"claim": "a Name in some patchset and in no commit",
               "count": len(p1_names), "names": p1_names,
               "verdict": "CONFIRMED" if p1_names else "LOST"},
        "P2": {"claim": "a (Name, Changed) pair, Changed != 0, in some patchset and in no commit",
               "count": len(p2_pairs), "pairs": [list(p) for p in p2_pairs],
               "verdict": "CONFIRMED" if p2_pairs else "LOST"},
        "P3": {"claim": "a full six-field tuple at some commit that no release tag carried",
               "count": len(p3_tuples), "tuples": [list(t) for t in p3_tuples],
               "reduced_names_only": p3_reduced_names,
               "reduced_name_changed_pairs": [list(p) for p in p3_reduced_pairs],
               "verdict": "CONFIRMED" if p3_tuples else "LOST"},
        "P4": {"claim": "if P2 holds, at least one such pair comes from a superseded patchset "
                        "of a change later MERGED",
               "statuses_seen": p4_status,
               "provenance": prov,
               "verdict": ("NOT APPLICABLE" if not p2_pairs
                           else "CONFIRMED" if "MERGED" in p4_status else "LOST")},
        "P1_provenance": prov_names,
        "reverse_direction": {
            "names_in_a_commit_and_in_no_patchset": commit_only_names,
            "tuples_in_a_commit_and_in_no_patchset": commit_only_tuples_n,
        },
    }
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(res, f, indent=1)

    for k in ("grid_sizes", "P1", "P2", "P3", "P4"):
        v = dict(res[k])
        v.pop("provenance", None)
        print(k, json.dumps(v, indent=1)[:1800])
    print("parse failures:", len(res["parse_failures"]))
    print("reverse:", json.dumps(res["reverse_direction"])[:400])


if __name__ == "__main__":
    main()
