#!/usr/bin/env python3
"""measure.py — Session 71, 2026-08-26.

Offline. Standard library only. Reads what harvest.py wrote and this practice's
own committed state grid from works/2026-08-25-under-the-commit/grids.json, and
computes the two norms' extensions over one field's review history.

It fetches nothing. Every number in tonight's work comes out of here.

The two norms, as PREDICTIONS.md §2 fixed them:

  M  the rules src/internal/godebugs/godebugs_test.go states AT THAT PATCH SET,
     restricted to those evaluable from table.go alone. A rule counts as stated
     if and only if the exact error-message literal the test uses for it is
     present in the test file at that patch set — so the transcription is
     anchored to the project's own words, not to my reading of them.

  H  an inline comment on path src/internal/godebugs/table.go, from Gerrit's own
     comment record.

Usage:
    python3 measure.py --raw .raw
"""

import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GRIDS = os.path.join(REPO, "works", "2026-08-25-under-the-commit", "grids.json")
PATH_TABLE = "src/internal/godebugs/table.go"

# ---------------------------------------------------------------------------
# M — the rules, each anchored to the literal the test itself prints.
# Only rules evaluable from table.go alone. The two the test also states —
# presence in doc/godebug.md, and a matching IncNonDefault call somewhere in the
# tree — are NOT transcribed and are declared as M's lower-bound in the work.
# ---------------------------------------------------------------------------

RULES = [
    {
        "id": "R1-sorted",
        "literal": 'All not sorted: %s then %s',
        "says": "All is sorted strictly increasing by Name",
        "table": "All",
    },
    {
        "id": "R2-package",
        "literal": 'Name=%s missing Package',
        "says": "every entry has a non-empty Package",
        "table": "All",
    },
    {
        "id": "R3-changed-needs-old",
        "literal": 'Name=%s has Changed, missing Old',
        "says": "Changed != 0 implies Old != \"\"",
        "table": "All",
    },
    {
        "id": "R4-old-needs-changed",
        "literal": 'Name=%s has Old, missing Changed',
        "says": "Old != \"\" implies Changed != 0",
        "table": "All",
    },
    {
        "id": "R5-removed-not-in-all",
        "literal": 'GODEBUG: %v exists in both Removed and All',
        "says": "no Name appears in both Removed and All",
        "table": "Removed",
    },
    {
        "id": "R6-removed-needs-old",
        "literal": 'GODEBUG: %v is missing Old predicate',
        "says": "every Removed entry has an Old predicate",
        "table": "Removed",
    },
]

# ---------------------------------------------------------------------------
# P4's matcher, fixed in PREDICTIONS.md §4 and not adjustable here.
# ---------------------------------------------------------------------------

CITE_WORDS = ["test", "tests", "doc", "docs", "documentation", "policy", "rule",
              "rules", "convention", "conventions", "spec", "guideline",
              "guidelines", "standard", "proposal", "readme"]
CITE_WORD_RE = re.compile(
    r"(?:^|[^a-z0-9.])(" + "|".join(CITE_WORDS) + r")(?:[^a-z0-9.]|$)")


def cites(message):
    m = (message or "").lower()
    if "http" in m:
        return True, ["http"]
    hits = sorted(set(CITE_WORD_RE.findall(m)))
    if "godebug.md" in m:
        hits = sorted(set(hits + ["godebug.md"]))
    return bool(hits), hits


# ---------------------------------------------------------------------------
# Parsing table.go
# ---------------------------------------------------------------------------

VAR_RE = {
    "All": re.compile(r"\bAll\s*=\s*\[\]\*?Info\s*\{"),
    "Removed": re.compile(r"\bRemoved\s*=\s*\[\]\s*\w*\s*\{"),
}

FIELD_STR = re.compile(r'(\w+)\s*:\s*"((?:[^"\\]|\\.)*)"')
FIELD_INT = re.compile(r'(\w+)\s*:\s*(-?\d+)\b')
FIELD_BOOL = re.compile(r'(\w+)\s*:\s*(true|false)\b')
FIELD_OTHER = re.compile(r'(\w+)\s*:\s*([A-Za-z_][\w.]*)')


def _block(text, start):
    """Return the text between the brace at `start` and its match, or None."""
    depth, i, n = 0, start, len(text)
    instr = inchr = incom = inline = False
    esc = False
    while i < n:
        c = text[i]
        if inline:
            if c == "\n":
                inline = False
        elif incom:
            if c == "*" and i + 1 < n and text[i + 1] == "/":
                incom = False
                i += 1
        elif instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        elif inchr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == "'":
                inchr = False
        else:
            if c == "/" and i + 1 < n and text[i + 1] == "/":
                inline = True
                i += 1
            elif c == "/" and i + 1 < n and text[i + 1] == "*":
                incom = True
                i += 1
            elif c == '"':
                instr = True
            elif c == "'":
                inchr = True
            elif c == "`":
                j = text.find("`", i + 1)
                i = j if j != -1 else n
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return text[start + 1:i]
        i += 1
    return None


def _entries(block):
    """Split a []Info{...} block into its top-level {...} entries."""
    out, depth, start = [], 0, None
    instr = esc = inline = False
    i, n = 0, len(block)
    while i < n:
        c = block[i]
        if inline:
            if c == "\n":
                inline = False
        elif instr:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                instr = False
        else:
            if c == "/" and i + 1 < n and block[i + 1] == "/":
                inline = True
                i += 1
            elif c == '"':
                instr = True
            elif c == "{":
                if depth == 0:
                    start = i
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0 and start is not None:
                    out.append(block[start + 1:i])
                    start = None
        i += 1
    return out


def parse_table(text):
    """Parse table.go -> {'All': [...], 'Removed': [...], 'ok': bool, 'why': str}."""
    res = {"All": [], "Removed": [], "ok": True, "why": ""}
    for name, rx in VAR_RE.items():
        m = rx.search(text)
        if not m:
            if name == "All":
                res["ok"] = False
                res["why"] = "no All = []Info{ literal"
            continue
        blk = _block(text, m.end() - 1)
        if blk is None:
            res["ok"] = False
            res["why"] = f"unbalanced braces in {name}"
            continue
        for e in _entries(blk):
            info = {}
            for k, v in FIELD_STR.findall(e):
                info[k] = v
            for k, v in FIELD_INT.findall(e):
                info.setdefault(k, int(v))
            for k, v in FIELD_BOOL.findall(e):
                info.setdefault(k, v == "true")
            for k, v in FIELD_OTHER.findall(e):
                info.setdefault(k, v)
            if "Name" in info:
                res[name].append(info)
    return res


# ---------------------------------------------------------------------------
# M applied
# ---------------------------------------------------------------------------

def rules_stated(test_text):
    return {r["id"] for r in RULES if r["literal"] in test_text}


def apply_M(parsed, stated):
    """Return list of violations: [{'rule':id,'name':...,'detail':...}]."""
    v = []
    allrows = parsed["All"]
    if "R1-sorted" in stated:
        last = ""
        for info in allrows:
            nm = info.get("Name", "")
            if nm <= last:
                v.append({"rule": "R1-sorted", "name": nm,
                          "detail": f"{last} then {nm}"})
            last = nm
    if "R2-package" in stated:
        for info in allrows:
            if not info.get("Package", ""):
                v.append({"rule": "R2-package", "name": info.get("Name", ""),
                          "detail": "Package empty or absent"})
    if "R3-changed-needs-old" in stated:
        for info in allrows:
            ch = info.get("Changed", 0)
            if isinstance(ch, int) and ch != 0 and not info.get("Old", ""):
                v.append({"rule": "R3-changed-needs-old",
                          "name": info.get("Name", ""),
                          "detail": f"Changed={ch}, no Old"})
    if "R4-old-needs-changed" in stated:
        for info in allrows:
            old = info.get("Old", "")
            ch = info.get("Changed", 0)
            if old and (not isinstance(ch, int) or ch == 0):
                v.append({"rule": "R4-old-needs-changed",
                          "name": info.get("Name", ""),
                          "detail": f'Old="{old}", no Changed'})
    if "R5-removed-not-in-all" in stated:
        names = {i.get("Name") for i in allrows}
        for info in parsed["Removed"]:
            if info.get("Name") in names:
                v.append({"rule": "R5-removed-not-in-all",
                          "name": info.get("Name", ""),
                          "detail": "in Removed and All"})
    if "R6-removed-needs-old" in stated:
        for info in parsed["Removed"]:
            if "Old" not in info:
                v.append({"rule": "R6-removed-needs-old",
                          "name": info.get("Name", ""),
                          "detail": "Removed entry without Old"})
    return v


# ---------------------------------------------------------------------------
# Verdicts
# ---------------------------------------------------------------------------

VERDICT_RE = re.compile(
    r"^Patch Set (\d+):\s*(?:LUCI-)?TryBot-Result([+-]\d+)\s*$", re.M)


def verdicts_of(detail):
    """{ps: {'plus': n, 'minus': n, 'seq': [...]}} from the change's messages."""
    out = {}
    for m in detail.get("messages", []):
        for ps, vote in VERDICT_RE.findall(m.get("message", "")):
            d = out.setdefault(int(ps), {"plus": 0, "minus": 0, "seq": []})
            if vote.startswith("+"):
                d["plus"] += 1
            else:
                d["minus"] += 1
            d["seq"].append(vote)
    return out


def verdict_class(d, strict):
    """'green' | 'red' | 'mixed' | 'none'. strict: mixed counts as not-green."""
    if d is None:
        return "none"
    if d["plus"] and d["minus"]:
        return "mixed"
    if d["plus"]:
        return "green"
    if d["minus"]:
        return "red"
    return "none"


def is_green(d, strict):
    c = verdict_class(d, strict)
    if c == "green":
        return True
    if c == "mixed":
        return not strict          # loose reading: "a recorded +1"
    return False


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(HERE, ".raw"))
    args = ap.parse_args()
    raw = os.path.abspath(args.raw)

    grids = json.load(open(GRIDS))
    harvest = json.load(open(os.path.join(HERE, "harvest.json")))
    blobs = grids["blobs"]
    states = [p for p in grids["points"] if p["grid"] == "patchset"]

    print("measure -- two norms over one field\n")

    # --- test file per state --------------------------------------------
    test_sha = {(t["change"], t["ps"]): t["sha256"]
                for t in harvest["test_file"]["per_state"]}
    test_text = {}
    for sha in {v for v in test_sha.values() if v}:
        with open(os.path.join(raw, "test", sha + ".go"), "rb") as f:
            test_text[sha] = f.read().decode("utf-8", "replace")
    stated_by_sha = {sha: rules_stated(txt) for sha, txt in test_text.items()}
    print(f"  {len(test_text)} distinct test files; rule sets:")
    for sha, st in sorted(stated_by_sha.items(), key=lambda kv: -len(kv[1])):
        print(f"    {sha[:12]}  {len(st)}  {' '.join(sorted(st))}")

    # --- parse every state ----------------------------------------------
    parsed_by_blob, parse_fail = {}, []
    for b, txt in blobs.items():
        p = parse_table(txt)
        parsed_by_blob[b] = p
        if not p["ok"]:
            parse_fail.append({"blob": b, "why": p["why"]})
    print(f"\n  parsed {len(parsed_by_blob)} distinct states, "
          f"{len(parse_fail)} failures")

    # --- verdicts --------------------------------------------------------
    verd = {}
    for n in sorted({p["change"] for p in states}):
        fn = os.path.join(raw, "detail", f"{n}.json")
        if not os.path.exists(fn):
            continue
        verd[n] = verdicts_of(json.load(open(fn)))

    # --- comments on table.go -------------------------------------------
    comments = {}          # change -> [comment dicts]
    other_paths = 0
    for n in sorted({p["change"] for p in states}):
        fn = os.path.join(raw, "comments", f"{n}.json")
        if not os.path.exists(fn):
            continue
        d = json.load(open(fn))
        rows = []
        for path, cs in d.items():
            if path != PATH_TABLE:
                other_paths += len(cs)
                continue
            for c in cs:
                msg = c.get("message", "")
                ok, hits = cites(msg)
                rows.append({
                    "change": n,
                    "ps": c.get("patch_set"),
                    "author": (c.get("author") or {}).get("_account_id"),
                    "id": c.get("id"),
                    "in_reply_to": c.get("in_reply_to"),
                    "updated": c.get("updated"),
                    "line": c.get("line"),
                    "chars": len(msg),
                    "sha256": hashlib.sha256(msg.encode()).hexdigest(),
                    "cites": ok,
                    "cite_hits": hits,
                    "is_suggestion": "```suggestion" in msg,
                    "_msg": msg,
                })
        if rows:
            comments[n] = sorted(rows, key=lambda r: (r["ps"] or 0,
                                                      r["updated"] or ""))
    n_com = sum(len(v) for v in comments.values())
    print(f"  inline comments on {PATH_TABLE}: {n_com} across "
          f"{len(comments)} changes ({other_paths} on other paths, unused)")

    # --- states, corrections --------------------------------------------
    by_change = {}
    for p in states:
        by_change.setdefault(p["change"], {})[p["patchset"]] = p

    uploader = {}          # (change, ps) -> account id
    for n, pss in by_change.items():
        for ps, p in pss.items():
            uploader[(n, ps)] = p.get("uploader")
    # grids.json points carry no uploader; take it from the detail record
    for n in by_change:
        fn = os.path.join(raw, "detail", f"{n}.json")
        if not os.path.exists(fn):
            continue
        d = json.load(open(fn))
        for rev, r in (d.get("revisions") or {}).items():
            ps = r.get("_number")
            up = (r.get("uploader") or r.get("real_uploader") or {})
            uploader[(n, ps)] = up.get("_account_id")

    corrections, gapped = [], 0
    for n, pss in sorted(by_change.items()):
        for ps in sorted(pss):
            if ps + 1 not in pss:
                if ps + 1 in {p for p in pss} or True:
                    pass
                continue
            a, b = pss[ps], pss[ps + 1]
            if a["blob"] != b["blob"]:
                corrections.append({
                    "change": n, "from_ps": ps, "to_ps": ps + 1,
                    "from_blob": a["blob"], "to_blob": b["blob"],
                    "to_kind": b.get("kind"),
                    "to_created": b.get("created"),
                    "uploader_to": uploader.get((n, ps + 1)),
                })
        allps = sorted(pss)
        gapped += sum(1 for i in range(len(allps) - 1)
                      if allps[i + 1] != allps[i] + 1)
    print(f"  corrections (consecutive patch sets whose table.go bytes differ): "
          f"{len(corrections)} in {len({c['change'] for c in corrections})} changes")
    print(f"  non-consecutive patch-set gaps skipped: {gapped}")

    # --- M over every state ---------------------------------------------
    m_rows = []
    for p in states:
        key = (p["change"], p["patchset"])
        sha = test_sha.get(key)
        if not sha:
            m_rows.append({"change": p["change"], "ps": p["patchset"],
                           "in_domain": False, "reason": "no test file"})
            continue
        st = stated_by_sha[sha]
        viol = apply_M(parsed_by_blob[p["blob"]], st)
        m_rows.append({"change": p["change"], "ps": p["patchset"],
                       "in_domain": True, "test_sha": sha,
                       "rules": sorted(st), "violations": viol,
                       "rejects": bool(viol), "blob": p["blob"]})
    in_dom = [r for r in m_rows if r["in_domain"]]
    rejected = [r for r in in_dom if r["rejects"]]
    print(f"\n  M's domain: {len(in_dom)}/{len(states)} states · "
          f"M rejects {len(rejected)}")

    # --- P3: does M contradict the record? ------------------------------
    def vd(n, ps):
        return (verd.get(n) or {}).get(ps)

    p3 = {}
    for strict in (True, False):
        greens = [r for r in in_dom if is_green(vd(r["change"], r["ps"]), strict)]
        bad = [r for r in greens if r["rejects"]]
        p3["strict" if strict else "loose"] = {
            "green_states": len(greens),
            "rejected_by_M": len(bad),
            "rows": [{"change": r["change"], "ps": r["ps"],
                      "violations": r["violations"]} for r in bad],
        }
    print(f"  P3  green states {p3['loose']['green_states']} (loose) / "
          f"{p3['strict']['green_states']} (strict) · "
          f"M rejects {p3['loose']['rejected_by_M']} / "
          f"{p3['strict']['rejected_by_M']}")

    # --- P1: only-H ------------------------------------------------------
    def comments_upto(n, ps):
        return [c for c in comments.get(n, []) if (c["ps"] or 0) <= ps]

    p1 = {}
    for strict in (True, False):
        rows = []
        for c in corrections:
            if not is_green(vd(c["change"], c["from_ps"]), strict):
                continue
            up = c["uploader_to"]
            cs = [x for x in comments_upto(c["change"], c["from_ps"])
                  if x["author"] != up]
            if cs:
                rows.append({**c, "n_comments": len(cs),
                             "comment_ids": [x["id"] for x in cs],
                             "authors": sorted({x["author"] for x in cs})})
        p1["strict" if strict else "loose"] = {
            "corrections": len(rows),
            "distinct_changes": sorted({r["change"] for r in rows}),
            "rows": rows,
        }
    print(f"  P1  only-H corrections {p1['loose']['corrections']} (loose) / "
          f"{p1['strict']['corrections']} (strict) · distinct changes "
          f"{len(p1['loose']['distinct_changes'])} / "
          f"{len(p1['strict']['distinct_changes'])}")

    # --- P2: only-M ------------------------------------------------------
    only_m = []
    for r in rejected:
        cs = [c for c in comments.get(r["change"], []) if c["ps"] == r["ps"]]
        if not cs:
            only_m.append({"change": r["change"], "ps": r["ps"],
                           "violations": r["violations"],
                           "verdict": verdict_class(vd(r["change"], r["ps"]), True)})
    print(f"  P2  states M rejects with no comment on the file at that patch set: "
          f"{len(only_m)}")

    # --- P4: do the demanding comments cite anything? --------------------
    corr_index = {(c["change"], c["from_ps"]): c for c in corrections}
    demanding = []
    for n, rows in comments.items():
        for c in rows:
            key = (n, c["ps"])
            if key in corr_index:
                demanding.append({**c, "uploader_next":
                                  corr_index[key]["uploader_to"]})
    def share(rows):
        if not rows:
            return None
        return sum(1 for r in rows if r["cites"]) / len(rows)

    d_all = demanding
    d_nonup = [r for r in demanding if r["author"] != r["uploader_next"]]
    d_nonup_top = [r for r in d_nonup if not r["in_reply_to"]]
    p4 = {
        "as_written": {"n": len(d_all), "citing": sum(1 for r in d_all if r["cites"]),
                       "share": share(d_all)},
        "non_uploader": {"n": len(d_nonup),
                         "citing": sum(1 for r in d_nonup if r["cites"]),
                         "share": share(d_nonup)},
        "non_uploader_top_level": {
            "n": len(d_nonup_top),
            "citing": sum(1 for r in d_nonup_top if r["cites"]),
            "share": share(d_nonup_top)},
    }
    for k, v in p4.items():
        s = "n/a" if v["share"] is None else f"{v['share']:.3f}"
        print(f"  P4  {k:24s} {v['citing']}/{v['n']} cite  share={s}")

    # --- write ------------------------------------------------------------
    def strip(rows):
        return [{k: v for k, v in r.items() if k != "_msg"} for r in rows]

    out = {
        "measured_from": {"grids": os.path.relpath(GRIDS, REPO),
                          "harvest": "harvest.json"},
        "rules": RULES,
        "test_files": {sha: {"rules": sorted(st), "bytes": len(test_text[sha])}
                       for sha, st in stated_by_sha.items()},
        "parse_failures": parse_fail,
        "counts": {
            "states": len(states),
            "distinct_blobs": len(blobs),
            "changes": len(by_change),
            "corrections": len(corrections),
            "correction_changes": len({c["change"] for c in corrections}),
            "patchset_gaps_skipped": gapped,
            "comments_on_table_go": n_com,
            "comments_on_other_paths": other_paths,
            "changes_with_comments_on_table_go": len(comments),
            "M_domain": len(in_dom),
            "M_rejects": len(rejected),
        },
        "verdict_histogram": {},
        "P1_only_H": p1,
        "P2_only_M": only_m,
        "P3_validation": p3,
        "P4_citation": p4,
        "M_rejections": [{"change": r["change"], "ps": r["ps"],
                          "violations": r["violations"],
                          "verdict": verdict_class(vd(r["change"], r["ps"]), True)}
                         for r in rejected],
        "corrections": corrections,
        "comments": {str(n): strip(v) for n, v in comments.items()},
        "demanding_comment_ids": {
            "as_written": [r["id"] for r in d_all],
            "non_uploader": [r["id"] for r in d_nonup],
            "non_uploader_top_level": [r["id"] for r in d_nonup_top],
        },
    }
    hist = {}
    for p in states:
        c = verdict_class(vd(p["change"], p["patchset"]), True)
        hist[c] = hist.get(c, 0) + 1
    out["verdict_histogram"] = hist
    print("\n  verdict histogram over states:", hist)

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("\n  wrote results.json")


if __name__ == "__main__":
    main()
