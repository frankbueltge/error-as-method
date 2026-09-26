#!/usr/bin/env python3
"""verify.py -- what this work claims about its own order and its borrowed instruments, checked.

1. Ancestry: the commit that added PREDICTIONS.md precedes the one that added corpus.json.gz, which
   precedes the one that added results.json; inspection.json comes after results.json.
2. The instruments imported by path are unchanged since the nights that published them: no commit
   after Session 94's touches measure.py (S86), reach.py (S90), validate.py (S91), port.py or
   inspect.py (S94).
3. The exploratory 'immediate' rate in inspection.json reproduces Session 94's published
   subjecthood for all four earlier traditions, so the post-hoc instrument measures what it says.
4. The corpus on disk hashes as the manifest says.
"""
import gzip
import hashlib
import json
import subprocess
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parent.parent
REL = H.relative_to(ROOT)
ok = True


def check(cond, msg):
    global ok
    ok &= bool(cond)
    print(("  ok   " if cond else "  FAIL ") + msg)


def added(path):
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%H %ct", "--", str(path)],
                         cwd=ROOT, capture_output=True, text=True).stdout.split()
    return (out[-2], int(out[-1])) if out else (None, None)


def before(a, b):
    return subprocess.run(["git", "merge-base", "--is-ancestor", a, b], cwd=ROOT).returncode == 0 \
        and a != b


pre, har, res, ins = (added(REL / f) for f in ("PREDICTIONS.md", "corpus.json.gz", "results.json",
                                               "inspection.json"))
check(pre[0] and har[0] and before(pre[0], har[0]), "PREDICTIONS.md committed before the harvest")
check(har[0] and res[0] and before(har[0], res[0]), "harvest committed before results.json")
check(ins[0] is None or before(res[0], ins[0]), "inspection.json after results.json (or not yet committed)")

S94_COMMIT = added(Path("works/2026-09-21-three-other-offices/port.py"))[0]
for f in ("works/2026-09-10-only-when-capitals/measure.py", "works/2026-09-15-not-part-of-the-act/reach.py",
          "works/2026-09-17-the-second-instrument/validate.py",
          "works/2026-09-21-three-other-offices/port.py", "works/2026-09-21-three-other-offices/inspect.py"):
    later = subprocess.run(["git", "log", "--format=%h", S94_COMMIT + "..HEAD", "--", f],
                           cwd=ROOT, capture_output=True, text=True).stdout.split()
    dirty = subprocess.run(["git", "diff", "--quiet", "HEAD", "--", f], cwd=ROOT).returncode
    check(not later and dirty == 0, "%s unchanged since Session 94" % f)

s94 = {r["corpus"].split(" (")[0]: r["subjecthood_rate_pct"] for r in json.load(
    open(ROOT / "works/2026-09-21-three-other-offices/inspection.json"))["rows"]}
mine = json.load(open(H / "inspection.json"))["rows"]
for k, v in s94.items():
    check(mine[k]["immediate_pct"] == v, "immediate rate for %s = %.2f, Session 94 published %.2f"
          % (k, mine[k]["immediate_pct"], v))
r = json.load(open(H / "results.json"))
check(mine["14 CFR F+G"]["immediate_pct"] == r["subjecthood"]["narrow"]["subjecthood_rate_pct"],
      "immediate rate for 14 CFR equals tonight's subjecthood")

man = json.load(open(H / "sources" / "MANIFEST.json"))["rows"][0]
raw = gzip.decompress((H / man["committed_as"]).read_bytes())
check(hashlib.sha256(raw).hexdigest() == man["sha256"], "committed title-14 XML hashes as the manifest says")

print("\nverify: %s" % ("all checks pass" if ok else "FAILURES"))
raise SystemExit(0 if ok else 1)
