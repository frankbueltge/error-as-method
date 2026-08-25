#!/usr/bin/env python3
"""Harvest the three grids for Session 70.

Reads Go's GODEBUG table, `src/internal/godebugs/table.go`, at three nested
sampling units:

  release   -- every go1.N / go1.N.P tag whose tree contains the file
  commit    -- every commit reachable from a branch or tag that touches the file
  patchset  -- every Gerrit revision of every change in the union population
               defined in PREDICTIONS.md sec. 3

Method. A blobless clone of go.googlesource.com/go supplies the *structure*
(refs, commits, trees) at no bandwidth cost; the Gerrit patchset refs are
fetched into it by name. Blob *content* is then fetched over HTTP from
gitiles, once per DISTINCT blob object id -- 175 objects stand behind ~1,100
sampling points -- and each fetched byte string is verified against the object
id git itself recorded for it (sha1 of "blob <len>\\0" + content). A mismatch
is a hard error, not a warning.

The first version of this script read blobs out of the partial clone with
`git cat-file`, which triggers one lazy fetch per object at ~85 s each. That
is recorded in the night's adjudication as C0, not silently repaired.

Stdlib only. Usage:  python3 harvest.py <path-to-blobless-clone>
Writes: changes.json, grids.json, sources/MANIFEST.json
"""

import base64
import concurrent.futures
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = "src/internal/godebugs/table.go"
GERRIT = "https://go-review.googlesource.com"
GITILES = "https://go.googlesource.com/go"
QUERIES = [
    "file:src/internal/godebugs/table.go",
    "file:doc/godebug.md",
    "file:src/internal/godebug/godebug.go",
]
TAG_RE = re.compile(r"^go1\.\d+(\.\d+)?$")
MANIFEST = []
REPO = None


def note(url, status, body, what):
    MANIFEST.append({"url": url, "http_status": status, "bytes": len(body),
                     "sha256": hashlib.sha256(body).hexdigest(),
                     "fetched": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                     "what": what, "committed": False})


def fetch(url, what=None):
    req = urllib.request.Request(url, headers={"User-Agent": "error-as-method/session-70"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                body, status = r.read(), r.status
            if what:
                note(url, status, body, what)
            return body
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def gerrit_json(url, what):
    body = fetch(url, what).decode("utf-8")
    return json.loads(body[body.index("\n") + 1:] if body.startswith(")]}'") else body)


def git(*args):
    return subprocess.run(["git", "-C", REPO, *args], capture_output=True,
                          text=True, check=False).stdout


# ---------------------------------------------------------------- population

def collect_changes():
    changes = {}
    for q in QUERIES:
        url = "%s/changes/?q=%s&n=500&o=ALL_REVISIONS" % (
            GERRIT, urllib.parse.quote(q, safe=":"))
        got = gerrit_json(url, "Gerrit change search: %s" % q)
        if got and got[-1].get("_more_changes"):
            raise SystemExit("population truncated for %s -- raise n" % q)
        for c in got:
            rec = changes.setdefault(c["_number"], {
                "number": c["_number"], "project": c.get("project"),
                "branch": c.get("branch"), "status": c.get("status"),
                "subject": c.get("subject"), "created": c.get("created"),
                "updated": c.get("updated"),
                "owner": c.get("owner", {}).get("_account_id"),
                "queries": [], "revisions": {}})
            rec["queries"].append(q)
            for sha, rv in (c.get("revisions") or {}).items():
                rec["revisions"][sha] = {"number": rv.get("_number"), "ref": rv.get("ref"),
                                         "kind": rv.get("kind"), "created": rv.get("created"),
                                         "uploader": rv.get("uploader", {}).get("_account_id")}
    return changes


def fetch_refs(refs):
    got, missing = 0, []
    spec = lambda r: "%s:refs/patchsets/%s" % (r, r.replace("refs/changes/", ""))
    for i in range(0, len(refs), 60):
        batch = refs[i:i + 60]
        r = subprocess.run(["git", "-C", REPO, "fetch", "--quiet", "--filter=blob:none",
                            "origin", *[spec(x) for x in batch]],
                           capture_output=True, text=True, check=False)
        if r.returncode == 0:
            got += len(batch)
        else:
            for one in batch:
                r1 = subprocess.run(["git", "-C", REPO, "fetch", "--quiet",
                                     "--filter=blob:none", "origin", spec(one)],
                                    capture_output=True, text=True, check=False)
                (missing.append(one) if r1.returncode else None)
                got += 0 if r1.returncode else 1
        print("  refs %d/%d" % (min(i + 60, len(refs)), len(refs)), flush=True)
    return got, missing


# ------------------------------------------------------------------- content

def blob_oid(rev):
    """The object id git records for PATH at rev, or None if absent."""
    out = git("ls-tree", rev, PATH).strip()
    return out.split()[2] if out else None


def fetch_blob(oid_and_rev):
    """Fetch one blob's bytes via gitiles and verify it against its object id."""
    oid, rev = oid_and_rev
    url = "%s/+/%s/%s?format=TEXT" % (GITILES, rev, urllib.parse.quote(PATH))
    raw = base64.b64decode(fetch(url))
    check = hashlib.sha1(b"blob %d\x00" % len(raw) + raw).hexdigest()
    if check != oid:
        raise SystemExit("object id mismatch at %s: git says %s, bytes hash to %s"
                         % (rev, oid, check))
    return oid, raw


def main():
    global REPO
    REPO = sys.argv[1]

    print("Gerrit population ...", flush=True)
    changes = collect_changes()
    go_changes = {n: c for n, c in changes.items() if c["project"] == "go"}
    print("  %d changes, %d in project go" % (len(changes), len(go_changes)), flush=True)

    refs = sorted({rv["ref"] for c in go_changes.values()
                   for rv in c["revisions"].values() if rv["ref"]})
    have = set(git("for-each-ref", "--format=%(refname)", "refs/patchsets/").split())
    want = [r for r in refs
            if "refs/patchsets/" + r.replace("refs/changes/", "") not in have]
    print("fetching %d of %d patchset refs ..." % (len(want), len(refs)), flush=True)
    got, missing = fetch_refs(want) if want else (0, [])

    # --- the three grids, as lists of sampling points --------------------
    tags_all = [t for t in git("tag").split() if TAG_RE.match(t)]
    tags_all.sort(key=lambda t: [int(x) for x in t[2:].split(".")])
    tagdate = {}
    for t in tags_all:
        tagdate[t] = subprocess.run(["git", "-C", REPO, "log", "-1", "--format=%cI", t],
                                    capture_output=True, text=True).stdout.strip()
    release = [{"grid": "release", "point": t, "rev": t, "cdate": tagdate[t]}
               for t in tags_all]

    # NOTE: `--all` would now include refs/patchsets/*, which are exactly what
    # the commit grid must exclude. The commit grid is the project's own refs.
    proj_refs = [r for r in git("for-each-ref", "--format=%(refname)",
                                "refs/remotes/", "refs/tags/").split()]
    # %cI, the committer date, is the order in which states entered the
    # history; %aI survives rebase and would misorder them.
    log = subprocess.run(["git", "-C", REPO, "log", "--format=%H%x09%aI%x09%cI%x09%an%x09%s",
                          *proj_refs, "--", PATH], capture_output=True, text=True).stdout
    # Branches interleave in date order, so "the next state" is only well
    # defined along one lineage. master_rank walks the first-parent history of
    # origin/master: 0 is the newest state there, None means the commit is on
    # a release branch or a dev branch and never on master.
    master = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "origin/master",
                             "--", PATH], capture_output=True, text=True).stdout.split()
    rank = {sha: i for i, sha in enumerate(master)}
    seen, commit = set(), []
    for line in log.strip().splitlines():
        sha, date, cdate, author, subject = line.split("\t", 4)
        if sha in seen:
            continue
        seen.add(sha)
        commit.append({"grid": "commit", "point": sha, "rev": sha, "date": date,
                       "cdate": cdate, "author": author, "subject": subject,
                       "master_rank": rank.get(sha)})

    patchset = []
    for c in sorted(go_changes.values(), key=lambda c: c["number"]):
        for sha, rv in sorted(c["revisions"].items(), key=lambda kv: kv[1]["number"] or 0):
            patchset.append({"grid": "patchset", "point": sha, "rev": sha,
                             "change": c["number"], "status": c["status"],
                             "branch": c["branch"], "subject": c["subject"],
                             "patchset": rv["number"], "ref": rv["ref"],
                             "kind": rv["kind"], "created": rv["created"]})

    # --- map every point to its blob object id ---------------------------
    absent = {"release": 0, "commit": 0, "patchset": 0}
    points, need = [], {}
    for p in release + commit + patchset:
        oid = blob_oid(p["rev"])
        if oid is None:
            absent[p["grid"]] += 1
            continue
        p["blob"] = oid
        need.setdefault(oid, p["rev"])
        points.append(p)
    print("%d points carry the file, %d distinct blobs" % (len(points), len(need)), flush=True)

    # --- fetch each distinct blob once, verified against its object id ----
    blobs, done = {}, 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for oid, raw in ex.map(fetch_blob, sorted(need.items())):
            blobs[oid] = raw.decode("utf-8", "replace")
            done += 1
            if done % 25 == 0:
                print("  blobs %d/%d" % (done, len(need)), flush=True)
    note("%s/+/<rev>/%s?format=TEXT" % (GITILES, PATH), 200, b"",
         "%d distinct blob objects fetched by rev+path and verified against the "
         "object id git recorded for each" % len(blobs))

    out = {
        "harvested": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "path": PATH,
        "population": {
            "changes_in_union": len(changes),
            "changes_project_go": len(go_changes),
            "changes_other_projects": sorted({c["project"] for c in changes.values()
                                              if c["project"] != "go"}),
            "patchset_refs": len(refs),
            "patchset_refs_fetched_this_run": got,
            "patchset_refs_unfetchable": missing,
            "release_tags_matching": len(tags_all),
            "points_without_the_file": absent,
            "release_points": sum(1 for p in points if p["grid"] == "release"),
            "commit_points": sum(1 for p in points if p["grid"] == "commit"),
            "patchset_points": sum(1 for p in points if p["grid"] == "patchset"),
            "distinct_blobs": len(blobs),
        },
        "blobs": blobs,
        "points": points,
    }
    json.dump(out, open(os.path.join(HERE, "grids.json"), "w"), indent=1)
    json.dump({str(k): v for k, v in sorted(changes.items())},
              open(os.path.join(HERE, "changes.json"), "w"), indent=1)
    os.makedirs(os.path.join(HERE, "sources"), exist_ok=True)
    json.dump({"note": "Fetched, hashed, not committed -- see PROTOCOL.md, 'Sources are "
                       "committed only where the licence allows it'. Per-state content "
                       "hashes are in grids.json; the object ids are git's own.",
               "entries": MANIFEST},
              open(os.path.join(HERE, "sources", "MANIFEST.json"), "w"), indent=1)
    print(json.dumps(out["population"], indent=1))


if __name__ == "__main__":
    main()
