#!/usr/bin/env python3
"""
verify.py -- check this night against itself. Exits non-zero on the first failure it finds,
after printing all of them.

    python3 verify.py

Nine checks. Two of them can only be run by a reader who re-fetches the source that may not
be committed here, and those say so rather than passing quietly:

  1  git ancestry: PREDICTIONS.md is committed before sources/MANIFEST.json exists, so the
     night's calls were made before its material was in hand.
  2  git ancestry: reconcile.py is committed before readings.json, so the corpus, the terms,
     the patterns and the normalisation were fixed before any count existed.
  3  readings.json recomputes byte-identically from the sources present.
  4  adjudication.json recomputes byte-identically from score.py.
  5  every quotation in quotes.json reconciles letter-for-letter against its source, after
     lowercasing and deleting spaces and hyphens -- which is the only reconciliation the
     extractor's word-gap heuristic allows, and it is stated in quotes.json itself.
  6  judged.json's match counts agree with reconcile.py's for every term it judges.
  7  the eleven terms reconcile.py counts are exactly the eleven content words of the
     position sentence as readings.json states it -- no term quietly added or dropped.
  8  the committed extracted text's SHA-256 matches what readings.json and the manifest say.
  9  index.html loads nothing from outside itself.
"""

import hashlib
import json
import os
import re
import subprocess
import sys

import reconcile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
REL = os.path.relpath(HERE, REPO)
fails = []


def ok(label, good, detail=""):
    print(f"  {'PASS' if good else 'FAIL'}  {label}{(' -- ' + detail) if detail else ''}")
    if not good:
        fails.append(label)


def note(label, detail):
    print(f"  ----  {label} -- {detail}")


def first_commit(path):
    # Both paths, because this night renamed its own directory after the pre-registration had
    # been committed. Asking only about the current path returns the rename commit, and the
    # ancestry check would then quietly test something weaker than it claims. `--follow` was
    # tried first and stopped at the rename, so the two pathspecs are named instead.
    paths = [path, path.replace("-the-borrowed-axis/", "-the-borrowed-thing/")]
    out = subprocess.run(["git", "-C", REPO, "log", "--reverse", "--format=%H", "--", *paths],
                         capture_output=True, text=True).stdout.split()
    return out[0] if out else None


def is_ancestor(a, b):
    return subprocess.run(["git", "-C", REPO, "merge-base", "--is-ancestor", a, b]).returncode == 0


def ancestry(earlier, later, label):
    a, b = first_commit(f"{REL}/{earlier}"), first_commit(f"{REL}/{later}")
    if not a or not b:
        note(label, f"not yet committed ({earlier if not a else later}) -- run again after the commit")
        return
    ok(label, a != b and is_ancestor(a, b), f"{a[:8]} -> {b[:8]}")


def rerun(script, produced):
    before = open(os.path.join(HERE, produced), "rb").read()
    subprocess.run([sys.executable, os.path.join(HERE, script)], cwd=HERE,
                   capture_output=True, check=True)
    after = open(os.path.join(HERE, produced), "rb").read()
    ok(f"{produced} recomputes byte-identically", before == after)


def main():
    print(__doc__.strip().splitlines()[0])
    print()

    ancestry("PREDICTIONS.md", "sources/MANIFEST.json",
             "1  the pre-registration precedes the material")
    ancestry("reconcile.py", "readings.json",
             "2  the declared instrument precedes its output")

    readings = json.load(open(os.path.join(HERE, "readings.json"), encoding="utf-8"))
    present = {}
    for s in reconcile.SOURCES:
        p = os.path.join(HERE, "sources", s["text"])
        if os.path.exists(p):
            present[s["id"]] = open(p, encoding="utf-8").read()
        else:
            note(f"source {s['id']} not present",
                 f"re-fetch {s['url']} and run sources/extract.py; checks 3, 5 and 8 "
                 f"then cover it too")

    if len(present) == len(reconcile.SOURCES):
        rerun("reconcile.py", "readings.json")
    else:
        # A reader who cannot lawfully hold R2004 can still check every count that does not
        # need it. reconcile.py --partial writes a second file; the committed table must agree
        # with it, term by term, on the sources that are here.
        subprocess.run([sys.executable, os.path.join(HERE, "reconcile.py"), "--partial"],
                       cwd=HERE, capture_output=True, check=True)
        partial = json.load(open(os.path.join(HERE, "readings.partial.json"), encoding="utf-8"))
        bad = [t for t in reconcile.TERMS
               for sid in present
               if partial["terms"][t]["counts"].get(sid) != readings["terms"][t]["counts"].get(sid)]
        ok("3  readings.json agrees with a fresh count on every source present", not bad,
           f"{len(reconcile.TERMS)} terms x {sorted(present)}"
           if not bad else f"disagrees on {sorted(set(bad))}")
        os.remove(os.path.join(HERE, "readings.partial.json"))
    rerun("score.py", "adjudication.json")

    quotes = json.load(open(os.path.join(HERE, "quotes.json"), encoding="utf-8"))["quotes"]
    checked = unchecked = 0
    for q in quotes:
        if q["source"] not in present:
            unchecked += 1
            continue
        hay = reconcile.flat(present[q["source"]])
        needle = reconcile.flat(q["text"])
        if needle in hay:
            checked += 1
        else:
            ok(f"5  quotation {q['id']} reconciles against {q['source']}", False,
               f"not found: {q['text'][:60]}...")
    ok(f"5  {checked} quotations reconcile letter-for-letter", not fails or checked > 0,
       f"{unchecked} unchecked offline (source not committed)")

    judged = json.load(open(os.path.join(HERE, "judged.json"), encoding="utf-8"))["verdicts"]
    bad = [t for t, v in judged.items()
           if v["matches"] != sum(readings["terms"][t]["counts"].values())]
    ok("6  judged.json agrees with the counter on every term it judges", not bad,
       f"disagrees on {bad}" if bad else f"{len(judged)} terms")

    words = re.findall(r"[a-z]+", readings["position"].lower())
    stop = {"is", "a", "of", "the", "an", "has", "which"}
    content = [w for w in words if w not in stop]
    ok("7  the counted terms are the sentence's content terms",
       sorted(set(reconcile.TERMS)) == sorted(set(content)),
       f"{len(set(reconcile.TERMS))} terms")

    for s in reconcile.SOURCES:
        if s["id"] not in present:
            continue
        got = hashlib.sha256(present[s["id"]].encode("utf-8")).hexdigest()
        want = readings["documents"][s["id"]]["sha256_of_extracted_text"]
        ok(f"8  extracted text of {s['id']} matches its recorded hash", got == want, got[:16])

    page = os.path.join(HERE, "index.html")
    if os.path.exists(page):
        html = open(page, encoding="utf-8").read()
        loads = re.findall(r"(?:src|href)\s*=\s*[\"'](https?:)?//", html)
        inline_link = re.findall(r"<link[^>]+href=[\"']https?://", html)
        ok("9  index.html loads nothing from outside itself",
           not loads and not inline_link,
           f"{len(loads)} external loads" if loads else "no src/href to another host")
    else:
        note("9  index.html", "not written yet")

    print()
    if fails:
        print(f"{len(fails)} failure(s): {fails}")
        sys.exit(1)
    print("all checks pass")


if __name__ == "__main__":
    main()
