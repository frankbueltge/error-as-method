#!/usr/bin/env python3
"""What the sentence lets in — the mechanical half of Session 85.

Three measurements, in the order the pre-registration fixes them.

  1. RECONCILE. Every row of `candidates.json` names a source file and quotes it. Each quote must
     be found in that file byte for byte, ignoring nothing but Markdown emphasis marks, which the
     record uses inconsistently around the same sentence. A row whose quote is not there is a row
     I invented, and this script exits non-zero rather than printing a number.

  2. THE LEXICAL TEST. For each candidate I have written, by hand, its minimal admission form —
     the shortest wording of the standing sentence that would carry the claim. This script
     tokenises that form and reports which of its content words are absent from the standing
     sentence's own word list. The judgement is mine; the comparison is the machine's.

  3. THE AFTERLIFE. For each satellite, scan every journal entry and every work file dated after
     the night that minted it, for the keys fixed in `candidates.json`. Emit every context. The
     contexts are adjudicated by hand in `adjudication.json` into attendance or use, because
     Session 60's afterlife test returned `inert: 0` for 42 headings and meant nothing: it counted
     mentions, and every journal of that era takes attendance in one line.

Reads only committed files. Writes `results.json` and `afterlife.json`. Deterministic, stdlib
only, no network.

    python3 measure.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# This night's own date. An afterlife is what LATER nights did with a claim, and tonight is not a
# later night. The first version of this file excluded only this work's own directory, so the run
# that produced the published numbers was correct — and the moment the night's journal entry and
# position note existed on disk, a re-run counted them and returned different numbers for every
# claim (S84's structural zero became 17). An instrument whose population grows to include its own
# report is not reproducible, and it is the exact figure this practice studies: the observer
# entering the system it is measuring. Filed as F-127. Everything dated on or after tonight is out.
TONIGHT = "2026-09-09"

# The standing sentence, and the only word list the lexical test consults.
SENTENCE = ("Error is a special case of the epistemic thing — a difference onto which "
            "an observer has already imposed a norm.")

# Words that carry no claim on their own. Kept short and fixed here rather than tuned: a longer
# list would let me decide the result by deciding what counts as a content word.
FUNCTION_WORDS = {
    "a", "an", "the", "is", "are", "be", "been", "has", "have", "of", "to", "and", "or", "that",
    "which", "who", "it", "its", "in", "on", "at", "by", "for", "with", "as", "not", "no", "some",
    "this", "these", "one", "two", "more", "need", "can", "must", "where", "when", "what",
}

WORD = re.compile(r"[a-z]+")
EMPHASIS = re.compile(r"[*_`]")
DATED = re.compile(r"(\d{4}-\d{2}-\d{2})")


def content_words(text):
    """The content words of a passage, lowercased, in order of first appearance."""
    seen, out = set(), []
    for tok in WORD.findall(text.lower()):
        if tok in FUNCTION_WORDS or tok in seen:
            continue
        seen.add(tok)
        out.append(tok)
    return out


def flatten(text):
    """Drop Markdown emphasis so a quote matches however the record chose to bold it."""
    return EMPHASIS.sub("", text)


def record_files():
    """Every journal entry and every work file the afterlife scan may look at, with its date.

    A file's date is the date in its path — the record is sorted and counted by that everywhere
    it is read (tools/validate_v3_night.py says so, and this follows it rather than inventing a
    second rule). Files with no date in the path are scanned and dated None, which the scan then
    excludes from 'later than' comparisons rather than guessing.
    """
    out = []
    for base in ("journal", "works"):
        for dirpath, _dirs, names in os.walk(os.path.join(ROOT, base)):
            for name in sorted(names):
                if not name.endswith((".md", ".json")):
                    continue
                path = os.path.join(dirpath, name)
                rel = os.path.relpath(path, ROOT)
                found = DATED.search(rel)
                date = found.group(1) if found else None
                if date is not None and date >= TONIGHT:
                    continue  # tonight's own writing, in every file it lives in
                out.append((rel, date))
    return sorted(out)


def reconcile(rows):
    """Complaint list. Empty means every quote is where its row says it is."""
    bad = []
    for row in rows:
        if row["verdict"] == "excluded" and row["minimal_admission_form"] is None:
            pass  # excluded rows still carry a quote and are still checked
        path = os.path.join(ROOT, row["source"])
        if not os.path.exists(path):
            bad.append(f"{row['id']}: no such file {row['source']}")
            continue
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        if flatten(row["quote"]) not in flatten(text):
            bad.append(f"{row['id']}: quote not found in {row['source']}")
    return bad


def lexical(rows, sentence_words):
    """The lexical test, one row at a time."""
    out = []
    for row in rows:
        form = row["minimal_admission_form"]
        if form is None:
            out.append({**{k: row[k] for k in ("id", "population", "session", "verdict",
                                               "verdict_word", "sharpens_word")},
                        "new_words": None, "tested": False})
            continue
        new = [w for w in content_words(form) if w not in sentence_words]
        out.append({**{k: row[k] for k in ("id", "population", "session", "verdict",
                                           "verdict_word", "sharpens_word")},
                    "new_words": new, "n_new": len(new), "tested": True})
    return out


def afterlife(satellites, files):
    """Every context, in every file dated after the minting night, matching any of a satellite's keys."""
    out = {}
    for sat in satellites:
        hits = []
        for rel, date in files:
            if date is None or date <= sat["minted"]:
                continue
            with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                lines = fh.read().splitlines()
            for n, line in enumerate(lines, 1):
                low = line.lower()
                matched = [k for k in sat["keys"] if k.lower() in low]
                if matched:
                    hits.append({"file": rel, "date": date, "line": n,
                                 "keys": matched, "text": line.strip()[:400]})
        out[sat["id"]] = {"name": sat["name"], "row": sat["row"], "minted": sat["minted"],
                          "minted_session": sat["minted_session"], "keys": sat["keys"],
                          "n_contexts": len(hits), "n_files": len({h["file"] for h in hits}),
                          "contexts": hits}
    return out


def load(readings, sentence_words):
    """How many distinct fixed readings each word of the sentence carries, and which.

    The sentence's words never changed, so every night that added something to it had to add it
    to what one of its words means. This counts that.
    """
    per = {}
    for r in readings:
        if r["word"] not in sentence_words:
            sys.exit(f"readings.json fixes a reading on {r['word']!r}, which is not in the sentence")
        per.setdefault(r["word"], []).append(
            {"session": r["session"], "date": r["date"], "reading": r["reading"]})
    return {w: sorted(v, key=lambda x: x["session"]) for w, v in
            sorted(per.items(), key=lambda kv: (-len(kv[1]), kv[0]))}


def main():
    with open(os.path.join(HERE, "candidates.json"), encoding="utf-8") as fh:
        census = json.load(fh)
    with open(os.path.join(HERE, "readings.json"), encoding="utf-8") as fh:
        readings = json.load(fh)["readings"]
    rows = census["candidates"]

    if census["_sentence"] != SENTENCE:
        sys.exit("the sentence in candidates.json is not the sentence in this file — stop")

    bad = reconcile(rows) + reconcile([
        {"id": f"reading:{r['word']}:S{r['session']}", "source": r["source"],
         "quote": r["quote"], "verdict": "reading", "minimal_admission_form": None}
        for r in readings])
    if bad:
        for line in bad:
            print("RECONCILE:", line)
        sys.exit(1)

    sentence_words = set(content_words(SENTENCE))
    lex = lexical(rows, sentence_words)

    files = record_files()
    after = afterlife(census["satellites"], files)
    with open(os.path.join(HERE, "afterlife.json"), "w", encoding="utf-8") as fh:
        json.dump(after, fh, indent=1, ensure_ascii=True, sort_keys=True)
        fh.write("\n")

    # Three disjoint buckets. The first draft of these two lines used startswith("entered") for the
    # reading bucket, which swallowed the one row of the other kind and reported five readings where
    # there are four. Caught by reading the printed total against the census by hand; the rule this
    # line keeps is that a prefix match is not a category test.
    moved = [r for r in lex if r["verdict"] == "entered-the-sentence"]
    entered = [r for r in lex if r["verdict"] == "entered-the-reading"]
    outside = [r for r in lex if r["verdict"] == "outside"]

    results = {
        "_what": "Session 85's measurement. Reconciled against the record by measure.py; the "
                 "attendance/use verdicts live in adjudication.json and are hand-signed.",
        "sentence": SENTENCE,
        "sentence_content_words": sorted(sentence_words),
        "n_candidates": len(rows),
        "n_tested": sum(1 for r in lex if r["tested"]),
        "n_excluded": sum(1 for r in lex if not r["tested"]),
        "entered_the_sentence": len(moved),
        "entered_the_reading": len(entered),
        "outside": len(outside),
        "lexical": lex,
        "moved_the_sentence_with_new_words": [r["id"] for r in moved if r["tested"] and r["n_new"] > 0],
        "entered_with_new_words": [r["id"] for r in entered if r["tested"] and r["n_new"] > 0],
        "outside_with_no_new_words": [r["id"] for r in outside if r["tested"] and r["n_new"] == 0],
        "words_sharpened": sorted({r["sharpens_word"] for r in lex if r["sharpens_word"]}),
        "load": load(readings, sentence_words),
        "files_scanned": len(files),
        "afterlife_summary": {k: {"name": v["name"], "n_contexts": v["n_contexts"],
                                  "n_files": v["n_files"]} for k, v in sorted(after.items())},
    }
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=True, sort_keys=False)
        fh.write("\n")

    print(f"reconciled {len(rows)} rows against the record, all quotes found")
    print(f"tested {results['n_tested']}, excluded {results['n_excluded']}")
    print(f"entered the sentence : {results['entered_the_sentence']}  "
          f"(with new content words: {results['moved_the_sentence_with_new_words'] or 'none'})")
    print(f"entered the reading  : {results['entered_the_reading']}  "
          f"(with new content words: {results['entered_with_new_words'] or 'none'})")
    print(f"outside              : {results['outside']}  "
          f"(with no new content words: {results['outside_with_no_new_words'] or 'none'})")
    print(f"words given a fixed reading: {', '.join(results['words_sharpened'])}")
    print("the load on the sentence's own words:")
    for word, rs in results["load"].items():
        print(f"  {word:10s} {len(rs)} reading(s)  "
              f"[{', '.join('S%d' % r['session'] for r in rs)}]")
    print(f"scanned {len(files)} record files for the afterlife of {len(after)} claims")
    for key, val in sorted(after.items()):
        print(f"  {key:5s} {val['name']:24s} {val['n_contexts']:4d} contexts "
              f"in {val['n_files']:3d} files")


if __name__ == "__main__":
    main()
