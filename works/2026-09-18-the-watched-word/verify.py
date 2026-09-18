#!/usr/bin/env python3
"""Eight checks on Session 92's night. Exits non-zero if any fails.

The point of this file is that a reader should not have to take the night's word for the order in
which it did things, or for the numbers surviving a re-run. Checks 1 and 2 are about the order;
3 to 5 are about reproduction; 6 to 8 are about the material.

    python3 verify.py
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
S85 = os.path.join(ROOT, "works", "2026-09-09-what-the-sentence-lets-in")
SENTENCE = ("Error is a special case of the epistemic thing — a difference onto which "
            "an observer has already imposed a norm.")
EMPHASIS = re.compile(r"[*_`]")
ok, fail = [], []


def check(name, condition, detail=""):
    (ok if condition else fail).append(f"{name}{(' — ' + detail) if detail else ''}")


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True).stdout.strip()


def first_commit(rel):
    out = git("log", "--diff-filter=A", "--format=%H", "--", rel)
    return out.splitlines()[-1] if out else ""


rel = lambda n: os.path.relpath(os.path.join(HERE, n), ROOT)

# 1 — the declaration precedes the instrument, by git and not by assertion.
cp, cc = first_commit(rel("PREDICTIONS.md")), first_commit(rel("census.py"))
if cp and cc:
    anc = subprocess.run(["git", "-C", ROOT, "merge-base", "--is-ancestor", cp, cc]).returncode == 0
    check("1 PREDICTIONS.md's commit is an ancestor of census.py's", anc or cp == cc, f"{cp[:8]} -> {cc[:8]}")
else:
    check("1 PREDICTIONS.md's commit is an ancestor of census.py's", False, "one of them is uncommitted")

# 2 — the shapes were committed with the declaration, not after the numbers.
cs = first_commit(rel("shapes.json"))
check("2 shapes.json was committed no later than census.py", bool(cs) and (cs == cp or cs == cc or
      subprocess.run(["git", "-C", ROOT, "merge-base", "--is-ancestor", cs, cc]).returncode == 0),
      f"{cs[:8]}")

# 3 — results.json reproduces byte for byte.
before = open(os.path.join(HERE, "results.json"), "rb").read()
subprocess.run([sys.executable, "census.py"], cwd=HERE, capture_output=True)
check("3 results.json reproduces byte-identically",
      before == open(os.path.join(HERE, "results.json"), "rb").read())

# 4 — adjudication.json reproduces byte for byte.
before = open(os.path.join(HERE, "adjudication.json"), "rb").read()
subprocess.run([sys.executable, "score.py"], cwd=HERE, capture_output=True)
check("4 adjudication.json reproduces byte-identically",
      before == open(os.path.join(HERE, "adjudication.json"), "rb").read())

R = json.load(open(os.path.join(HERE, "results.json"), encoding="utf-8"))
shapes = json.load(open(os.path.join(HERE, "shapes.json"), encoding="utf-8"))

# 5 — one sentence, three files, byte for byte.
check("5 the standing sentence is identical in shapes.json, census.py and results.json",
      shapes["_sentence"] == SENTENCE == R["sentence"]
      and SENTENCE in open(os.path.join(HERE, "census.py"), encoding="utf-8").read()
      .replace('"\n            "', ""))

# 6 — every quote, re-reconciled here rather than trusted from census.py.
bad = []
for s in shapes["shapes"]:
    text = EMPHASIS.sub("", open(os.path.join(ROOT, s["source"]), encoding="utf-8").read())
    if EMPHASIS.sub("", s["quote"]) not in text:
        bad.append(s["id"])
for r in json.load(open(os.path.join(S85, "readings.json"), encoding="utf-8"))["readings"]:
    text = EMPHASIS.sub("", open(os.path.join(ROOT, r["source"]), encoding="utf-8").read())
    if EMPHASIS.sub("", r["quote"]) not in text:
        bad.append(f"reading:{r['word']}:S{r['session']}")
check("6 every quote in shapes.json and in Session 85's readings.json is in the file it names",
      not bad, ", ".join(bad))

# 7 — the windows are disjoint, equal in length, and neither contains the night that fixed the row.
pre, post = R["windows"]["pre"]["sessions"], R["windows"]["post"]["sessions"]
check("7 the two windows are disjoint, six nights each, and exclude Session 85",
      len(pre) == len(post) == 6 and not set(pre) & set(post) and 85 not in pre + post)

# 8 — the unread terms, recomputed straight from Session 85's table.
worded = {r["word"] for r in json.load(open(os.path.join(S85, "readings.json"),
                                            encoding="utf-8"))["readings"]}
recomputed = sorted(t for t in R["terms"] if t not in worded)
check("8 the seven unread terms recompute from readings.json",
      recomputed == sorted(R["unread_terms"]) and len(recomputed) == 7, ", ".join(recomputed))

for line in ok:
    print("  ok   ", line)
for line in fail:
    print("  FAIL ", line)
print(f"\n{len(ok)} passed, {len(fail)} failed")
sys.exit(1 if fail else 0)
