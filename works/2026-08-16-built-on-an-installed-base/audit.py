#!/usr/bin/env python3
"""
audit.py -- turn the honest-cost anecdote into a count.

S26 found that this line had re-minted a concept the field already owned, and wrote it
up as an honest cost. S59 found the same thing again, for 'installed base'. Twice is a
pattern and a pattern can be measured, so this reads the corpus rather than my memory.

For each term in register.json it reports, off journal/ and works/:
  - how often the line writes it, and in how many files
  - the first file that writes it, and that file's date
  - whether the owner of the term is named anywhere in that same file
    (the crude credited-at-first-use test; see the caveat below)
  - the debt interval: how old the term already was when this line first wrote it

Deterministic, stdlib only, no network. Everything dated 2026-08-16 is excluded -- this
work's directory AND tonight's journal entry. Both argue about the vocabulary and both
write every term in the register, so counting them would be counting the argument as
its own evidence. The first draft excluded only the directory, which was fine until the
journal entry existed and then silently inflated every count on re-run. Anyone re-running
this after tonight gets the same numbers work.md reports; that is the point of the rule.

CAVEAT ON THE CREDIT TEST, stated here because it is the instrument's weak point.
Surname-in-same-file is a generous test: it can pass on a file that names Star for an
unrelated reason. It is generous on purpose. A generous test that still returns
'uncredited' is worth more than a strict one that does, and every failure it reports
is therefore a floor, not an estimate.

Word boundaries matter and the first draft did not have them: 'closure' matched inside
'disclosure' and reported a first use twelve days too early, in a file about
sequential disclosure of an animation. Fixed with \\b, and recorded in the journal,
because a substring match is a measurement of nothing that looks like a measurement of
something -- which is the same failure S57 logged with the tab-split.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
THIS_WORK = os.path.basename(HERE)
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
TONIGHT = "2026-08-16"
# works/INDEX.md is a catalogue OF this corpus, not part of it: it restates every work in
# a row of its own, so a term is counted again for each work described, and tonight's row
# would count this argument as its own evidence. Excluded on that ground, which is about
# double-counting and not only about tonight.
AGGREGATORS = {os.path.join("works", "INDEX.md")}


def corpus():
    """Every markdown file in journal/ and works/, minus tonight's own directory."""
    out = []
    for sub in ("journal", "works"):
        base = os.path.join(ROOT, sub)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d != THIS_WORK]
            for fn in filenames:
                if not fn.endswith(".md"):
                    continue
                path = os.path.join(dirpath, fn)
                rel = os.path.relpath(path, ROOT)
                m = DATE_RE.search(rel)
                if m and m.group(1) == TONIGHT:
                    continue
                if rel in AGGREGATORS:
                    continue
                out.append({
                    "rel": rel,
                    "date": m.group(1) if m else None,
                    "text": open(path, encoding="utf-8", errors="replace").read(),
                })
    # undated files (genealogie.md, parry-problem.md, the Fehlerkataster) sort last:
    # they carry no date in the path, so they cannot establish a first use. They are
    # still counted in the totals. Stated rather than silently dropped.
    out.sort(key=lambda f: (f["date"] is None, f["date"] or "", f["rel"]))
    return out


def audit(term, files):
    pat = re.compile(r"\b" + term["pattern"] + r"\b", re.I)
    hits, first = [], None
    for f in files:
        found = pat.findall(f["text"])
        if not found:
            continue
        hits.append({"file": f["rel"], "date": f["date"], "n": len(found)})
        if first is None and f["date"] is not None:
            m = pat.search(f["text"])
            s, e = max(0, m.start() - 170), min(len(f["text"]), m.end() + 170)
            ctx = " ".join(f["text"][s:e].split())
            credited = [k for k in term["credit_markers"]
                        if re.search(r"\b" + re.escape(k) + r"\b", f["text"], re.I)]
            first = {
                "file": f["rel"],
                "date": f["date"],
                "context": ctx,
                "credit_markers_present": credited,
                "credited_at_first_use": bool(credited),
            }

    fy = term["field"].get("year")
    debt = None
    if first and fy:
        debt = int(first["date"][:4]) - fy

    return {
        "term": term["term"],
        "verdict": term["verdict"],
        "line_sense": term["line_sense"],
        "field_owner": term["field"].get("owner"),
        "field_year": fy,
        "total_occurrences": sum(h["n"] for h in hits),
        "files_containing": len(hits),
        "first_use": first,
        "years_old_when_first_written_here": debt,
        "files": hits,
    }


def main():
    reg = json.load(open(os.path.join(HERE, "register.json"), encoding="utf-8"))
    files = corpus()
    rows = [audit(t, files) for t in reg["terms"]]

    dated = [f for f in files if f["date"]]
    results = {
        "measured": "2026-08-16, Session 59",
        "corpus": {
            "files": len(files),
            "dated_files": len(dated),
            "undated_files": len(files) - len(dated),
            "earliest": dated[0]["date"],
            "latest": dated[-1]["date"],
            "excluded": f"everything dated {TONIGHT} (works/{THIS_WORK}/ and "
                        f"journal/{TONIGHT}.md), plus works/INDEX.md as a catalogue of the "
                        f"corpus rather than part of it. All three restate the argument or "
                        f"the works; counting them would count the argument as its own "
                        f"evidence.",
        },
        "terms": rows,
    }
    json.dump(results, open(os.path.join(HERE, "results.json"), "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)

    print(f"corpus: {len(files)} markdown files, {dated[0]['date']} .. {dated[-1]['date']}"
          f" ({len(files) - len(dated)} undated, counted but never first)\n")
    hdr = f"{'term':<26}{'verdict':<34}{'uses':>5}{'files':>6}  {'first':<12}{'cred':<6}{'age':>4}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        fu = r["first_use"]
        print(f"{r['term']:<26}{r['verdict']:<34}{r['total_occurrences']:>5}"
              f"{r['files_containing']:>6}  {(fu['date'] if fu else '-'):<12}"
              f"{('yes' if fu and fu['credited_at_first_use'] else ('no' if fu else '-')):<6}"
              f"{(r['years_old_when_first_written_here'] if r['years_old_when_first_written_here'] is not None else '-'):>4}")

    used = [r for r in rows if r["first_use"]]
    unc = [r for r in used if not r["first_use"]["credited_at_first_use"]]
    print(f"\n{len(used)} of {len(rows)} register terms are actually written by this line.")
    print(f"{len(unc)} of those {len(used)} name nobody in the file that first writes them:"
          f" {', '.join(r['term'] for r in unc) or 'none'}")
    never = [r for r in rows if not r["first_use"]]
    print(f"{len(never)} are never written here: {', '.join(r['term'] for r in never) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
