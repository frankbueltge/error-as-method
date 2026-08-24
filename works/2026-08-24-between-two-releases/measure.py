#!/usr/bin/env python3
"""Read the two boundary fields at every harvested state of Lib/__future__.py and ask the
question PREDICTIONS.md fixed: does a value exist between two releases that no release ever
carried?

Offline. stdlib only. Reads sources/blobs/ (harvested by harvest.py, not committed),
commits.json (committed) and Session 62's own results.json (committed, in this repository).

    python3 measure.py

Parsing note, and it matters. Ten of the forty commit states cannot be parsed by this
interpreter's `ast`: they use Python 2's backtick-repr syntax in _Feature.__repr__. A
Python-3 `ast.parse` raises SyntaxError on the whole file, which would silently drop the
first six years of the record — the exact period the question is about. So the extractor
below does not use `ast.parse` on the module. It finds each top-level assignment whose
right-hand side begins `_Feature(` or `Feature(` or a bare tuple pair, balances the
brackets by hand, and evaluates only the literal arguments with `ast.literal_eval`. Every
state that fails to yield is reported by name, never skipped.
"""

import ast
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BLOBS = os.path.join(HERE, "sources", "blobs")
S62 = os.path.join(HERE, os.pardir, "2026-08-19-a-boundary-that-predicts", "results.json")

# A top-level assignment: name at column 0, then '=', then the right-hand side.
ASSIGN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$", re.MULTILINE)

# Names that are module machinery, not features. all_feature_names and the CO_* flags are
# assignments too; excluding them by name is a norm I am imposing and it is declared here.
NOT_A_FEATURE = re.compile(r"^(CO_|all_feature_names$|__|_Feature$)")


def _balanced(text, start):
    """Return the substring from `start` (which indexes an opening bracket) to its match."""
    opens = "([{"
    closes = ")]}"
    depth = 0
    in_str = None
    i = start
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2
                continue
            if ch == in_str:
                in_str = None
        elif ch in "\"'":
            in_str = ch
        elif ch in opens:
            depth += 1
        elif ch in closes:
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
        i += 1
    return None


def _split_top(argtext):
    """Split a bracketed argument list on top-level commas."""
    inner = argtext[1:-1]
    parts, depth, cur, in_str = [], 0, [], None
    for ch in inner:
        if in_str:
            cur.append(ch)
            if ch == in_str:
                in_str = None
            continue
        if ch in "\"'":
            in_str = ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
            continue
        cur.append(ch)
    parts.append("".join(cur))
    return [p.strip() for p in parts if p.strip()]


def _literal(text):
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return "<unparsed:" + text.strip()[:40] + ">"


def extract(source):
    """feature name -> {'optional': tuple|None, 'mandatory': tuple|None, 'form': str}."""
    out = {}
    for m in ASSIGN.finditer(source):
        name, rhs = m.group(1), m.group(2).strip()
        if NOT_A_FEATURE.match(name):
            continue
        call = re.match(r"(_?Feature)\s*\(", rhs)
        if call:
            open_at = m.start(2) + call.end() - 1
            args = _balanced(source, open_at)
            if args is None:
                out[name] = {"optional": "<unbalanced>", "mandatory": "<unbalanced>",
                             "form": "call"}
                continue
            parts = _split_top(args)
            out[name] = {
                "optional": _literal(parts[0]) if len(parts) > 0 else None,
                "mandatory": _literal(parts[1]) if len(parts) > 1 else None,
                "form": "call/" + call.group(1),
            }
            continue
        # The oldest state of the file: `nested_scopes = (2,1,0,"beta",1), (2,2,0,"final",0)`
        if rhs.startswith("("):
            whole = source[m.start(2):]
            # a bare tuple pair may run to the end of the logical line only
            line_end = whole.find("\n\n")
            candidate = whole[:line_end if line_end > 0 else len(whole)].strip()
            val = _literal(candidate)
            if isinstance(val, tuple) and len(val) == 2 and all(
                    isinstance(v, tuple) for v in val):
                out[name] = {"optional": val[0], "mandatory": val[1], "form": "bare-pair"}
    return out


def minor(v):
    """The release a boundary tuple names, reduced the way S62 reduced it."""
    if v is None:
        return None
    if not isinstance(v, (list, tuple)) or len(v) < 2:
        return "<malformed>"
    return f"{v[0]}.{v[1]}"


def tup(v):
    return None if v is None else tuple(v) if isinstance(v, (list, tuple)) else v


def read_states():
    """Every harvested state, both populations, in order."""
    meta = json.load(open(os.path.join(HERE, "commits.json")))
    states = []
    for c in meta["commits"]:
        if c["blob_oid"] is None:
            states.append({"population": "P-B", "key": f"c{c['ordinal']:03d}",
                           "commit": c["sha"], "date": c["author_date"][:10],
                           "subject": c["subject"], "author": c["author"],
                           "deleted": True, "features": {}})
            continue
        path = os.path.join(BLOBS, f"{c['ordinal']:03d}-{c['blob_oid'][:12]}.py")
        src = open(path, encoding="utf-8", errors="replace").read()
        states.append({"population": "P-B", "key": f"c{c['ordinal']:03d}",
                       "commit": c["sha"], "date": c["author_date"][:10],
                       "subject": c["subject"], "author": c["author"],
                       "blob_oid": c["blob_oid"], "deleted": False,
                       "features": extract(src)})
    rels = []
    for r in meta["releases"]:
        if not r.get("blob_oid"):
            rels.append({"population": "P-A", "key": r["series"], "tag": r["tag"],
                         "missing": True, "features": {}})
            continue
        path = os.path.join(BLOBS, f"rel-{r['series']}-{r['blob_oid'][:12]}.py")
        src = open(path, encoding="utf-8", errors="replace").read()
        rels.append({"population": "P-A", "key": r["series"], "tag": r["tag"],
                     "ref_kind": r.get("ref_kind"), "ref_date": r.get("tag_date", "")[:10],
                     "ref_subject": r.get("tag_subject"), "blob_oid": r["blob_oid"],
                     "missing": False, "features": extract(src)})
    return states, rels


def runs(seq):
    """Collapse consecutive equal values into runs, keeping the first key of each."""
    out = []
    for key, val in seq:
        if out and out[-1]["value"] == val:
            out[-1]["until"] = key
            continue
        out.append({"value": val, "since": key, "until": key})
    return out


def main():
    commits, releases = read_states()

    unparsed = [
        (s["key"], name)
        for s in commits + releases
        for name, f in s["features"].items()
        if any(isinstance(f[k], str) and f[k].startswith("<") for k in
               ("optional", "mandatory"))
    ]

    names_B, names_A = set(), set()
    for s in commits:
        names_B |= set(s["features"])
    for s in releases:
        names_A |= set(s["features"])

    per_feature = {}
    for name in sorted(names_B | names_A, key=lambda n: min(
            [i for i, s in enumerate(commits) if n in s["features"]] or [99])):
        rec = {}
        for field in ("optional", "mandatory"):
            seqB = [(s["key"], tup(s["features"][name][field]))
                    for s in commits if name in s["features"]]
            seqA = [(s["key"], tup(s["features"][name][field]))
                    for s in releases if name in s["features"]]
            valsB = [r["value"] for r in runs(seqB)]
            valsA = [r["value"] for r in runs(seqA)]
            rec[field] = {
                "commit_runs": runs(seqB),
                "release_runs": runs(seqA),
                "commit_distinct_tuples": sorted(
                    {json.dumps(v) for v in valsB}),
                "release_distinct_tuples": sorted(
                    {json.dumps(v) for v in valsA}),
                "commit_distinct_minor": sorted(
                    {str(minor(v)) for v in valsB}),
                "release_distinct_minor": sorted(
                    {str(minor(v)) for v in valsA}),
            }
            # The night's question, per field.
            rec[field]["tuples_never_released"] = sorted(
                set(rec[field]["commit_distinct_tuples"])
                - set(rec[field]["release_distinct_tuples"]))
            rec[field]["minors_never_released"] = sorted(
                set(rec[field]["commit_distinct_minor"])
                - set(rec[field]["release_distinct_minor"]))
            rec[field]["moves_commit_tuple"] = max(0, len(valsB) - 1)
            rec[field]["moves_release_tuple"] = max(0, len(valsA) - 1)
            rec[field]["moves_commit_minor"] = max(
                0, len(runs([(k, minor(v)) for k, v in seqB])) - 1)
            rec[field]["moves_release_minor"] = max(
                0, len(runs([(k, minor(v)) for k, v in seqA])) - 1)
        rec["in_commits"] = name in names_B
        rec["in_releases"] = name in names_A
        per_feature[name] = rec

    # --- the four predictions, scored mechanically where they can be ---
    p1_hits = [
        {"feature": n, "field": f, "values": per_feature[n][f]["tuples_never_released"]}
        for n in per_feature for f in ("optional", "mandatory")
        if per_feature[n][f]["tuples_never_released"]
    ]
    p1_hits_minor = [
        {"feature": n, "field": f, "values": per_feature[n][f]["minors_never_released"]}
        for n in per_feature for f in ("optional", "mandatory")
        if per_feature[n][f]["minors_never_released"]
    ]
    p3_extra_features = sorted(names_B - names_A)

    # --- the audit of S62's own committed numbers, against S62's own grid re-derived ---
    s62 = json.load(open(S62))
    audit = {}
    for name, v in s62["per_feature"].items():
        mine = per_feature.get(name)
        audit[name] = {
            "s62_optional_values": v["optional_values"],
            "mine_release_optional_minor": mine["optional"]["release_distinct_minor"],
            "s62_optional_changed": v["optional_changed"],
            "mine_release_optional_moves_minor": mine["optional"]["moves_release_minor"],
            "mine_release_optional_moves_tuple": mine["optional"]["moves_release_tuple"],
            "s62_mandatory_values": [m["value"] for m in v["mandatory_runs"]],
            "mine_release_mandatory_minor": mine["mandatory"]["release_distinct_minor"],
            "s62_mandatory_changed": v["mandatory_changed"],
            "mine_release_mandatory_moves_minor": mine["mandatory"]["moves_release_minor"],
            "mine_release_mandatory_moves_tuple": mine["mandatory"]["moves_release_tuple"],
        }
        audit[name]["agrees_on_minor_moves"] = (
            v["optional_changed"] == mine["optional"]["moves_release_minor"]
            and v["mandatory_changed"] == mine["mandatory"]["moves_release_minor"])

    # The 2x2 the whole night turns on: two grids (release, commit) crossed with two
    # precisions (the release a tuple names, the tuple itself). Counted in features, not
    # in transitions: "the field moved in N of the ten features".
    grid = {}
    for g in ("release", "commit"):
        for prec in ("minor", "tuple"):
            for field in ("optional", "mandatory"):
                grid[f"{g}_grid.{prec}_precision.{field}"] = sum(
                    1 for n in per_feature
                    if per_feature[n][field][f"moves_{g}_{prec}"] > 0)

    out = {
        "night": "2026-08-24",
        "session": 69,
        "what_this_measures": (
            "The two boundary fields of every __future__ feature, read at every commit that "
            "has ever touched Lib/__future__.py on any ref (population P-B, 40 states), and "
            "at Session 62's own 22-release grid re-derived from the same clone (population "
            "P-A). The night's question is whether any value exists in P-B that is absent "
            "from P-A: a state of the norm that no release ever carried."
        ),
        "populations": {
            "P-B_commit_states": len(commits),
            "P-A_release_states": sum(1 for r in releases if not r["missing"]),
            "features_seen_at_commit_level": sorted(names_B),
            "features_seen_at_release_level": sorted(names_A),
        },
        "features_in_which_the_field_moved": grid,
        "unparsed_fields": unparsed,
        "P1_tuple_values_never_released": p1_hits,
        "P1_minor_values_never_released": p1_hits_minor,
        "P3_features_never_released": p3_extra_features,
        "per_feature": per_feature,
        "audit_of_session_62": audit,
        "release_refs": [
            {"series": r["key"], "tag": r.get("tag"), "ref_kind": r.get("ref_kind"),
             "ref_date": r.get("ref_date"), "ref_subject": r.get("ref_subject")}
            for r in releases
        ],
        "commit_states": [
            {"key": s["key"], "date": s["date"], "author": s["author"],
             "subject": s["subject"], "commit": s["commit"],
             "features": sorted(s["features"])}
            for s in commits
        ],
    }
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=1)

    for k in sorted(grid):
        print(f"  {k:<44} {grid[k]}")
    print(f"P-B {len(commits)} commit states, P-A "
          f"{out['populations']['P-A_release_states']} release states")
    print(f"unparsed fields: {len(unparsed)}")
    print(f"P1 (tuple values no release carried): {len(p1_hits)} "
          f"-> {[(h['feature'], h['field']) for h in p1_hits]}")
    print(f"P1 (reduced to major.minor):          {len(p1_hits_minor)} "
          f"-> {[(h['feature'], h['field']) for h in p1_hits_minor]}")
    print(f"P3 (features no release carried):     {p3_extra_features}")
    dis = [n for n, a in audit.items() if not a["agrees_on_minor_moves"]]
    print(f"audit of S62 move counts, disagreements: {dis}")


if __name__ == "__main__":
    main()
