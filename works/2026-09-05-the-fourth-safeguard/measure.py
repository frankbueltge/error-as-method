#!/usr/bin/env python3
"""The Fourth Safeguard -- measurement over Regulation (EU) 2016/679.

Reads one committed file, sources/celex-32016R0679-en.html, the EUR-Lex HTML of the GDPR
(CELEX 32016R0679, English, fetched 2026-09-05; hash in sources/MANIFEST.json).

It cuts that file into 173 recitals and 99 articles, and then measures three things:

  1. THE REGISTER.  Where 'shall' occurs and where 'should' occurs.  The Joint Practical Guide
     (2015), Guideline 10.1, says the recitals use "non-mandatory language and must not be capable
     of being confused with the enacting terms"; the heading of Guideline 10 says they "SHALL NOT
     CONTAIN NORMATIVE PROVISIONS OR POLITICAL EXHORTATIONS".

  2. DIRECTED NORMATIVE SENTENCES.  A sentence in a recital that names an actor of the regulation
     and tells that actor, with 'should', to do something.  P1 and P2 of PREDICTIONS.md.

  3. THE SAFEGUARD ATOMS.  Every 'right (not) to ...' in both halves, decomposed into the
     coordinated infinitives that follow it, because that is the form in which recital 71 lists
     four safeguards and Article 22(3) lists three.  Each recital atom gets a MECHANICAL verdict
     here; the HAND verdict lives in census.json and is not computed by this file.

Everything is deterministic.  No randomness, so no seed.

Writes: corpus.json, results.json.
"""

import html as H
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "sources" / "celex-32016R0679-en.html"

N_RECITALS = 173
N_ARTICLES = 99

# The signature block that follows Article 99.  Everything from here on -- the signatures and the
# footnote apparatus -- is outside the population and is cut off.
ARTICLE_TAIL_CUT = "Done at Brussels"


# --------------------------------------------------------------------------- corpus

def strip_tags(fragment: str) -> str:
    text = re.sub(r"(?s)<[^>]+>", " ", fragment)
    text = H.unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def build_corpus(raw: str):
    """Split the document at the ELI subdivision anchors EUR-Lex puts on every recital and article.

    A division runs from just after its own anchor tag to just before the next one's; the last
    recital ends where the first article begins, and the last article is cut at the signature.
    """

    def anchor(prefix: str, n: int) -> int:
        match = re.search(r'id="%s_%d"' % (prefix, n), raw)
        if match is None:
            raise SystemExit("anchor %s_%d not found -- the source is not the expected document" % (prefix, n))
        return raw.index(">", match.start()) + 1

    rec_at = {i: anchor("rct", i) for i in range(1, N_RECITALS + 1)}
    art_at = {i: anchor("art", i) for i in range(1, N_ARTICLES + 1)}

    ordered = all(rec_at[i] < rec_at[i + 1] for i in range(1, N_RECITALS)) \
        and all(art_at[i] < art_at[i + 1] for i in range(1, N_ARTICLES)) \
        and rec_at[N_RECITALS] < art_at[1]
    if not ordered:
        raise SystemExit("the divisions are not in document order -- refusing to measure")

    recitals = {}
    for i in range(1, N_RECITALS + 1):
        end = rec_at[i + 1] if i < N_RECITALS else art_at[1]
        text = strip_tags(raw[rec_at[i]:end])
        recitals[i] = re.sub(r"^\(%d\)\s*" % i, "", text)

    articles = {}
    for i in range(1, N_ARTICLES + 1):
        end = art_at[i + 1] if i < N_ARTICLES else None
        text = strip_tags(raw[art_at[i]:end])
        if i == N_ARTICLES:
            text = text.split(ARTICLE_TAIL_CUT)[0].strip()
        articles[i] = text

    return recitals, articles


# --------------------------------------------------------------------------- 1. register

def register(recitals, articles):
    def count(corpus, word):
        return {i: len(re.findall(r"\b%s\b" % word, t, re.I)) for i, t in corpus.items()}

    out = {}
    for name, corpus in (("recitals", recitals), ("articles", articles)):
        out[name] = {}
        for word in ("shall", "should", "must", "may"):
            per = count(corpus, word)
            out[name][word] = {
                "total": sum(per.values()),
                "divisions_with_at_least_one": sum(1 for v in per.values() if v),
                "per_division": {str(k): v for k, v in per.items() if v},
            }
    return out


# --------------------------------------------------------------------------- 2. directed norms

# The actors the regulation itself names.  Fixed in PREDICTIONS.md before this file existed.
ACTORS = [
    ("the controller", r"[Tt]he controllers?\b"),
    ("the processor", r"[Tt]he processors?\b"),
    ("the data subject", r"[Tt]he data subjects?\b"),
    ("Member States", r"Member States?\b"),
    ("the supervisory authority", r"[Tt]he supervisory authorit(?:y|ies)\b"),
    ("the Commission", r"[Tt]he Commission\b"),
    ("the Board", r"[Tt]he Board\b"),
]

SENTENCE = re.compile(r"(?<=[.;:])\s+(?=[A-Z(‘])")


def sentences(text: str):
    return [s.strip() for s in SENTENCE.split(text) if s.strip()]


def directed(recitals):
    """A recital is 'directed' where one sentence names an actor and then tells it 'should <verb>'.

    The actor must come before the 'should' in the same sentence and the word after 'should' (or
    after an intervening adverb or 'not', or after 'be') must be alphabetic -- that is the verb.
    Impersonal 'it should be possible' and 'this Regulation should apply' never match, because
    neither 'it' nor 'this Regulation' is in ACTORS.
    """
    hits = {}
    per_actor = {name: 0 for name, _ in ACTORS}
    for i, text in recitals.items():
        found = []
        for sentence in sentences(text):
            for name, pattern in ACTORS:
                for m in re.finditer(pattern, sentence):
                    tail = sentence[m.end():]
                    d = re.match(r"[^.]{0,80}?\bshould\s+(?:not\s+)?(?:be\s+)?(?:\w+ly\s+)?([a-z]+)", tail)
                    if d:
                        found.append({"actor": name, "verb": d.group(1), "sentence": sentence})
                        break
        if found:
            hits[i] = found
            for f in found:
                per_actor[f["actor"]] += 1
    return {
        "recitals_with_a_directed_sentence": sorted(hits),
        "count": len(hits),
        "occurrences": sum(len(v) for v in hits.values()),
        "per_actor_occurrences": per_actor,
        "detail": {str(k): v for k, v in hits.items()},
    }


# --------------------------------------------------------------------------- 3. safeguard atoms

RIGHT = re.compile(r"\bright\s+(not\s+)?to\b", re.I)
# A coordinated infinitive after the first one: ", to X", " and to X", " or to X".
COORD = re.compile(r",\s*(?=to\s)|\s+and\s+(?=to\s)|\s+or\s+(?=to\s)")


def sentence_end(text: str, pos: int) -> int:
    m = re.search(r"\.(?=\s+[A-Z(]|\s*$)", text[pos:])
    return pos + m.start() if m else len(text)


def atoms(text: str):
    out = []
    for m in RIGHT.finditer(text):
        span = text[m.end():sentence_end(text, m.end())]
        parts = COORD.split(span)
        head = parts[0].strip()
        if head:
            out.append(("not to " if m.group(1) else "") + head)
        for p in parts[1:]:
            p = p.strip()
            if p.startswith("to "):
                out.append(p[3:].strip())
    return out


def stem(word: str) -> str:
    """A crude stem: the first four characters, which is all the mechanical verdict is entitled to.

    'challenge' -> 'chal', 'obtain' -> 'obta'.  Deliberately blunt: this rule exists to be beaten by
    the hand pass, and P4 predicts how often it is.
    """
    return word.lower()[:4]


def collect_atoms(recitals, articles):
    rec_atoms, art_atoms = [], []
    for i in sorted(recitals):
        for a in atoms(recitals[i]):
            rec_atoms.append({"recital": i, "atom": a})
    for i in sorted(articles):
        for a in atoms(articles[i]):
            art_atoms.append({"article": i, "atom": a})

    article_text = " ".join(articles.values()).lower()
    for entry in rec_atoms:
        head = re.match(r"(?:not to\s+)?([a-z’']+)", entry["atom"].lower())
        entry["head_word"] = head.group(1) if head else ""
        entry["head_stem"] = stem(entry["head_word"]) if entry["head_word"] else ""
        entry["mechanical"] = "MATCHED" if entry["head_stem"] and entry["head_stem"] in article_text else "UNMATCHED"
    return rec_atoms, art_atoms


STOP = {"his", "her", "the", "and", "or", "of", "to", "a", "an", "such", "that", "this", "which",
        "him", "she", "he", "for", "with", "after", "shall", "should", "any", "part", "concerning",
        "personal", "data", "subject", "controller", "processor", "not", "from", "their", "its"}


def content_words(atom: str):
    """The words of an atom that carry its object, with the head verb removed.

    The head verb is removed because leaving it in was the night's second dead end and the same
    mistake as the first: 'obtain an explanation' and 'obtain human intervention' then intersect on
    'obtain' and the check calls them the same safeguard.  Twice, an instrument built to find a
    missing safeguard mistook a shared verb for a shared right -- which is exactly what a string
    match does to a legal text, made on the one atom a court has ruled about.
    """
    words = [w for w in re.findall(r"[a-z]+", atom.lower())]
    if words:
        words = words[1:]
    return {w for w in words if len(w) >= 4 and w not in STOP}


def calibration(recitals, articles):
    """The declared check: recital 71 lists four safeguards after 'right to', Article 22(3) three.

    The instrument is only allowed to run if this reproduces the diff a court has already ruled on.

    An atom of the recital counts as PRESENT in the article when some article atom shares its head
    stem AND at least one content word with it.  The head stem alone is not enough and the first
    version of this function, which used it alone, is the night's first dead end: 'obtain human
    intervention' and 'obtain an explanation of the decision reached' share a verb and are not the
    same safeguard, so the check reported no diff at all and the calibration failed.  Recorded in
    work.md rather than quietly fixed.
    """
    r71 = atoms(recitals[71])
    a22 = atoms(articles[22])
    r_safe = [a for a in r71 if not a.startswith("not to")]
    a_safe = [a for a in a22 if not a.startswith("not to")]

    missing = []
    for a in r_safe:
        head, words = stem(a.split()[0]), content_words(a)
        present = any(stem(b.split()[0]) == head and (words & content_words(b)) for b in a_safe)
        if not present:
            missing.append(a)
    return {
        "recital_71_atoms": r71,
        "article_22_atoms": a22,
        "recital_71_safeguards": r_safe,
        "article_22_safeguards": a_safe,
        "in_recital_not_in_article": missing,
        "passes": any("explanation" in a for a in missing),
    }


# --------------------------------------------------------------------------- main

def main():
    raw = SRC.read_text(encoding="utf-8")
    recitals, articles = build_corpus(raw)

    cal = calibration(recitals, articles)
    if not cal["passes"]:
        raise SystemExit("calibration failed: the extractor does not reproduce the recital 71 / Article 22(3) diff")

    rec_atoms, art_atoms = collect_atoms(recitals, articles)

    words = {}
    for word in ("explanation", "explain", "contest", "challenge", "meaningful information", "logic involved"):
        words[word] = {
            "recitals": sum(len(re.findall(word, t, re.I)) for t in recitals.values()),
            "articles": sum(len(re.findall(word, t, re.I)) for t in articles.values()),
        }

    # An extra measurement, added after the predictions were closed and scored by none of them:
    # which words does the non-binding half of the regulation use that the binding half never uses?
    # Reported because the census turned up three of them by hand and a count is cheaper to check
    # than three anecdotes.  Marked 'unpredicted' in results.json so nothing here can be read as a
    # confirmation of anything fixed in advance.
    rec_words, art_words = {}, set()
    for t in recitals.values():
        for w in re.findall(r"[a-z]{5,}", t.lower()):
            rec_words[w] = rec_words.get(w, 0) + 1
    for t in articles.values():
        art_words.update(re.findall(r"[a-z]{5,}", t.lower()))
    gap = sorted(((c, w) for w, c in rec_words.items() if w not in art_words and c >= 2), reverse=True)

    results = {
        "unpredicted_vocabulary_gap": {
            "rule": "alphabetic tokens of five characters or more, lower-cased; a token is in the gap "
                    "if it occurs at least twice in the 173 recitals and never in the 99 articles",
            "distinct_recital_tokens": len(rec_words),
            "distinct_article_tokens": len(art_words),
            "gap_size": len(gap),
            "gap": [{"word": w, "recital_occurrences": c} for c, w in gap],
        },
        "source": {
            "file": SRC.name,
            "celex": "32016R0679",
            "recitals": len(recitals),
            "articles": len(articles),
            "recital_words": sum(len(t.split()) for t in recitals.values()),
            "article_words": sum(len(t.split()) for t in articles.values()),
        },
        "calibration": cal,
        "register": register(recitals, articles),
        "directed_normative": directed(recitals),
        "word_counts": words,
        "atoms": {
            "recital_atoms": rec_atoms,
            "article_atoms": art_atoms,
            "n_recital_atoms": len(rec_atoms),
            "n_article_atoms": len(art_atoms),
            "mechanical_unmatched": [a for a in rec_atoms if a["mechanical"] == "UNMATCHED"],
        },
    }

    (HERE / "corpus.json").write_text(
        json.dumps({"recitals": {str(k): v for k, v in recitals.items()},
                    "articles": {str(k): v for k, v in articles.items()}},
                   ensure_ascii=False, indent=1),
        encoding="utf-8")
    (HERE / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")

    d = results["directed_normative"]
    print("recitals %d  articles %d" % (len(recitals), len(articles)))
    print("calibration: recital 71 has %d safeguard atoms, Article 22 has %d; missing %s"
          % (len(cal["recital_71_safeguards"]), len(cal["article_22_safeguards"]),
             cal["in_recital_not_in_article"]))
    print("shall  recitals %d / articles %d" % (results["register"]["recitals"]["shall"]["total"],
                                                results["register"]["articles"]["shall"]["total"]))
    print("should recitals %d / articles %d" % (results["register"]["recitals"]["should"]["total"],
                                                results["register"]["articles"]["should"]["total"]))
    print("directed recitals: %d of 173 (%d occurrences)" % (d["count"], d["occurrences"]))
    print("per actor:", d["per_actor_occurrences"])
    print("atoms: %d recital / %d article; mechanically unmatched %d"
          % (len(rec_atoms), len(art_atoms), len(results["atoms"]["mechanical_unmatched"])))


if __name__ == "__main__":
    main()
