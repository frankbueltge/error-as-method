#!/usr/bin/env python3
"""
preflight.py -- is this checkout actually current before the night starts?

WHY THIS EXISTS. Three nights running, the same fault. Session 46 began work on a branch two commits
behind `origin/main` and caught it when a path did not exist. Session 47 began four commits behind,
caught it when `ls tools/` returned nothing, and along the way wrote out a full correction accusing
its predecessor of a failure that was its own stale tree. Session 47 filed the decision to Session
48: does a pre-flight check belong in `tools/`, or is one line in the protocol enough?

Session 48's answer is this file, and the reasoning is on the record in `journal/2026-08-11-session-48.md`.
Short version: the practice already refused once to fix a copied number with a sentence -- that
refusal is `tools/sessions.py` -- and the same argument applies here. A warning is a sentence. What
caught the fault on both prior nights was an *instrument returning an unexpected result*. So: an
instrument.

HONEST LIMIT, stated at the top rather than buried. This only helps if it is run, which makes it a
sentence in a different typeface unless the standing instruction that opens these nights names it,
the way that instruction now names `tools/sessions.py`. That instruction is not mine to edit. It is
asked for in REQUESTS.md, 2026-08-11.

    python3 tools/preflight.py

Exit code 0 if the checkout is current, 1 if it is not. Read-only except for the fetch: it never
checks out, merges, resets or deletes anything.
"""

import subprocess
import sys


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        return None
    return r.stdout.strip()


def main():
    if git("rev-parse", "--git-dir") is None:
        print("preflight: not a git repository.")
        return 2

    default = "main"
    print("preflight -- checking this tree against the remote before the night starts\n")

    print(f"  fetching origin/{default} ...")
    if subprocess.run(["git", "fetch", "origin", default],
                      capture_output=True, text=True).returncode != 0:
        print(f"  COULD NOT FETCH. The comparison below is against whatever `origin/{default}` said\n"
              f"  the last time this tree heard from the remote, which is exactly the thing this\n"
              f"  script exists to distrust. Treat every line after this as unverified.\n")

    remote = git("rev-parse", f"origin/{default}")
    head = git("rev-parse", "HEAD")
    branch = git("rev-parse", "--abbrev-ref", "HEAD") or "(detached)"
    if remote is None:
        print(f"  no ref origin/{default}. Nothing to compare against.")
        return 2

    behind = git("rev-list", "--count", f"HEAD..origin/{default}") or "?"
    ahead = git("rev-list", "--count", f"origin/{default}..HEAD") or "?"

    print(f"\n  branch           : {branch}")
    print(f"  HEAD             : {head[:12]}  {git('log','-1','--format=%s', head) or ''}")
    print(f"  origin/{default:<9} : {remote[:12]}  {git('log','-1','--format=%s', remote) or ''}")
    print(f"  behind / ahead   : {behind} / {ahead}")

    dirty = git("status", "--porcelain")
    if dirty:
        print(f"  uncommitted      : {len(dirty.splitlines())} path(s)")

    print()
    if behind == "0":
        print(f"  OK. This tree contains everything on origin/{default}.")
        print(f"     Cut the night's branch from here: git checkout -b night/<date> origin/{default}")
        return 0

    print(f"  STALE. {behind} commit(s) on origin/{default} are not in this tree.")
    print(f"     Anything you conclude from files that are missing here may be an artefact of that.")
    print(f"     Session 47 wrote a full correction against its predecessor on exactly this ground,")
    print(f"     and the predecessor was right. Before working:")
    print(f"        git checkout -b night/<date> origin/{default}")
    print(f"\n     Commits you do not have:")
    for line in (git("log", "--oneline", f"HEAD..origin/{default}") or "").splitlines()[:12]:
        print(f"        {line}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
