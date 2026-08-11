#!/usr/bin/env python3
"""The gate's check, written for the protocol this repository actually runs.

The auto-land workflow was copied from the parent repo, where gate 5 runs
`tools/validate_v4_projects.py` against the branch tree. That validator checks v4 project
records — SCORE.md, mandate_check, disposition — and this line has none: it works under
Research Protocol v3, where a night produces a work directory or a reading entry. The file
was never copied either, so the gate refused every branch with `refused_validation` and a
Python "no such file" three lines above it.

So this is the v3 check, and it asks only what v3 asks:

  * a work directory carries `meta.json` with title, date, author, medium, embodies, all
    non-empty — that list is the protocol's, not this file's invention;
  * the date in the metadata matches the date in the directory name, because the record is
    sorted and counted by that name everywhere it is read;
  * the work is actually there: `work.md` or `index.html`;
  * `works/INDEX.md` names the directory, or the register silently loses it;
  * the night has a journal entry, because both outcomes v3 allows end in one.

It checks the tree it is pointed at, prints every failure rather than the first, and exits
non-zero if any work fails. A night that reads rather than builds adds no work directory and
passes here with nothing to say — which is correct: reading is a full outcome.

    python3 tools/validate_v3_night.py [tree]
"""
import json
import os
import re
import sys

WORK_FIELDS = ("title", "date", "author", "medium", "embodies")
# Every form this line has used for the work itself. The record holds all four: `work.astro`
# and `index.html` from the first run, `work.md` since the fork. A gate that knew only the
# newest of them would call thirty inherited works empty.
WORK_FORMS = ("work.md", "index.html", "work.astro", "index.astro")
DATED_DIR = re.compile(r"^(\d{4}-\d{2}-\d{2})-")


def check_work(root, slug, index_text):
    """Return a list of complaints about one work directory. Empty means it passes."""
    bad = []
    where = os.path.join(root, "works", slug)
    meta_path = os.path.join(where, "meta.json")

    if not os.path.exists(meta_path):
        return [f"{slug}: no meta.json"]
    try:
        with open(meta_path, encoding="utf-8") as fh:
            meta = json.load(fh)
    except (OSError, ValueError) as err:
        return [f"{slug}: meta.json does not parse ({err})"]

    for field in WORK_FIELDS:
        value = meta.get(field)
        if not isinstance(value, str) or not value.strip():
            bad.append(f"{slug}: meta.json has no non-empty {field!r}")

    named = DATED_DIR.match(slug)
    if named and meta.get("date") != named.group(1):
        bad.append(f"{slug}: meta.json date {meta.get('date')!r} is not the directory's {named.group(1)!r}")

    if not any(os.path.exists(os.path.join(where, f)) for f in WORK_FORMS):
        bad.append(f"{slug}: none of {', '.join(WORK_FORMS)} — nothing to read")

    if slug not in index_text:
        bad.append(f"{slug}: works/INDEX.md does not name it")

    if named:
        day = named.group(1)
        journal = os.path.join(root, "journal")
        entries = os.listdir(journal) if os.path.isdir(journal) else []
        if not any(e.startswith(day) and e.endswith(".md") for e in entries):
            bad.append(f"{slug}: no journal entry for {day}")

    return bad


def main(root, only=None):
    """`only` scopes the check to named work directories — what a branch changed.

    A gate judges the change in front of it, not the record behind it. Three works from the
    first week of July carry no `author` and no `medium`; the practice's metadata conventions
    firmed up after them. Failing tonight's branch for that would be a gate that can never open
    again, so the workflow passes the slugs the branch touched and the rest stands as history.
    """
    works = os.path.join(root, "works")
    if not os.path.isdir(works):
        print("no works/ directory — nothing to validate")
        return 0

    index_path = os.path.join(works, "INDEX.md")
    index_text = ""
    if os.path.exists(index_path):
        with open(index_path, encoding="utf-8") as fh:
            index_text = fh.read()
    else:
        print("works/INDEX.md is missing — every work will fail its register check", file=sys.stderr)

    failures = []
    checked = 0
    for slug in sorted(os.listdir(works)):
        if not os.path.isdir(os.path.join(works, slug)):
            continue
        if only and slug not in only:
            continue
        checked += 1
        failures.extend(check_work(root, slug, index_text))

    for line in failures:
        print(f"FAIL {line}", file=sys.stderr)
    print(f"validate_v3_night: {checked} work(s) checked, {len(failures)} complaint(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    scope = None
    if "--only" in args:
        cut = args.index("--only")
        scope = set(args[cut + 1:])
        args = args[:cut]
    sys.exit(main(args[0] if args else ".", scope))
