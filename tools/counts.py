#!/usr/bin/env python3
"""counts.py -- recompute the numbers this record publishes in prose.

Session 90 went to write "sixteen rows stand" into a journal entry, counted instead, and found 25.
The published figure had tracked the mechanical one exactly until 2026-09-03 and drifted for eleven
nights afterwards. F-143 says why that is worse than an ordinary slip: this line verifies its
measurements adversarially and **a summary sentence is on none of those paths**. Session 90's open
thread 5 asked for a small tool that recomputes the countable ones from the files.

This is that tool. It does not repair anything and it never edits a file. It counts, prints, and
exits non-zero if a published number and a counted one disagree.

    python3 tools/counts.py [--session N]

What it checks:

  works       -- dated directories under works/ against the rows of works/INDEX.md
  falsifiers  -- rows of the Standing table in works/FALSIFIERS.md, open and closed
  position    -- the "unchanged for N nights" sentence in the journal, whose offset from the
                 session number must be constant; the tool reports the value the next night owes
  journal     -- defers to tools/sessions.py for the session number itself

Every count is a count of files in this repository, so a disagreement is always this record's and
never the world's.
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
    "eighty": 80, "ninety": 90,
}
DATED = re.compile(r"^\d{4}-\d{2}-\d{2}-")

problems = []


def spelled(text):
    """'forty-three' -> 43.  Returns None if the string is not a spelled number."""
    parts = text.lower().replace("–", "-").split("-")
    if not parts or any(p not in WORDS for p in parts):
        return None
    return sum(WORDS[p] for p in parts)


def say(ok, name, detail):
    print("  %-4s %-26s %s" % ("ok" if ok else "DIFF", name, detail))
    if not ok:
        problems.append(name)


def works():
    dirs = sorted(p.name for p in (ROOT / "works").iterdir()
                  if p.is_dir() and DATED.match(p.name))
    index = (ROOT / "works" / "INDEX.md").read_text(encoding="utf-8")
    named = [d for d in dirs if d in index]
    missing = [d for d in dirs if d not in index]
    say(not missing, "works directories",
        "%d dated directories, %d named in INDEX.md%s"
        % (len(dirs), len(named), "" if not missing else "; MISSING: " + ", ".join(missing)))
    rows = re.findall(r"^\|\s*(\d+)\s*\|", index, re.M)
    nums = [int(r) for r in rows]
    # Reported, never failed: Session 90 found row 72 standing below 73-75 from an earlier append
    # and left it there, because this record accumulates rather than being tidied after the fact.
    # Row order is not a count, so a tool about counts does not get to fail on it.
    print("  ---- %-21s %d numbered rows, highest %s, %s"
          % ("INDEX.md row order", len(nums), max(nums) if nums else "-",
             "in order" if nums == sorted(nums) else "OUT OF ORDER (recorded, not repaired)"))
    return len(dirs)


def falsifiers():
    text = (ROOT / "works" / "FALSIFIERS.md").read_text(encoding="utf-8")
    standing = text.split("## Standing", 1)
    if len(standing) < 2:
        say(False, "falsifier table", "no '## Standing' heading found")
        return
    body = standing[1]
    body = body.split("\n## ", 1)[0]
    ids = re.findall(r"^\|\s*\*\*([A-Z0-9._-]+)\*\*\s*\|", body, re.M)
    rows = [ln for ln in body.splitlines() if re.match(r"^\|\s*\*\*[A-Z0-9._-]+\*\*\s*\|", ln)]
    # An outcome, not only a check.  Until 2026-09-21 this line counted "checked" alone, because
    # every row that had ever left the open state had left it that way; Session 94 falsified
    # S91.RULEBOUND and the counter could not see it -- a category set fixed before the event it
    # had to count.  Widened here, with the reason attached rather than quietly.  (F-152)
    OUTCOME = ("checked", "falsified", "resolved")
    closed = sum(1 for ln in rows
                 if any(w in ln.lower().split("|")[-2].lower() for w in OUTCOME))
    print("  ---- %-21s %d rows: %d with an outcome in the status cell, %d without"
          % ("falsifier table", len(rows), closed, len(rows) - closed))
    print("       ids: %s" % ", ".join(ids))
    # A published tally, if any night wrote one into this file.  The LAST one, not the first:
    # this record accumulates and never retouches an earlier sentence, so an older tally is
    # correct about the file as it then stood and the newest is the one that claims today.
    tallies = list(re.finditer(r"\*\*(\d+) rows: (\d+) open, (\d+) closed\.?\*\*", text))
    if tallies:
        tot, op, cl = (int(x) for x in tallies[-1].groups())
        say(tot == len(rows) and cl == closed, "the newest published tally",
            "file says %d rows (%d open, %d closed); the table holds %d (%d with an outcome), "
            "and %d earlier %s as its night wrote it"
            % (tot, op, cl, len(rows), closed, len(tallies) - 1,
               "tally stands" if len(tallies) == 2 else "tallies stand"))
    return len(rows)


def position(session):
    """The 'unchanged for N nights' sentence: its offset from the session number must be constant."""
    seen = []
    for p in sorted((ROOT / "journal").glob("*.md")):
        t = p.read_text(encoding="utf-8")
        s = re.search(r"\(Session\s+(\d+)\)", t)
        n = re.search(r"unchanged for \*\*([a-z-]+) nights?\*\*", t, re.I)
        if s and n:
            v = spelled(n.group(1))
            if v is not None:
                seen.append((int(s.group(1)), v, p.name))
    if not seen:
        say(False, "position nights", "no journal states one")
        return None
    offsets = {s - v for s, v, _ in seen[-8:]}
    ok = len(offsets) == 1
    off = sorted(offsets)[0]
    say(ok, "position nights",
        "%d journals state it; last eight give offset%s %s%s"
        % (len(seen), "" if ok else "S", sorted(offsets),
           "" if not session else " -- Session %d owes %d" % (session, session - off)))
    if not ok:
        for s, v, f in seen[-8:]:
            print("       %-22s session %3d, %2d nights, offset %d" % (f, s, v, s - v))
    return None if not ok else session - off if session else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", type=int, default=None,
                    help="the session about to be written; reports what it owes")
    a = ap.parse_args()
    print("counts.py -- numbers this record publishes in prose, recomputed from the files\n")
    works()
    falsifiers()
    position(a.session)
    print("\n  %s" % ("all counted numbers agree with the published ones"
                      if not problems else "DISAGREEMENTS: " + ", ".join(problems)))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
