#!/usr/bin/env python3
"""harvest.py — Session 71, 2026-08-26.

Fetches the *review* record of one file from Go's Gerrit: for every change that
touches src/internal/godebugs/table.go, the per-patch-set machine verdict, the
inline comments on that path, and the project's own test file as it stood at
that patch set.

It fetches; it does not measure. Every number this night reports comes out of
measure.py, which is offline and reads only what this script wrote.

Three rules it keeps, and they are not incidental:

  1. No third-party document is committed as bytes. Comment bodies are authored
     by identifiable people and carry no redistribution licence, so they are
     written to a raw cache OUTSIDE the committed tree (--raw, .gitignored) and
     the committed record carries metadata and hashes only. PROTOCOL.md,
     "Sources are committed only where the licence allows it".
  2. Every fetch is recorded in sources/MANIFEST.json with URL, status, bytes
     and SHA-256 — individually for the load-bearing few, in aggregate for the
     bulk classes, with the aggregate hash taken over the sorted per-URL digests
     so a stranger can reproduce the same aggregate.
  3. Nothing is retried into silence: a URL that never returns 200 is recorded
     with the status it did return and the run reports it.

Usage:
    python3 harvest.py --raw .raw
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GRIDS = os.path.join(REPO, "works", "2026-08-25-under-the-commit", "grids.json")
CHANGES_S70 = os.path.join(REPO, "works", "2026-08-25-under-the-commit", "changes.json")

GERRIT = "https://go-review.googlesource.com"
PATH_TABLE = "src/internal/godebugs/table.go"
PATH_TEST = "src/internal/godebugs/godebugs_test.go"

QUERIES = [
    "file:src/internal/godebugs/table.go",
    "file:doc/godebug.md",
    "file:src/internal/godebug/godebug.go",
]

UA = "error-as-method/session-71 (nightly research line; one file's review history)"

_manifest_lock = None
MANIFEST = []


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def fetch(url, tries=4):
    """GET url. Returns (status, body_bytes). Never raises on HTTP status."""
    last = None
    for i in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            body = b""
            try:
                body = e.read()
            except Exception:
                pass
            if e.code in (404, 403):        # a real answer, not a hiccup
                return e.code, body
            last = (e.code, body)
        except Exception as e:              # noqa: BLE001 - network, any shape
            last = (0, str(e).encode())
        time.sleep(1.5 * (2 ** i))
    return last if last else (0, b"")


def gerrit_json(url):
    """Gerrit prefixes JSON with )]}'\\n — strip it. Returns (status, obj, raw)."""
    st, raw = fetch(url)
    if st != 200:
        return st, None, raw
    txt = raw.decode("utf-8", "replace")
    i = txt.find("\n")
    if txt.startswith(")]}'") and i != -1:
        txt = txt[i + 1:]
    try:
        return st, json.loads(txt), raw
    except json.JSONDecodeError:
        return st, None, raw


def record(url, status, raw, what, committed=False):
    MANIFEST.append({
        "url": url,
        "http_status": status,
        "bytes": len(raw) if raw else 0,
        "sha256": hashlib.sha256(raw or b"").hexdigest(),
        "fetched": now(),
        "what": what,
        "committed": committed,
    })


# ---------------------------------------------------------------- populations

def query_changes():
    """Re-run S70's three file queries. Returns (numbers set, per-query counts)."""
    found = {}
    counts = {}
    for q in QUERIES:
        url = (GERRIT + "/changes/?q=" + urllib.parse.quote(q, safe=":")
               + "&n=500&o=ALL_REVISIONS")
        st, obj, raw = gerrit_json(url)
        record(url, st, raw, "Gerrit change search: " + q)
        if st != 200 or obj is None:
            print(f"  QUERY FAILED {st}: {q}", file=sys.stderr)
            counts[q] = None
            continue
        counts[q] = len(obj)
        for c in obj:
            n = int(c["_number"])
            e = found.setdefault(n, {
                "number": n,
                "project": c.get("project"),
                "branch": c.get("branch"),
                "status": c.get("status"),
                "subject": c.get("subject"),
                "queries": [],
            })
            e["queries"].append(q)
        print(f"  {len(obj):4d}  {q}")
    return found, counts


# ------------------------------------------------------------------ per change

VERDICT_RE = re.compile(
    r"^Patch Set (\d+):\s*(?:LUCI-)?TryBot-Result([+-]\d+)\s*$", re.M)


def change_detail(number):
    url = (GERRIT + f"/changes/go~{number}/detail"
           "?o=ALL_REVISIONS&o=MESSAGES&o=DETAILED_LABELS")
    st, obj, raw = gerrit_json(url)
    return url, st, obj, raw


def change_comments(number):
    url = GERRIT + f"/changes/go~{number}/comments"
    st, obj, raw = gerrit_json(url)
    return url, st, obj, raw


def content_at(number, rev, path):
    url = (GERRIT + f"/changes/go~{number}/revisions/{rev}/files/"
           + urllib.parse.quote(path, safe="") + "/content")
    st, raw = fetch(url)
    if st != 200:
        return url, st, None, raw
    try:
        return url, st, base64.b64decode(raw), raw
    except Exception:                        # noqa: BLE001
        return url, st, None, raw


# ----------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=os.path.join(HERE, ".raw"),
                    help="directory for uncommitted raw bodies")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    raw_dir = os.path.abspath(args.raw)
    for sub in ("detail", "comments", "test", "table"):
        os.makedirs(os.path.join(raw_dir, sub), exist_ok=True)

    print("harvest -- the review record of one file\n")

    # --- 0. the inherited state grid ------------------------------------
    grids = json.load(open(GRIDS))
    s70_changes = json.load(open(CHANGES_S70))
    states = [p for p in grids["points"] if p["grid"] == "patchset"]
    print(f"  inherited from S70: {len(s70_changes)} changes, "
          f"{len(states)} patch-set states, {len(grids['blobs'])} blobs")

    # --- 1. re-verify the change population ------------------------------
    print("\n  re-running the three file queries ...")
    fresh, qcounts = query_changes()
    inherited = {int(k) for k in s70_changes}
    now_set = set(fresh)
    pop = {
        "inherited_count": len(inherited),
        "fresh_count": len(now_set),
        "per_query": qcounts,
        "only_in_inherited": sorted(inherited - now_set),
        "only_in_fresh": sorted(now_set - inherited),
    }
    print(f"  inherited {len(inherited)} · fresh {len(now_set)} · "
          f"new {len(now_set - inherited)} · gone {len(inherited - now_set)}")

    # The measured population is the inherited one: the states come from it.
    # A change that appeared since last night has no state grid here and is
    # reported, not silently added.
    numbers = sorted(inherited)

    # --- 2. detail + comments, per change --------------------------------
    print(f"\n  fetching detail + comments for {len(numbers)} changes ...")
    detail_stats, comment_stats = [], []

    def do_change(n):
        out = {"number": n}
        u1, s1, o1, r1 = change_detail(n)
        if s1 == 200 and o1 is not None:
            with open(os.path.join(raw_dir, "detail", f"{n}.json"), "w") as f:
                json.dump(o1, f)
        out["detail"] = (u1, s1, hashlib.sha256(r1 or b"").hexdigest(), len(r1 or b""))
        u2, s2, o2, r2 = change_comments(n)
        if s2 == 200 and o2 is not None:
            with open(os.path.join(raw_dir, "comments", f"{n}.json"), "w") as f:
                json.dump(o2, f)
        out["comments"] = (u2, s2, hashlib.sha256(r2 or b"").hexdigest(), len(r2 or b""))
        return out

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for i, out in enumerate(ex.map(do_change, numbers), 1):
            detail_stats.append(out["detail"])
            comment_stats.append(out["comments"])
            if i % 40 == 0:
                print(f"    {i}/{len(numbers)}")

    bad_d = [d for d in detail_stats if d[1] != 200]
    bad_c = [c for c in comment_stats if c[1] != 200]
    print(f"  detail: {len(detail_stats)} fetched, {len(bad_d)} not 200")
    print(f"  comments: {len(comment_stats)} fetched, {len(bad_c)} not 200")

    # --- 3. the test file at every state ---------------------------------
    # M is the rule set the project's own test states AT THAT PATCH SET, so the
    # test file is fetched per state rather than assumed constant.
    print(f"\n  fetching {PATH_TEST} at {len(states)} states ...")
    test_stats = []

    def do_test(p):
        n, rev = p["change"], p["rev"]
        u, st, body, raw = content_at(n, rev, PATH_TEST)
        if st == 200 and body is not None:
            h = hashlib.sha256(body).hexdigest()
            fn = os.path.join(raw_dir, "test", h + ".go")
            if not os.path.exists(fn):
                with open(fn, "wb") as f:
                    f.write(body)
            return {"change": n, "rev": rev, "ps": p["patchset"], "status": st,
                    "sha256": h, "bytes": len(body), "url": u,
                    "raw_sha256": hashlib.sha256(raw).hexdigest(),
                    "raw_bytes": len(raw)}
        return {"change": n, "rev": rev, "ps": p["patchset"], "status": st,
                "sha256": None, "bytes": 0, "url": u,
                "raw_sha256": hashlib.sha256(raw or b"").hexdigest(),
                "raw_bytes": len(raw or b"")}

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for i, out in enumerate(ex.map(do_test, states), 1):
            test_stats.append(out)
            if i % 100 == 0:
                print(f"    {i}/{len(states)}")

    have = sum(1 for t in test_stats if t["status"] == 200)
    miss = sum(1 for t in test_stats if t["status"] == 404)
    other = [t for t in test_stats if t["status"] not in (200, 404)]
    distinct_tests = len({t["sha256"] for t in test_stats if t["sha256"]})
    print(f"  test file present at {have} states, absent (404) at {miss}, "
          f"other status at {len(other)} · {distinct_tests} distinct test files")

    # --- 4. the cross-route verification sample --------------------------
    # Fixed in PREDICTIONS.md §6: every state with patch set 1 whose change
    # number ends in 7. Re-fetched from Gerrit's content endpoint — a different
    # route from S70's git-object fetch — and compared byte for byte.
    sample = [p for p in states if p["patchset"] == 1 and p["change"] % 10 == 7]
    print(f"\n  cross-route check on {len(sample)} states "
          f"(patch set 1, change number ends in 7) ...")
    checks = []

    def do_check(p):
        u, st, body, raw = content_at(p["change"], p["rev"], PATH_TABLE)
        inherited_txt = grids["blobs"].get(p["blob"])
        rec = {"change": p["change"], "ps": p["patchset"], "rev": p["rev"],
               "blob": p["blob"], "status": st, "url": u,
               "raw_sha256": hashlib.sha256(raw or b"").hexdigest(),
               "raw_bytes": len(raw or b"")}
        if st == 200 and body is not None and inherited_txt is not None:
            got = body
            want = inherited_txt.encode("utf-8")
            rec["match"] = (got == want)
            rec["sha256_fetched"] = hashlib.sha256(got).hexdigest()
            rec["sha256_inherited"] = hashlib.sha256(want).hexdigest()
            # git's own object id over the fetched bytes, as S70 computed it
            hdr = b"blob " + str(len(got)).encode() + b"\0"
            rec["oid_fetched"] = hashlib.sha1(hdr + got).hexdigest()
            rec["oid_matches_s70"] = (rec["oid_fetched"] == p["blob"])
        else:
            rec["match"] = None
        return rec

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        checks = list(ex.map(do_check, sample))

    ok = sum(1 for c in checks if c.get("match") is True)
    bad = [c for c in checks if c.get("match") is False]
    unk = [c for c in checks if c.get("match") is None]
    print(f"  matched {ok}/{len(checks)} · mismatched {len(bad)} · "
          f"unresolved {len(unk)}")

    # --- 5. aggregate manifest entries -----------------------------------
    def agg(name, rows, what):
        digs = sorted(r[2] if isinstance(r, tuple) else r for r in rows)
        blob = "\n".join(digs).encode()
        MANIFEST.append({
            "url": name,
            "http_status": "aggregate",
            "bytes": None,
            "sha256": hashlib.sha256(blob).hexdigest(),
            "fetched": now(),
            "what": what,
            "committed": False,
            "n": len(digs),
        })

    agg(GERRIT + "/changes/go~{n}/detail?o=ALL_REVISIONS&o=MESSAGES&o=DETAILED_LABELS",
        [d[2] for d in detail_stats],
        f"{len(detail_stats)} change details; aggregate sha256 over the sorted "
        f"per-response digests")
    agg(GERRIT + "/changes/go~{n}/comments",
        [c[2] for c in comment_stats],
        f"{len(comment_stats)} inline-comment records; aggregate sha256 over the "
        f"sorted per-response digests")
    agg(GERRIT + "/changes/go~{n}/revisions/{rev}/files/" + PATH_TEST + "/content",
        [t["raw_sha256"] for t in test_stats],
        f"{len(test_stats)} fetches of {PATH_TEST}, one per patch-set state; "
        f"aggregate sha256 over the sorted per-response digests")
    agg(GERRIT + "/changes/go~{n}/revisions/{rev}/files/" + PATH_TABLE + "/content",
        [c["raw_sha256"] for c in checks],
        f"{len(checks)} cross-route re-fetches of {PATH_TABLE}; aggregate sha256 "
        f"over the sorted per-response digests")

    # --- 6. write -------------------------------------------------------
    out = {
        "harvested": now(),
        "gerrit": GERRIT,
        "paths": {"table": PATH_TABLE, "test": PATH_TEST},
        "population": pop,
        "states": len(states),
        "detail_not_200": [{"url": d[0], "status": d[1]} for d in bad_d],
        "comments_not_200": [{"url": c[0], "status": c[1]} for c in bad_c],
        "test_file": {
            "present": have, "absent_404": miss,
            "other_status": [{"url": t["url"], "status": t["status"]} for t in other],
            "distinct": distinct_tests,
            "per_state": [{"change": t["change"], "ps": t["ps"], "rev": t["rev"],
                           "status": t["status"], "sha256": t["sha256"]}
                          for t in test_stats],
        },
        "cross_route_check": {
            "rule": "every patch-set state with patch set 1 whose change number "
                    "ends in the digit 7, fixed in PREDICTIONS.md §6",
            "n": len(checks), "matched": ok,
            "mismatched": bad, "unresolved": [u["url"] for u in unk],
            "rows": checks,
        },
        "raw_cache": os.path.relpath(raw_dir, HERE),
    }
    with open(os.path.join(HERE, "harvest.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)

    with open(os.path.join(HERE, "sources", "MANIFEST.json"), "w") as f:
        json.dump({
            "note": ("Fetched, hashed, and — for everything a person wrote — NOT "
                     "committed. Gerrit inline comments are third-party authored "
                     "text with no redistribution licence: their bodies live only "
                     "in the uncommitted raw cache, and this work quotes within "
                     "citation length. The object under study, Go's source, is "
                     "BSD-3-Clause; the states of table.go it reuses are already "
                     "in works/2026-08-25-under-the-commit/grids.json and are not "
                     "duplicated here. Bulk classes are recorded as aggregates: "
                     "the sha256 is taken over the newline-joined sorted list of "
                     "the per-response sha256 digests, which a re-run reproduces."),
            "entries": MANIFEST,
        }, f, indent=1)

    print(f"\n  wrote harvest.json and sources/MANIFEST.json "
          f"({len(MANIFEST)} manifest entries)")
    print("  raw bodies (uncommitted):", raw_dir)


if __name__ == "__main__":
    main()
