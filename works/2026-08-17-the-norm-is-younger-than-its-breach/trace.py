#!/usr/bin/env python3
"""trace.py — date this practice's norms against the breakdowns they answer.

The question is Simondon's, at MEOT p. 202-203: technical thought does not separate from the
technical act until the act fails. *L'echec du geste technique dephase l'acte technique en deux
realites opposees* — a figural reality of learned schemas, and a ground of the world the gesture
is applied to. Before the failure there is no standing-apart from which anything could be judged.

If that describes this practice, then the positions from which it judges its own nights should be
younger than the breakdowns that produced them, and datably so. This script does the mechanical
half of the check: it fixes the populations, extracts them without selection, and traces each
item forward through the record. The adjudication is in work.md and is signed, not automated.

Two directions:

  A  norm -> breakdown.  Every instrument in tools/, every check the gate performs, every bullet
     under PROTOCOL.md's Prohibitions. For each, the record's own earliest mention, dated.
  B  breakdown -> norm.  Every numbered entry in works/fehlerkataster-*.md. For each, whether
     anything later in the record refers to it at all.

Direction B's test was, in its first version, deliberately generous in the manner of 2026-08-16's
audit: an entry counted as traced if its bare identifier appeared anywhere dated later than the
file that introduced it. That version returned `inert: 0` for all 42 headings — a measurement
carrying no information, because the register takes attendance in every journal of its era. The
fault and its repair are documented at `afterlife()` and the discarded version is in the night's
journal; the live test scores a mention by how many identifiers share its line.

stdlib only, no network, deterministic. Excludes this work's own directory *and everything dated on
or after this night* from the corpus, on 2026-08-16's lesson: a corpus that contains a catalogue of
itself counts its own argument as its evidence, and the fault is invisible while it is static. The
directory exclusion was written first and was not enough — tonight's journal entry names F-022 and
would have added a post-fork trace to an entry this work reports as untouched since the fork. Same
fault, one file over.

    python3 trace.py [repo-root]   ->  results.json beside this file
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SELF = os.path.basename(HERE)

DATED = re.compile(r"(\d{4}-\d{2}-\d{2})")
TONIGHT = "2026-08-17"   # nothing this night wrote may be evidence for what this night claims
ENTRY = re.compile(r"^#{2,3}\s*(F-\d{3})\b(.*)$", re.M)
REF = re.compile(r"\bF-(\d{3})\b")


# ---------------------------------------------------------------- corpus

def corpus(root):
    """Every markdown file in the record, minus this work's own directory.

    Returns [(path, date-or-None)] where the date is taken from the filename when the filename
    carries one, and otherwise from the directory name. Files with neither are kept and dated
    None: they can never establish an ordering, and saying so is better than dropping them.
    """
    out = []
    for base in ("journal", "works"):
        for dirpath, dirnames, filenames in os.walk(os.path.join(root, base)):
            dirnames[:] = [d for d in dirnames if d != SELF]
            if os.path.basename(dirpath) == SELF:
                continue
            for fn in sorted(filenames):
                if not fn.endswith(".md"):
                    continue
                path = os.path.join(dirpath, fn)
                m = DATED.search(fn) or DATED.search(os.path.basename(dirpath))
                if m and m.group(1) >= TONIGHT:
                    continue
                out.append((os.path.relpath(path, root), m.group(1) if m else None))
    for fn in ("PROTOCOL.md", "README.md", "REQUESTS.md"):
        p = os.path.join(root, fn)
        if os.path.exists(p):
            out.append((fn, None))
    return sorted(out)


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------- direction A: the norms

def instruments(root):
    """Every instrument in tools/, with its first commit date from git.

    An instrument is a .py file that is not a test and not a package helper: the population is
    the directory's contents, not a shortlist. tools/memory/ is one instrument, not eight files,
    and is reported under its entry point.
    """
    found = []
    for dirpath, _dirnames, filenames in os.walk(os.path.join(root, "tools")):
        for fn in sorted(filenames):
            if not fn.endswith(".py") or fn.startswith("test_"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            found.append(rel)
    keep = [f for f in found if "/memory/" not in f]
    mem = [f for f in found if f.endswith("memory/cli.py")]
    return sorted(keep + mem)


def first_commit(root, rel):
    try:
        out = subprocess.run(
            ["git", "-C", root, "log", "--diff-filter=A", "--format=%ad", "--date=short", "--", rel],
            capture_output=True, text=True, check=True).stdout.split()
        return out[-1] if out else None
    except (subprocess.CalledProcessError, OSError):
        return None


def mentions(root, needle, files):
    """Every dated file in the corpus naming `needle`, earliest first."""
    hits = []
    for rel, date in files:
        if needle in read(root, rel):
            hits.append({"file": rel, "date": date})
    hits.sort(key=lambda h: (h["date"] is None, h["date"] or "", h["file"]))
    return hits


def gate_checks(root):
    """The checks tools/validate_v3_night.py actually performs, read off its source.

    Each required metadata field is one norm; the four structural checks are one each. Extracted
    from the file rather than transcribed, so the population cannot drift from the gate.
    """
    src = read(root, "tools/validate_v3_night.py")
    fields = re.search(r"WORK_FIELDS\s*=\s*\(([^)]*)\)", src)
    names = re.findall(r"\"([a-z]+)\"", fields.group(1)) if fields else []
    checks = [f"meta.json carries a non-empty {n!r}" for n in names]
    checks += [
        "the metadata date equals the directory's date",
        "one of work.md / index.html / work.astro / index.astro exists",
        "works/INDEX.md names the directory",
        "the night has a journal entry",
    ]
    return checks


def prohibitions(root):
    """Every bullet under PROTOCOL.md's '## Prohibitions' heading, verbatim."""
    src = read(root, "PROTOCOL.md")
    block = re.search(r"^## Prohibitions\s*\n(.*?)(?=^## )", src, re.M | re.S)
    if not block:
        return []
    items, cur = [], None
    for line in block.group(1).splitlines():
        if line.startswith("- "):
            if cur:
                items.append(" ".join(cur.split()))
            cur = line[2:]
        elif cur is not None and line.strip():
            cur += " " + line.strip()
    if cur:
        items.append(" ".join(cur.split()))
    return items


# ------------------------------------------------ direction B: the register

def register(root):
    """Every numbered entry in works/fehlerkataster-*.md, in file order."""
    entries = []
    wdir = os.path.join(root, "works")
    for fn in sorted(os.listdir(wdir)):
        if not (fn.startswith("fehlerkataster-") and fn.endswith(".md")):
            continue
        rel = os.path.join("works", fn)
        text = read(root, rel)
        head = DATED.search(text)
        for m in ENTRY.finditer(text):
            entries.append({
                "id": m.group(1),
                "heading": " ".join(m.group(2).split())[:180],
                "source": rel,
                "source_date": head.group(1) if head else None,
            })
    return entries


ROLL_CALL = 3   # identifiers on one line, at or above which the line is a status list

FORK = "2026-08-10"


def afterlife(root, entries, files):
    """For each entry: where it is named later, and whether it is ever *used* rather than listed.

    The first version of this function counted any later mention as a trace and returned
    `inert: 0` for all 42 entries — a measurement with no information in it. The reason is in
    `journal/2026-07-10.md` line 244, which reads "Error count (after Session 21): active F-021,
    F-022 ..., F-035" and names eleven identifiers in one line. That is the register taking
    attendance, not the register doing work, and it was carrying most of the verdicts.

    So a mention is scored by the line it sits on. A line naming ROLL_CALL or more identifiers is
    a status list; a line naming one or two is the entry being reasoned with. The threshold is a
    judgement and it is the one number in this instrument that is not read off the corpus —
    `sweep_threshold` in results.json reports the verdict counts at 2, 3, 4 and 5 so a reader can
    see how much the finding depends on it.

    Also recorded: whether the entry is named anywhere dated on or after the fork (2026-08-10),
    which is the boundary this repository's own git history begins at.
    """
    where = {}
    for rel, date in files:
        for line in read(root, rel).splitlines():
            found = set(REF.findall(line))
            if not found:
                continue
            for num in found:
                where.setdefault("F-" + num, []).append(
                    {"file": rel, "date": date, "density": len(found)})
    out = []
    for e in entries:
        hits = [h for h in where.get(e["id"], []) if h["file"] != e["source"]]
        later = [h for h in hits if h["date"] and e["source_date"] and h["date"] > e["source_date"]]
        worked = [h for h in later if h["density"] < ROLL_CALL]
        post = sorted({h["file"] for h in hits if h["date"] and h["date"] >= FORK})
        if worked:
            verdict = "worked"
        elif later:
            verdict = "listed"
        elif hits:
            verdict = "same-day-only"
        else:
            verdict = "inert"
        out.append({
            **e,
            "later_files": sorted({h["file"] for h in later}),
            "worked_in": sorted({h["file"] for h in worked}),
            "post_fork": post,
            "verdict": verdict,
        })
    return out


def sweep(root, entries, files, thresholds=(2, 3, 4, 5)):
    """The same count at four thresholds, so the reader can price the one judgement in here."""
    global ROLL_CALL
    keep, out = ROLL_CALL, {}
    for t in thresholds:
        ROLL_CALL = t
        counts = {}
        for e in afterlife(root, entries, files):
            counts[e["verdict"]] = counts.get(e["verdict"], 0) + 1
        out[str(t)] = counts
    ROLL_CALL = keep
    return out


# ---------------------------------------------------------------- main

def main(root):
    files = corpus(root)
    tools = []
    for rel in instruments(root):
        name = os.path.basename(rel) if "/memory/" not in rel else "memory/cli.py"
        tools.append({
            "instrument": rel,
            "first_commit": first_commit(root, rel),
            "named_in": mentions(root, name, files)[:6],
        })

    entries = register(root)
    traced = afterlife(root, entries, files)
    counts = {}
    for t in traced:
        counts[t["verdict"]] = counts.get(t["verdict"], 0) + 1

    # Four identifiers carry two headings each: the register updates an entry in a later file
    # rather than opening a new number. Rolled up to the identifier, an entry takes the strongest
    # verdict any of its headings earned, so an entry revisited and then reasoned with counts once.
    rank = {"inert": 0, "same-day-only": 1, "listed": 2, "worked": 3}
    best = {}
    for t in traced:
        if rank[t["verdict"]] > rank.get(best.get(t["id"], "inert"), 0):
            best[t["id"]] = t["verdict"]
    by_entry = {}
    for v in best.values():
        by_entry[v] = by_entry.get(v, 0) + 1

    # Simondon's sentence names two registers born at the same break: the theoretical and the
    # normative. They can be counted separately. Norm-bearing artefacts are the ones that
    # constrain a later night; theory-bearing artefacts are the ones that state what this
    # practice holds. Both lists are named here rather than inferred, and both are complete.
    norm_bearing = ["PROTOCOL.md", "README.md"] + instruments(root) + ["pulse/vital-signs.json",
                                                                      "pulse/rhizome.json"]
    theory_bearing = ["works/genealogie.md", "works/parry-problem.md"] + sorted(
        os.path.join("works", f) for f in os.listdir(os.path.join(root, "works"))
        if f.startswith("position-") and f.endswith(".md"))
    def cite_count(rels):
        out = {}
        for rel in rels:
            if os.path.exists(os.path.join(root, rel)):
                out[rel] = len(set(REF.findall(read(root, rel))))
        return out
    registers = {
        "normative": cite_count(norm_bearing),
        "theoretical": cite_count(theory_bearing),
    }
    cites = [k for k, v in registers["normative"].items() if v]

    result = {
        "corpus_files": len(files),
        "direction_A": {
            "instruments": tools,
            "gate_checks": gate_checks(root),
            "prohibitions": prohibitions(root),
        },
        "direction_B": {
            "entries": len(entries),
            "register_files": len({e["source"] for e in entries}),
            "counts_by_heading": counts,
            "distinct_entries": len(best),
            "counts_by_entry": by_entry,
            "roll_call_threshold": ROLL_CALL,
            "sweep_threshold": sweep(root, entries, files),
            "worked_share_by_entry": round(by_entry.get("worked", 0) / len(best), 3) if best else None,
            "reached_after_the_fork": sorted({e["id"] for e in traced if e["post_fork"]}),
            "norm_artefacts_citing_the_register": cites,
            "two_registers": registers,
            "detail": traced,
        },
    }
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    print(f"corpus: {len(files)} files (this work's directory and everything dated "
          f"{TONIGHT} excluded)")
    print(f"A: {len(tools)} instruments, {len(result['direction_A']['gate_checks'])} gate checks, "
          f"{len(result['direction_A']['prohibitions'])} prohibitions")
    print(f"B: {len(entries)} register entries in {result['direction_B']['register_files']} files")
    for k in sorted(counts):
        print(f"   {k:<14} {counts[k]:>3}")
    print(f"   {len(best)} distinct entries: " + ", ".join(f"{k}={v}" for k, v in sorted(by_entry.items())))
    print(f"   worked share {result['direction_B']['worked_share_by_entry']}")
    print(f"   post-fork reach: {len(result['direction_B']['reached_after_the_fork'])} of {len(entries)} entries")
    print(f"   norm artefacts citing the register: {cites or 'none'}")
    for kind, d in registers.items():
        print(f"   {kind:<12} distinct entries cited: "
              + ", ".join(f"{os.path.basename(k)}={v}" for k, v in d.items() if v) or "none")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..")))
