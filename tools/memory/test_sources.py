#!/usr/bin/env python3
"""The index must see everywhere this practice writes.

The tool arrived here on 2026-08-12, ported from the atelier. It should have arrived with the
fork on 2026-08-10: Protocol v3, restored verbatim, names "the recall index" among the tools a
session carries between sessions, and the index was not carried across — `tools/` held only the
night validator. A constitution that names a tool the repository does not have sends every
session back to reading.

What there is to read: ~210,000 words inherited at the fork — 30 works, 46 research days, 21
error registers, the genealogy, both position papers — and the practice's position moved once,
at session 26, when it replaced "error is what method is made of" with error as a special case
of the epistemic thing. A night that argues against the standing position without knowing it is
a real error.

And the proof, in the first person and two days old: session 44 got its own session number
wrong, because it read the number out of prose instead of deriving it, and built
`tools/sessions.py` in response. That is what a missing memory looks like from inside.

This test guards the half a tool cannot: **does the index still point at the places this
repository actually keeps its records.** In the sibling houses the tool never broke — it kept
working perfectly on a corpus that no longer held the work.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cli import SOURCE_GLOBS, _collect_source_files

REPO_ROOT = Path(__file__).resolve().parents[2]

# This practice keeps two. A night makes a work and writes a research day; there is no
# work-line machinery here and no third place. A new one is added in the same commit that
# starts writing to it.
RECORD_DIRS = ["journal", "works"]

NOT_RECORDS = {
    "archive": "the superseded protocols, kept unchanged; recall should return the live text",
    "feedback": "build letters from the site gate, empty so far",
    "governance": "delegation documents, read directly and rarely",
    "memory": "the index itself, which is derived and gitignored",
    "tools": "code",
}


def _covered(rel_dir: str) -> bool:
    return any(glob.startswith(f"{rel_dir}/") for glob in SOURCE_GLOBS)


def test_every_record_directory_is_indexed() -> None:
    missing = [d for d in RECORD_DIRS if (REPO_ROOT / d).is_dir() and not _covered(d)]
    assert not missing, (
        f"these directories hold records but no SOURCE_GLOBS entry reaches them: {missing}. "
        "A session cannot recall what is not indexed, so it reads the whole record instead."
    )


def test_no_record_directory_is_silently_unindexed() -> None:
    unaccounted = []
    for entry in sorted(REPO_ROOT.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        if entry.name in RECORD_DIRS or entry.name in NOT_RECORDS:
            continue
        if not any(entry.rglob("*.md")):
            continue
        unaccounted.append(entry.name)
    assert not unaccounted, (
        f"top-level directories holding markdown are neither indexed nor declared non-records: "
        f"{unaccounted}. Add each to RECORD_DIRS (and SOURCE_GLOBS) or to NOT_RECORDS."
    )


def test_the_inherited_record_is_reachable() -> None:
    """The 30 works and 46 research days the fork inherited must be queryable, not readable."""
    indexed = {p.resolve() for p in _collect_source_files(REPO_ROOT)}
    works = {p.resolve() for p in (REPO_ROOT / "works").rglob("*.md")}
    days = {p.resolve() for p in (REPO_ROOT / "journal").rglob("*.md")}
    assert works & indexed, "no inherited work is indexed"
    assert days & indexed, "no research day is indexed"


def test_tools_v3_names_but_this_repo_lacks_are_declared_in_the_fork_note() -> None:
    """v3 was restored verbatim from a repository that had more tools than this one.

    The restored body names the recall index, `atlas/` and `pulse/`. Only the first was brought
    across. The v3 text is not edited to fix that — it is restored verbatim on purpose, and
    rewriting it would falsify the restoration. Instead the fork note above it declares what did
    and did not come, so a session is not sent looking for a directory that is not there.

    So the check is not "the constitution never names an absent tool". It is: **anything it
    names and this repository lacks is accounted for in the fork note.**
    """
    # Whitespace is normalised before searching. Markdown wraps prose at ~95 columns, so any
    # phrase long enough to be unambiguous is also long enough to straddle a newline — and a
    # line-based search then reports "missing" for text that is plainly there. That false
    # negative was hit three times in one night while this work was being done, twice against
    # this repository's own constitutions.
    text = re.sub(r"\s+", " ", (REPO_ROOT / "PROTOCOL.md").read_text(encoding="utf-8"))
    marker = "What the restoration actually carried, and what it did not"
    note, _, rest = text.partition(marker)
    declaration = rest[:2500]
    undeclared = []
    for name in ("atlas/", "pulse/"):
        if name not in text:
            continue
        if (REPO_ROOT / name.rstrip("/")).exists():
            continue
        if not rest or f"`{name}`" not in declaration:
            undeclared.append(name)
    assert not undeclared, (
        f"PROTOCOL.md names tools this repository does not have, and the fork note does not "
        f"account for them: {undeclared}. Either bring them across, or say in the fork note "
        "that they were not carried and why — a promise the repository cannot keep costs a "
        "session the time it spends looking."
    )
