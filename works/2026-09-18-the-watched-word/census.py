#!/usr/bin/env python3
"""The Watched Word — the mechanical half of Session 92.

Four measurements, in the order PREDICTIONS.md fixes them.

  1. RECONCILE. Every quote in `shapes.json`, and every quote in Session 85's committed
     `readings.json`, must be found byte for byte in the file its row names, ignoring nothing but
     Markdown emphasis marks. A row whose quote is not there is a row I invented, and this script
     exits non-zero rather than printing a number. (Method and the `flatten` trick inherited from
     `works/2026-09-09-what-the-sentence-lets-in/measure.py`, which is where they were written.)

  2. COVERAGE. Tokenise the standing sentence into its content terms under Session 85's own
     function-word list, and count how many fixed readings each term carries on Session 85's table.
     The terms with zero are the ones no night has ever said the sense of. PREDICTIONS.md §4 P6
     declares the answer; this recomputes it.

  3. THE WATCH EFFECT. For each of the eleven terms, its rate per 1,000 words in the journal
     entries of Sessions 79-84 (before `S85.OVERLOAD` was fixed) and 86-91 (after), and the ratio
     between them. Session 85 is excluded from both windows, declared in PREDICTIONS.md §4 before
     this file existed. Reported twice: over all text, and over text excluding blockquote lines,
     because every journal quotes the standing sentence and that is a constant offset.

  4. THE CROSS-CHECK I DO NOT CONTROL. For each shape, find the paragraph its quote sits in, and
     report which terms of the standing sentence occur there. My verdict about which term a shape
     loads is in `shapes.json`; this is the machine's independent reading of the same passage, and
     P4 predicts it disagrees with me more often than it agrees.

Reads only committed files. Writes `results.json`. Deterministic, stdlib only, no network.

    python3 census.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
S85 = os.path.join(ROOT, "works", "2026-09-09-what-the-sentence-lets-in")

SENTENCE = ("Error is a special case of the epistemic thing — a difference onto which "
            "an observer has already imposed a norm.")

# Session 85's list, copied unchanged rather than re-derived. A longer list would let me decide
# which terms count as content by deciding what a function word is.
FUNCTION_WORDS = {
    "a", "an", "the", "is", "are", "be", "been", "has", "have", "of", "to", "and", "or", "that",
    "which", "who", "it", "its", "in", "on", "at", "by", "for", "with", "as", "not", "no", "some",
    "this", "these", "one", "two", "more", "need", "can", "must", "where", "when", "what",
}

WORD = re.compile(r"[a-z]+")
EMPHASIS = re.compile(r"[*_`]")
HEAD = re.compile(r"^# Research day — (\d{4}-\d{2}-\d{2}) \(Session (\d+)\)")

PRE = list(range(79, 85))    # the six nights before S85.OVERLOAD was fixed
POST = list(range(86, 92))   # the six nights after it
ROW = "S85.OVERLOAD"


def flatten(text):
    return EMPHASIS.sub("", text)


def content_words(text):
    seen, out = set(), []
    for tok in WORD.findall(text.lower()):
        if tok in FUNCTION_WORDS or tok in seen:
            continue
        seen.add(tok)
        out.append(tok)
    return out


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def reconcile(rows):
    """Complaint list. Empty means every quote is where its row says it is."""
    bad = []
    for rid, source, quote in rows:
        path = os.path.join(ROOT, source)
        if not os.path.exists(path):
            bad.append(f"{rid}: no such file {source}")
            continue
        if flatten(quote) not in flatten(read(source)):
            bad.append(f"{rid}: quote not found in {source}")
    return bad


def journals():
    """Every journal entry that declares a session number in its first line: session -> path."""
    out = {}
    base = os.path.join(ROOT, "journal")
    for name in sorted(os.listdir(base)):
        if not name.endswith(".md"):
            continue
        rel = os.path.join("journal", name)
        first = read(rel).splitlines()[0] if read(rel).splitlines() else ""
        found = HEAD.match(first)
        if not found:
            continue
        session = int(found.group(2))
        if session in out:
            sys.exit(f"two journal entries claim Session {session}: {out[session]} and {rel}")
        out[session] = rel
    return out


def strip_quotes(text):
    """Drop blockquote lines. Every journal quotes the standing sentence in one, so the terms of
    that sentence carry a constant floor that is about the ritual and not about the night."""
    return "\n".join(l for l in text.splitlines() if not l.lstrip().startswith(">"))


def tally(paths, terms):
    """Per-window totals: words, and occurrences of each term as a whole token."""
    both = {}
    for label, prep in (("all", lambda t: t), ("no_quotes", strip_quotes)):
        words, counts = 0, {t: 0 for t in terms}
        per_night = {}
        for session, rel in sorted(paths.items()):
            toks = WORD.findall(flatten(prep(read(rel))).lower())
            words += len(toks)
            night = {t: 0 for t in terms}
            for tok in toks:
                if tok in night:
                    night[tok] += 1
                    counts[tok] += 1
            per_night[session] = {"words": len(toks), **night}
        both[label] = {"words": words, "counts": counts, "per_night": per_night}
    return both


def rates(window, terms):
    return {t: round(1000.0 * window["counts"][t] / window["words"], 4) for t in terms}


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def grip(paths):
    """Of the paragraphs that contain `observer`, how many also name the row that watches it."""
    n_obs = n_both = 0
    per_night = {}
    for session, rel in sorted(paths.items()):
        obs = both = 0
        for para in paragraphs(flatten(read(rel))):
            low = para.lower()
            if "observer" not in low:
                continue
            obs += 1
            if ROW.lower() in low:
                both += 1
        per_night[session] = {"observer_paragraphs": obs, "also_naming_the_row": both}
        n_obs += obs
        n_both += both
    return {"observer_paragraphs": n_obs, "also_naming_the_row": n_both,
            "share": round(n_both / n_obs, 4) if n_obs else None, "per_night": per_night}


def cross_check(shapes, terms):
    """Which terms of the standing sentence occur in the paragraph each shape's quote sits in."""
    out = []
    for sh in shapes:
        text = flatten(read(sh["source"]))
        quote = flatten(sh["quote"])
        hit = None
        for para in paragraphs(text):
            if quote in para:
                hit = para
                break
        if hit is None:
            sys.exit(f"{sh['id']}: quote reconciles against the file but sits in no paragraph")
        toks = WORD.findall(hit.lower())
        present = {t: toks.count(t) for t in terms if t in toks}
        ranked = sorted(present.items(), key=lambda kv: (-kv[1], kv[0]))
        out.append({"id": sh["id"], "my_verdict": sh["lands_on"],
                    "terms_in_its_paragraph": present,
                    "machine_top_term": ranked[0][0] if ranked else None,
                    "agrees_with_me": bool(ranked) and ranked[0][0] == sh["lands_on"]})
    return out


def main():
    with open(os.path.join(HERE, "shapes.json"), encoding="utf-8") as fh:
        book = json.load(fh)
    shapes = book["shapes"]
    if book["_sentence"] != SENTENCE:
        sys.exit("the sentence in shapes.json is not the sentence in this file — stop")

    with open(os.path.join(S85, "readings.json"), encoding="utf-8") as fh:
        readings = json.load(fh)["readings"]

    bad = reconcile([(s["id"], s["source"], s["quote"]) for s in shapes])
    bad += reconcile([(f"reading:{r['word']}:S{r['session']}", r["source"], r["quote"])
                      for r in readings])
    if bad:
        for line in bad:
            print("RECONCILE:", line)
        sys.exit(1)

    terms = content_words(SENTENCE)

    per_term = {t: [] for t in terms}
    for r in readings:
        if r["word"] not in per_term:
            sys.exit(f"readings.json fixes a reading on {r['word']!r}, not a term of the sentence")
        per_term[r["word"]].append({"session": r["session"], "reading": r["reading"]})
    coverage = {t: {"n_readings": len(v), "readings": sorted(v, key=lambda x: x["session"])}
                for t, v in per_term.items()}
    unread = [t for t in terms if not per_term[t]]

    js = journals()
    missing = [s for s in PRE + POST if s not in js]
    if missing:
        sys.exit(f"no journal entry found for sessions {missing}")
    pre_paths = {s: js[s] for s in PRE}
    post_paths = {s: js[s] for s in POST}

    pre, post = tally(pre_paths, terms), tally(post_paths, terms)
    watch = {}
    for label in ("all", "no_quotes"):
        pr, po = rates(pre[label], terms), rates(post[label], terms)
        watch[label] = {
            "pre_words": pre[label]["words"], "post_words": post[label]["words"],
            "per_term": {t: {"pre_count": pre[label]["counts"][t],
                             "post_count": post[label]["counts"][t],
                             "pre_rate": pr[t], "post_rate": po[t],
                             "ratio": round(po[t] / pr[t], 3) if pr[t] else None}
                         for t in terms},
            "pre_per_night": pre[label]["per_night"], "post_per_night": post[label]["per_night"],
        }
        ranked = [t for t in terms if watch[label]["per_term"][t]["ratio"] is not None]
        ranked.sort(key=lambda t: -watch[label]["per_term"][t]["ratio"])
        watch[label]["ratio_rank"] = ranked
        watch[label]["highest_pre_rate_term"] = max(terms, key=lambda t: pr[t])
        watch[label]["undefined_ratio_terms"] = [t for t in terms
                                                 if watch[label]["per_term"][t]["ratio"] is None]

    results = {
        "_what": "Session 92's counts. Written by census.py, which refuses to print if a quote in "
                 "shapes.json or in Session 85's readings.json is not in the file it names.",
        "sentence": SENTENCE,
        "terms": terms,
        "coverage": coverage,
        "unread_terms": unread,
        "n_unread_terms": len(unread),
        "windows": {"pre": {"sessions": PRE, "files": pre_paths},
                    "post": {"sessions": POST, "files": post_paths},
                    "excluded": {"session": 85, "why": "the night that fixed S85.OVERLOAD and "
                                 "wrote the load table; it would swamp `observer` by construction"}},
        "watch": watch,
        "grip_post": grip(post_paths),
        "grip_pre": grip(pre_paths),
        "cross_check": cross_check(shapes, terms),
    }
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")

    print(f"terms in the sentence            : {len(terms)}  {terms}")
    print(f"terms with zero fixed readings   : {len(unread)}  {unread}")
    print()
    print("watch effect (all text), rate per 1,000 words of a journal entry")
    print(f"{'term':<12}{'pre':>9}{'post':>9}{'ratio':>9}")
    for t in watch["all"]["ratio_rank"]:
        r = watch["all"]["per_term"][t]
        print(f"{t:<12}{r['pre_rate']:>9.3f}{r['post_rate']:>9.3f}{r['ratio']:>9.3f}")
    for t in watch["all"]["undefined_ratio_terms"]:
        r = watch["all"]["per_term"][t]
        print(f"{t:<12}{r['pre_rate']:>9.3f}{r['post_rate']:>9.3f}{'--':>9}")
    print()
    print(f"highest pre-window rate          : {watch['all']['highest_pre_rate_term']}")
    print(f"observer paragraphs, post window : {results['grip_post']['observer_paragraphs']}, "
          f"of which {results['grip_post']['also_naming_the_row']} name {ROW} "
          f"({results['grip_post']['share']})")
    print(f"observer paragraphs, pre window  : {results['grip_pre']['observer_paragraphs']}, "
          f"of which {results['grip_pre']['also_naming_the_row']} name {ROW}")
    print()
    print("cross-check — the machine's top sentence-term in each shape's own paragraph")
    for row in results["cross_check"]:
        mark = "agrees" if row["agrees_with_me"] else "differs"
        print(f"  {row['id']:<16} mine={row['my_verdict']:<11} "
              f"machine={str(row['machine_top_term']):<11} {mark}")
    agree = sum(1 for r in results["cross_check"] if r["agrees_with_me"])
    print(f"  agreement: {agree} of {len(results['cross_check'])}")


if __name__ == "__main__":
    main()
