#!/usr/bin/env python3
"""
probe.py — Session 63, 2026-08-20

Offline, deterministic, stdlib only. Run `harvest.py` first.

Three measurements, in the order the night made them:

  A. The book        — what Jones (2022) actually contains.
  B. The review      — where the phrase this practice used actually lives.
  C. This repository — how far it travelled once it was here.

Measurement C is taken against the commit this night was cut from, not the
working tree, so nothing written tonight can enter the count. The concern is
inherited from Session 59, which published a count inflated by its own argument
and corrected it downward; the mechanism is not, because Session 59's fix — an
exclusion list — is the one that failed here first (F-053).

Writes results.json.
"""

import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

PHRASE = "generative unknowing"

# The commit origin/main was at when this night was cut (tools/preflight.py, 0/0).
# Measurement C is taken against this tree state, never the working tree — see
# measure_repo() and F-053.
BASE = "9b28c29"


def flat(text):
    return re.sub(r"\s+", " ", text)


def whole_word(word, text):
    return len(re.findall(r"\b" + word + r"\b", text, re.I))


def measure_book():
    with open(os.path.join(SRC, "jones.txt")) as fh:
        raw = fh.read()
    pages = raw.split("\x0c")
    n = flat(raw)

    gen = [m.start() for m in re.finditer(r"\bgenerative\b", n, re.I)]
    unk = [m.start() for m in re.finditer(r"\bunknowing\b", n, re.I)]

    return {
        "pages": len(pages),
        "words": len(n.split()),
        "phrase_exact": n.lower().count(PHRASE),
        "phrase_variants": {
            v: n.lower().count(v)
            for v in ("generative un-knowing", "generatively unknowing",
                      "productive not-yet-knowing")
        },
        "counts": {w: whole_word(w, n) for w in
                   ("error", "errors", "glitch", "glitches", "unknowing",
                    "generative", "poetics", "stein")},
        "unknowing_occurrences": [
            {
                "char": i,
                "pdf_page_1based": next(
                    (k + 1 for k, p in enumerate(pages)
                     if re.search(r"unknowing", p, re.I)
                     and len(flat("\x0c".join(pages[:k + 1]))) >= i), None),
                "context": n[max(0, i - 260):i + 260].strip(),
            }
            for i in unk
        ],
        "generative_contexts": [n[max(0, i - 100):i + 100].strip() for i in gen],
        # The load-bearing number: the two words of the phrase never meet.
        "min_char_gap_generative_to_unknowing": min(
            abs(a - b) for a in gen for b in unk) if gen and unk else None,
        "approx_pages_apart": round(
            min(abs(a - b) for a in gen for b in unk) / (len(n) / len(pages)), 1)
        if gen and unk else None,
    }


def measure_review():
    with open(os.path.join(SRC, "carter.txt")) as fh:
        n = flat(fh.read())
    low = n.lower()
    hits = [m.start() for m in re.finditer(r"unknowing", low)]
    # The review's own title string, as the page prints it and as the article
    # instructs readers to cite it.
    title = "generative unknowing: nathan allen jones"
    return {
        "words": len(n.split()),
        "phrase_exact_total": low.count(PHRASE),
        "phrase_in_title_string": low.count(title),
        "unknowing_total": len(hits),
        "occurrences": [
            {
                "char": i,
                "in_title_or_masthead": bool(re.search(
                    title, low[max(0, i - 60):i + 90])),
                "context": n[max(0, i - 300):i + 300].strip(),
            }
            for i in hits
        ],
    }


def measure_repo():
    """Count the phrase in the repository AS OF THE COMMIT THIS NIGHT WAS CUT FROM.

    Not the working tree. The first version of this function walked the working
    tree with a hand-written exclusion list naming the three paths this night
    creates, and a determinism check caught it drifting upward — 74 to 77 —
    because the night's own prose had entered the corpus through `REQUESTS.md`
    and `works/INDEX.md`, which the list did not name and could not simply
    exclude, both holding legitimate earlier occurrences.

    A hand-maintained exclusion list is the wrong instrument for this: it has to
    anticipate every file the night will touch. Pinning to `BASE` needs no
    foresight, is reproducible by a stranger at any later date, and cannot be
    inflated by anything written after the night began. Logged as F-053.
    """
    files = subprocess.run(
        ["git", "-C", REPO, "ls-tree", "-r", "--name-only", BASE],
        capture_output=True, text=True, check=True).stdout.splitlines()

    per_file = {}
    for rel in files:
        if not rel.endswith((".md", ".json", ".astro", ".py")):
            continue
        body = subprocess.run(
            ["git", "-C", REPO, "show", "%s:%s" % (BASE, rel)],
            capture_output=True, text=True, errors="replace").stdout
        c = body.lower().count(PHRASE)
        if c:
            per_file[rel] = c

    return {
        "corpus": "the repository at commit %s — the state origin/main was in when "
                  "this night was cut, so nothing written tonight can enter the count" % BASE,
        "corpus_files_scanned": len(files),
        "files_containing_phrase": len(per_file),
        "total_occurrences": sum(per_file.values()),
        "per_file": dict(sorted(per_file.items(), key=lambda kv: (-kv[1], kv[0]))),
        "work_titled_with_the_phrase": "works/2026-07-13-generative-unknowing/meta.json" in files,
    }


def main():
    results = {
        "night": "2026-08-20",
        "session": 63,
        "phrase_under_test": PHRASE,
        "A_the_book": measure_book(),
        "B_the_review": measure_review(),
        "C_this_repository": measure_repo(),
    }
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(results, fh, indent=2)
        fh.write("\n")

    a, b, c = results["A_the_book"], results["B_the_review"], results["C_this_repository"]
    print("A  book      : %d pages, %d words" % (a["pages"], a["words"]))
    print("   %-22s : %d" % ("'" + PHRASE + "'", a["phrase_exact"]))
    print("   %-22s : %d" % ("'unknowing'", a["counts"]["unknowing"]))
    print("   %-22s : %d" % ("'generative'", a["counts"]["generative"]))
    print("   the two words never come within %d chars (~%s pages) of each other"
          % (a["min_char_gap_generative_to_unknowing"], a["approx_pages_apart"]))
    print("   glitch %d  vs  error %d" % (a["counts"]["glitch"], a["counts"]["error"]))
    print("B  review    : %d words, phrase total %d, of which in the title string %d"
          % (b["words"], b["phrase_exact_total"], b["phrase_in_title_string"]))
    print("   'unknowing' occurrences: %d" % b["unknowing_total"])
    print("C  this repo : %d occurrences across %d files (at commit %s)"
          % (c["total_occurrences"], c["files_containing_phrase"], BASE))
    print("   a work of this practice is titled with the phrase: %s"
          % c["work_titled_with_the_phrase"])
    print("wrote results.json")


if __name__ == "__main__":
    main()
