#!/usr/bin/env python3
"""analyse.py — Session 71, 2026-08-26.

POST-HOC. Written AFTER measure.py had run and after the four predictions in
PREDICTIONS.md were scored. Nothing here is a prediction and nothing here is
scored; it exists to say *what* the two norms were disagreeing about, once the
counting had already established *that* they do.

It is offline and reads results.json, the inherited state grid, and the
uncommitted raw comment cache. It computes:

  - the field-level diff of the All table across every correction in the
    only-H cell (which entry, which field, from what to what);
  - how long each superseded state stood, from the comment that refused it to
    the patch set that replaced it;
  - the same for the only-M cell and for the one state both norms refused.

Usage:
    python3 analyse.py --raw .raw
"""

import argparse
import datetime as dt
import json
import os

from measure import parse_table

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GRIDS = os.path.join(REPO, "works", "2026-08-25-under-the-commit", "grids.json")
PATH_TABLE = "src/internal/godebugs/table.go"

FIELDS = ["Package", "Changed", "Old", "Opaque", "Immutable", "Undocumented"]


def ts(s):
    if not s:
        return None
    return dt.datetime.strptime(s.split(".")[0], "%Y-%m-%d %H:%M:%S")


def dur(a, b):
    if not a or not b:
        return None
    d = b - a
    s = int(d.total_seconds())
    sign = "-" if s < 0 else ""
    s = abs(s)
    days, rem = divmod(s, 86400)
    h, rem = divmod(rem, 3600)
    m, sec = divmod(rem, 60)
    parts = []
    if days:
        parts.append(f"{days} d")
    if h or days:
        parts.append(f"{h} h")
    parts.append(f"{m} m")
    parts.append(f"{sec} s")
    return sign + " ".join(parts)


def line_at(blobs, states, change, ps, line):
    """The text of `line` in table.go as it stood at (change, ps)."""
    if not line:
        return None
    p = states.get((change, ps))
    if not p:
        return None
    txt = blobs.get(p["blob"])
    if txt is None:
        return None
    rows = txt.split("\n")
    if 1 <= line <= len(rows):
        return rows[line - 1].strip()
    return None


def table_diff(a, b):
    """Field-level diff between two parsed All tables, keyed by Name."""
    A = {i.get("Name"): i for i in a["All"]}
    B = {i.get("Name"): i for i in b["All"]}
    out = {"added": sorted(set(B) - set(A)), "removed": sorted(set(A) - set(B)),
           "changed": []}
    for n in sorted(set(A) & set(B)):
        deltas = {}
        for f in FIELDS:
            x, y = A[n].get(f), B[n].get(f)
            if x != y:
                deltas[f] = [x, y]
        if deltas:
            out["changed"].append({"name": n, "fields": deltas})
    ra = {i.get("Name") for i in a["Removed"]}
    rb = {i.get("Name") for i in b["Removed"]}
    if ra or rb:
        out["removed_table_added"] = sorted(rb - ra)
        out["removed_table_dropped"] = sorted(ra - rb)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(HERE, ".raw"))
    args = ap.parse_args()
    raw = os.path.abspath(args.raw)

    grids = json.load(open(GRIDS))
    res = json.load(open(os.path.join(HERE, "results.json")))
    blobs = grids["blobs"]
    states = {(p["change"], p["patchset"]): p
              for p in grids["points"] if p["grid"] == "patchset"}
    parsed = {b: parse_table(t) for b, t in blobs.items()}

    def comments_raw(n):
        fn = os.path.join(raw, "comments", f"{n}.json")
        if not os.path.exists(fn):
            return []
        return json.load(open(fn)).get(PATH_TABLE, [])

    print("analyse -- what the two norms were disagreeing about (post-hoc)\n")

    out = {"note": "POST-HOC. Written after measure.py ran and after the four "
                   "predictions were scored. Nothing here is scored.",
           "only_H": [], "only_M": [], "both": []}

    # ---- only-H --------------------------------------------------------
    for row in res["P1_only_H"]["loose"]["rows"]:
        n, a, b = row["change"], row["from_ps"], row["to_ps"]
        pa, pb = states[(n, a)], states[(n, b)]
        d = table_diff(parsed[pa["blob"]], parsed[pb["blob"]])
        cs = [c for c in comments_raw(n)
              if (c.get("patch_set") or 0) <= a
              and (c.get("author") or {}).get("_account_id") != row["uploader_to"]]
        cs.sort(key=lambda c: c.get("updated") or "")
        first = cs[0] if cs else None
        rec = {
            "change": n, "from_ps": a, "to_ps": b,
            "url": f"https://go-review.googlesource.com/c/go/+/{n}/{a}..{b}/"
                   + PATH_TABLE,
            "from_created": pa.get("created"), "to_created": pb.get("created"),
            "state_stood": dur(ts(pa.get("created")), ts(pb.get("created"))),
            "diff": d,
            "first_refusing_comment": None if not first else {
                "author": (first.get("author") or {}).get("_account_id"),
                "patch_set": first.get("patch_set"),
                "line": first.get("line"),
                "updated": first.get("updated"),
                "chars": len(first.get("message", "")),
                "is_suggestion": "```suggestion" in first.get("message", ""),
                "from_comment_to_next_patchset":
                    dur(ts(first.get("updated")), ts(pb.get("created"))),
                # Attribution check: a comment carries a line number into the
                # patch set it was left on. Reading that line out of the state
                # itself is what turns "a comment existed" into "a comment was
                # about this entry" — without it the only-H cell would be a
                # coincidence of timing.
                "anchored_line_text": line_at(
                    blobs, states, n, first.get("patch_set"),
                    first.get("line")),
            },
        }
        # Attribution, stricter than the prediction and computed after it:
        # a correction counts as ATTRIBUTED only if some non-uploader comment
        # anchors a line that names an entry the correction actually touched.
        # P1 as written asked only that a comment precede the correction. This
        # is the harder reading and it is reported beside the scored one.
        touched = ({c["name"] for c in d["changed"]}
                   | set(d["added"]) | set(d["removed"])
                   | set(d.get("removed_table_added", []))
                   | set(d.get("removed_table_dropped", [])))
        anchors = []
        for c in cs:
            txt = line_at(blobs, states, n, c.get("patch_set"), c.get("line"))
            hit = sorted(t for t in touched if txt and f'"{t}"' in txt)
            anchors.append({"comment": c.get("id"), "ps": c.get("patch_set"),
                            "line": c.get("line"), "line_text": txt,
                            "names_touched_on_that_line": hit})
        rec["anchors"] = anchors
        rec["attributed"] = any(a["names_touched_on_that_line"] for a in anchors)
        out["only_H"].append(rec)
        s = d["changed"][0] if d["changed"] else None
        print(f"  CL {n} ps{a}->{b}  stood {rec['state_stood']}")
        print(f"    +{d['added']} -{d['removed']} "
              f"changed={[c['name'] for c in d['changed']]}")
        if s:
            print(f"    {s['name']}: {s['fields']}")

    # ---- only-M and both ------------------------------------------------
    print()
    for row in res["M_rejections"]:
        n, ps = row["change"], row["ps"]
        cs = [c for c in comments_raw(n) if c.get("patch_set") == ps]
        cell = "only_M" if not cs else "both"
        nxt = states.get((n, ps + 1))
        p = states[(n, ps)]
        rec = {
            "change": n, "ps": ps, "verdict": row["verdict"],
            "violations": row["violations"],
            "url": f"https://go-review.googlesource.com/c/go/+/{n}/{ps}/"
                   + PATH_TABLE,
            "created": p.get("created"),
            "next_ps_created": nxt.get("created") if nxt else None,
            "state_stood": dur(ts(p.get("created")),
                               ts(nxt.get("created")) if nxt else None),
            "comments_at_this_ps": len(cs),
            "diff_to_next": (table_diff(parsed[p["blob"]], parsed[nxt["blob"]])
                             if nxt and nxt["blob"] != p["blob"] else None),
        }
        out[cell].append(rec)
        print(f"  {cell:7s} CL {n} ps{ps} verdict={row['verdict']} "
              f"stood {rec['state_stood']} · "
              f"{len(row['violations'])} violation(s)")
        for v in row["violations"]:
            print(f"      {v['rule']}  {v['name']}  {v['detail']}")

    # ---- the boundary values touched anywhere in the only-H cell --------
    bound = []
    for rec in out["only_H"]:
        for c in rec["diff"]["changed"]:
            if "Changed" in c["fields"]:
                bound.append({"change": rec["change"],
                              "ps": [rec["from_ps"], rec["to_ps"]],
                              "name": c["name"],
                              "from": c["fields"]["Changed"][0],
                              "to": c["fields"]["Changed"][1],
                              "stood": rec["state_stood"],
                              "url": rec["url"]})
    out["boundary_values_rewritten_in_only_H"] = bound
    att = [r for r in out["only_H"] if r["attributed"]]
    out["attribution"] = {
        "rule": "a non-uploader comment anchors a line, in the state it was left "
                "on, that names an entry the correction touched",
        "corrections_scored": len(out["only_H"]),
        "corrections_attributed": len(att),
        "changes_scored": sorted({r["change"] for r in out["only_H"]}),
        "changes_attributed": sorted({r["change"] for r in att}),
    }
    print(f"\n  attributed: {len(att)}/{len(out['only_H'])} corrections, "
          f"{len(out['attribution']['changes_attributed'])} distinct changes "
          f"{out['attribution']['changes_attributed']}")
    print("\n  boundary values (Changed) rewritten inside the only-H cell:")
    for b in bound:
        print(f"    CL {b['change']} ps{b['ps'][0]}->{b['ps'][1]}  "
              f"{b['name']}: Changed {b['from']} -> {b['to']}  "
              f"(stood {b['stood']})")

    with open(os.path.join(HERE, "findings.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("\n  wrote findings.json")


if __name__ == "__main__":
    main()
