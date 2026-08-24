#!/usr/bin/env python3
"""Harvest the population: Lib/__future__.py at every commit that has ever touched it,
on every ref in CPython's public history.

This is the de-aligned instrument declared in PREDICTIONS.md §3. Session 62 read this
file at 22 points — every published minor release, which is the object's own unit of
publication. Tonight reads it at every commit, which is not.

The clone is made outside this repository and is not committed; the bytes of
Lib/__future__.py are written to sources/blobs/ and are not committed either
(PROTOCOL.md, amendment of 2026-08-18 — one hash apiece is the better warrant, and
CPython being PSF-2.0 does not make forty copies of one file a good idea). What is
committed is sources/MANIFEST.json and the derived tables.

    python3 harvest.py [--clone /path/to/cpython]

Re-run from an empty sources/blobs/ and the measurement is identical: every blob is
addressed by its git object id, so the harvest is exactly reproducible from the same
upstream history.

Network is used only here. measure.py is offline.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")
BLOBS = os.path.join(SRC, "blobs")

PATH = "Lib/__future__.py"
UPSTREAM = "https://github.com/python/cpython.git"

# Session 62's population, re-derived here from the same clone rather than re-fetched over
# the network. Two reasons it is re-derived at all. First, S62's results.json records the
# full five-element boundary tuple only for MandatoryRelease and reduces OptionalRelease to
# a "major.minor" string, so a like-for-like comparison at tuple precision needs the release
# files themselves. Second, re-deriving lets tonight check S62's own numbers against its own
# population instead of trusting them, which is the cheaper half of auditing an inherited
# work. The tag naming is not uniform across this project's history, so both forms are tried
# — exactly as S62's own harvest.py does.
SERIES = [
    (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7),
    (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
    (3, 8), (3, 9), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14),
]


# The documents that decide what the two boundary fields mean and when the releases in
# question actually happened. Fetched over the network, hashed, not committed.
DOCS = [
    ("pep-0236", "https://peps.python.org/pep-0236/",
     "PEP 236, 'Back to the __future__', Tim Peters, 2001",
     "The document that authored both fields and says which records and which predicts"),
    ("pep-0356", "https://peps.python.org/pep-0356/",
     "PEP 356, 'Python 2.5 Release Schedule'",
     "The release dates that decide whether 2.5 alpha 1 existed on 2006-02-28"),
    ("pep-0343", "https://peps.python.org/pep-0343/",
     "PEP 343, 'The \"with\" Statement'",
     "The feature whose OptionalRelease is the one that moved"),
    ("docs-future", "https://docs.python.org/3/library/__future__.html",
     "CPython documentation, __future__ — Future statement definitions",
     "The project's current published statement of what OptionalRelease is"),
]


def fetch(url):
    import urllib.error
    import urllib.request
    req = urllib.request.Request(
        url, headers={"User-Agent": "error-as-method/night-2026-08-24"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:  # noqa: BLE001 — recorded, not swallowed
        return None, str(e).encode()


def git(clone, *args):
    out = subprocess.run(
        ["git", "-C", clone, *args],
        capture_output=True, check=True,
    )
    return out.stdout.decode("utf-8", "replace")


def ensure_clone(clone):
    """A blobless clone of the complete history, all refs. Blobs arrive on demand."""
    if os.path.isdir(os.path.join(clone, ".git")):
        return clone
    os.makedirs(os.path.dirname(clone) or ".", exist_ok=True)
    subprocess.run(
        ["git", "clone", "--filter=blob:none", "--no-checkout", UPSTREAM, clone],
        check=True,
    )
    subprocess.run(
        ["git", "-C", clone, "config", "remote.origin.fetch",
         "+refs/heads/*:refs/remotes/origin/*"], check=True,
    )
    subprocess.run(
        ["git", "-C", clone, "fetch", "--filter=blob:none", "--tags", "origin"],
        check=True,
    )
    return clone


def commits_touching(clone):
    """Every commit on every ref whose diff touches PATH, oldest first.

    --all is the whole ref set, not just main: nine of these commits are off the main
    line and a release-tag instrument would not have reached them either.
    """
    fmt = "%H%x00%an%x00%aI%x00%cI%x00%s"
    raw = git(clone, "log", "--all", "--reverse", "--no-merges",
              f"--format={fmt}", "--", PATH)
    rows = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        sha, author, adate, cdate, subject = line.split("\x00", 4)
        rows.append({
            "sha": sha, "author": author,
            "author_date": adate, "commit_date": cdate,
            "subject": subject,
        })
    return rows


def merges_touching(clone):
    """Merge commits are excluded from the population above; count them so the
    exclusion is a stated number and not a silence."""
    raw = git(clone, "log", "--all", "--merges", "--format=%H", "--", PATH)
    return [s for s in raw.split() if s]


def blob_at(clone, sha):
    """The file as it stands at that commit. Returns (blob_oid, bytes) or None if the
    commit deletes the path."""
    try:
        oid = git(clone, "rev-parse", f"{sha}:{PATH}").strip()
    except subprocess.CalledProcessError:
        return None
    data = subprocess.run(
        ["git", "-C", clone, "cat-file", "blob", oid],
        capture_output=True, check=True,
    ).stdout
    return oid, data


def refs_containing(clone, sha):
    """Which release tags contain this commit. Used only to place a commit in the
    project's own timeline; never used to decide a value."""
    try:
        raw = git(clone, "tag", "--contains", sha)
    except subprocess.CalledProcessError:
        return []
    return sorted(t.strip() for t in raw.splitlines() if t.strip())


def release_tags(clone):
    """The first ref that answers for each minor series, in S62's own three probe forms.

    The first version of this function probed only the two forms S62's code comment
    mentions and reported 2.3 as a hole; S62's code probes three, and the third answers.
    Mine was the deficient instrument and the correction is recorded rather than quietly
    applied: see verdict.json, correction C0.

    What is added here, and it is the whole point of re-deriving the grid: each ref is
    resolved and *described*. raw.githubusercontent.com resolves tags and branch heads
    alike and reports neither, so a fetch that answers 200 is not evidence that what
    answered is a release.
    """
    found = []
    for major, minor in SERIES:
        rec = {"series": f"{major}.{minor}", "tag": None, "probed": []}
        for cand in (f"v{major}.{minor}", f"v{major}.{minor}.0", f"{major}.{minor}"):
            rec["probed"].append(cand)
            try:
                commit = git(clone, "rev-parse", f"{cand}^{{commit}}").strip()
            except subprocess.CalledProcessError:
                continue
            rec["tag"] = cand
            rec["commit"] = commit
            rec["ref_kind"] = (
                "tag" if _exists(clone, f"refs/tags/{cand}")
                else "branch" if _exists(clone, f"refs/remotes/origin/{cand}")
                else "other"
            )
            rec["tag_subject"] = git(
                clone, "log", "-1", "--format=%s", commit).strip()
            rec["tag_date"] = git(
                clone, "log", "-1", "--format=%cI", commit).strip()
            break
        # Everything else the project tagged in this series, so a substitution is visible.
        siblings = git(clone, "tag", "-l", f"v{major}.{minor}*",
                       f"{major}.{minor}*").split()
        rec["sibling_tags"] = sorted(siblings)
        found.append(rec)
    return found


def _exists(clone, ref):
    try:
        git(clone, "rev-parse", "--verify", ref)
        return True
    except subprocess.CalledProcessError:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", default=os.path.join(HERE, "_cpython"),
                    help="where the blobless clone lives (outside git, not committed)")
    args = ap.parse_args()

    clone = ensure_clone(args.clone)
    os.makedirs(BLOBS, exist_ok=True)

    rows = commits_touching(clone)
    merges = merges_touching(clone)
    total_commits = git(clone, "rev-list", "--count", "--all").strip()

    manifest = {
        "night": "2026-08-24",
        "session": 69,
        "upstream": UPSTREAM,
        "path": PATH,
        "note": (
            "Bytes fetched and hashed, deliberately not committed (PROTOCOL.md, "
            "amendment of 2026-08-18). Every blob is addressed by its git object id, "
            "so a stranger reproduces this exactly: clone the upstream, run harvest.py, "
            "compare blob_oid and sha256."
        ),
        "population": {
            "commits_touching_path_all_refs": len(rows),
            "merge_commits_touching_path_excluded": len(merges),
            "commits_in_history_all_refs": int(total_commits),
        },
        "sources": [],
    }

    for i, r in enumerate(rows):
        got = blob_at(clone, r["sha"])
        if got is None:
            r["blob_oid"] = None
            r["sha256"] = None
            r["bytes"] = 0
            r["deleted"] = True
        else:
            oid, data = got
            r["blob_oid"] = oid
            r["sha256"] = hashlib.sha256(data).hexdigest()
            r["bytes"] = len(data)
            r["deleted"] = False
            with open(os.path.join(BLOBS, f"{i:03d}-{oid[:12]}.py"), "wb") as fh:
                fh.write(data)
        r["ordinal"] = i
        r["tags_containing"] = refs_containing(clone, r["sha"])
        manifest["sources"].append({
            "key": f"future-commit-{i:03d}",
            "url": f"https://github.com/python/cpython/commit/{r['sha']}",
            "commit": r["sha"],
            "blob_oid": r["blob_oid"],
            "what": f"Lib/__future__.py as it stood at {r['sha'][:12]}",
            "why": "Population P-B: the boundary field at every commit that touched it",
            "bytes": r["bytes"],
            "sha256": r["sha256"],
            "retrieved": "2026-08-24",
            "local": f"blobs/{i:03d}-{(r['blob_oid'] or 'deleted')[:12]}.py "
                     f"(fetched, not committed)",
        })

    # Population P-A: S62's own grid, re-derived from the same clone.
    rels = release_tags(clone)
    for j, rel in enumerate(rels):
        if rel["tag"] is None:
            rel["blob_oid"] = rel["sha256"] = None
            rel["bytes"] = 0
            continue
        got = blob_at(clone, rel["tag"])
        if got is None:
            rel["blob_oid"] = rel["sha256"] = None
            rel["bytes"] = 0
            continue
        oid, data = got
        rel["blob_oid"] = oid
        rel["sha256"] = hashlib.sha256(data).hexdigest()
        rel["bytes"] = len(data)
        with open(os.path.join(BLOBS, f"rel-{rel['series']}-{oid[:12]}.py"), "wb") as fh:
            fh.write(data)
        manifest["sources"].append({
            "key": f"future-release-{rel['series']}",
            "url": f"https://raw.githubusercontent.com/python/cpython/{rel['tag']}/{PATH}",
            "tag": rel["tag"],
            "blob_oid": oid,
            "what": f"Lib/__future__.py as published in CPython {rel['tag']}",
            "why": "Population P-A: Session 62's grid, re-derived for a like-for-like check",
            "bytes": rel["bytes"],
            "sha256": rel["sha256"],
            "retrieved": "2026-08-24",
            "local": f"blobs/rel-{rel['series']}-{oid[:12]}.py (fetched, not committed)",
        })

    manifest["population"]["release_tags_read"] = sum(1 for r in rels if r["blob_oid"])

    for key, url, what, why in DOCS:
        status, body = fetch(url)
        if status == 200:
            with open(os.path.join(BLOBS, f"{key}.html"), "wb") as fh:
                fh.write(body)
        manifest["sources"].append({
            "key": key,
            "url": url,
            "what": what,
            "why": why,
            "status": status,
            "bytes": len(body) if status == 200 else None,
            "sha256": hashlib.sha256(body).hexdigest() if status == 200 else None,
            "retrieved": "2026-08-24",
            "local": f"blobs/{key}.html (fetched, not committed)" if status == 200 else None,
        })
        print(f"  {key:<12} {status}")

    # The gate's allowlist covers works/ and not the repository root, so the ignore rule
    # for the harvested bytes lives here — S62's F-046, and it still applies.
    with open(os.path.join(SRC, ".gitignore"), "w") as fh:
        fh.write(
            "# Harvested bytes are fetched and hashed, never committed: PROTOCOL.md,\n"
            "# amendment of 2026-08-18. MANIFEST.json beside them is the warrant — every\n"
            "# blob is addressed by its git object id, so a stranger clones the upstream,\n"
            "# re-runs harvest.py and compares.\n"
            "blobs/\n"
        )

    with open(os.path.join(HERE, "commits.json"), "w") as fh:
        json.dump({"path": PATH, "upstream": UPSTREAM,
                   "commits": rows, "releases": rels}, fh, indent=1)
    with open(os.path.join(SRC, "MANIFEST.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)

    print(f"{len(rows)} commits touching {PATH} on all refs "
          f"({len(merges)} merge commits excluded), "
          f"out of {total_commits} commits in the history; "
          f"{manifest['population']['release_tags_read']} release tags re-read.")


if __name__ == "__main__":
    sys.exit(main())
