#!/usr/bin/env python3
"""The Rate of the Rule -- measurement over 63 EU legal acts.

Written after PREDICTIONS.md was committed.  Reads sources/raw/<celex>.html, the EUR-Lex
HTML of every act in sources/MANIFEST.json that returned HTTP 200 with ELI subdivision
anchors, and asks of each act the question Session 81 asked of one:

    How many of its recitals -- the half a 1998 judgment says binds nobody -- contain a
    sentence that names an actor its own articles command and tells that actor to do
    something?

Guideline 10 of the Joint Practical Guide (2015) says the recitals "SHALL NOT CONTAIN
NORMATIVE PROVISIONS OR POLITICAL EXHORTATIONS".  The Guide gives no test.  The test here
is mine, it is fixed in PREDICTIONS.md, and it is printed so a reader can disagree.

Four measurements per act:

  1. THE CORPUS.  Cut at the rct_/art_ anchors into recitals and articles, word-counted.
  2. THE ACTORS, derived from the act's own enacting terms: heads of noun phrases that are
     the subject of `shall` at least three times in the articles, minus a printed stop
     list, intersected with the words that occur in the recitals.
  3. THE REGISTER.  `shall`, `should`, `must`, `may` in each half.
  4. DIRECTED NORMATIVE SENTENCES.  The Session 81 grammar exactly, over the derived
     actors.  The GDPR is measured a second time under Session 81's own fixed actor list,
     so that the two nights' numbers can be compared and their difference reported.

The instrument is calibrated: measure.py exits without measuring anything if it cannot
reproduce Session 81's GDPR figures -- 173 recitals, 99 articles, `shall` 0/479,
`should` 420/2 -- from the same source under the same cut.  That check is the only
guard against a silent change in EUR-Lex's markup between two nights.

Deterministic except for the audit samples, which are drawn by audit.py with a fixed seed.

Writes: corpus.json, results.json.
"""

import html as H
import gzip
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent


def load_json(path):
    """Read a JSON file, transparently accepting the gzipped form.

    corpus.json and the two superseded run files are committed gzipped: they are 12.7 MB
    of largely repeated legal text against an 11 MB repository, and the licence question
    is not the size question.  Gzip keeps every byte checkable offline at a proportionate
    cost, which is the same trade the raw HTML lost.
    """
    path = pathlib.Path(path)
    if path.exists():
        return json.loads(path.read_text())
    gz = path.with_suffix(path.suffix + ".gz")
    with gzip.open(gz, "rt") as fh:
        return json.load(fh)


def dump_json(path, payload, gzipped=False):
    path = pathlib.Path(path)
    text = json.dumps(payload, indent=1) + "\n"
    if gzipped:
        with gzip.open(str(path) + ".gz", "wt") as fh:
            fh.write(text)
        if path.exists():
            path.unlink()
    else:
        path.write_text(text)


RAW = HERE / "sources" / "raw"
MANIFEST = HERE / "sources" / "MANIFEST.json"

REFERENCE = "32016R0679"  # the GDPR, the act Session 81 measured

# Session 81's figures.  If any of these five cannot be reproduced, the cut has changed
# and nothing this file computes about any other act is trustworthy either.
CALIBRATION = {"recitals": 173, "articles": 99,
               "shall_recitals": 0, "shall_articles": 479,
               "should_recitals": 420, "should_articles": 2}

# Fixed in PREDICTIONS.md before this file existed.  Words that name parts of a legal text
# or objects it regulates, not parties it commands.
STOP_HEADS = set("""
regulation regulations directive directives decision decisions recommendation article
articles paragraph paragraphs subparagraph point points annex annexes chapter section
title sentence reference references provision provisions definition definitions
requirement requirements rule rules measure measures obligation obligations condition
conditions procedure procedures criterion criteria list lists date dates deadline period
periods entry force application act acts text texts amendment amendments exemption
exemptions derogation derogations information data following this that which it they them
there who whom and or be been is are was were above below thereof case cases event events
purpose purposes respect accordance addition particular
""".split())

# Session 81's own actor list, used only to re-measure the GDPR for the bridge.
S81_ACTORS = [
    ("the controller", r"[Tt]he controllers?\b"),
    ("the processor", r"[Tt]he processors?\b"),
    ("the data subject", r"[Tt]he data subjects?\b"),
    ("Member States", r"Member States?\b"),
    ("the supervisory authority", r"[Tt]he supervisory authorit(?:y|ies)\b"),
    ("the Commission", r"[Tt]he Commission\b"),
    ("the Board", r"[Tt]he Board\b"),
]

ARTICLE_TAIL_CUT = "Done at"


# --------------------------------------------------------------------------- corpus

def strip_tags(fragment):
    text = re.sub(r"(?s)<[^>]+>", " ", fragment)
    text = H.unescape(text).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def anchors(raw, prefix):
    """Every id="<prefix>_N" in the document, as {N: offset just past the tag}."""
    out = {}
    for m in re.finditer(r'id="%s_(\d+)"' % prefix, raw):
        n = int(m.group(1))
        if n not in out:                       # first occurrence wins
            out[n] = raw.index(">", m.start()) + 1
    return out


def build_corpus(raw):
    """Cut one act into its recitals and articles.  Returns None if the cut is not sound."""
    rec_at = anchors(raw, "rct")
    art_at = anchors(raw, "art")
    if not rec_at or not art_at:
        return None

    # The anchors must number 1..N without a gap, and every recital must precede every
    # article.  An act that fails this is dropped from the population with its reason,
    # rather than measured on a cut nobody checked.
    n_rec, n_art = max(rec_at), max(art_at)
    if sorted(rec_at) != list(range(1, n_rec + 1)):
        return {"error": "recital anchors are not 1..%d without a gap" % n_rec}
    if sorted(art_at) != list(range(1, n_art + 1)):
        return {"error": "article anchors are not 1..%d without a gap" % n_art}
    if not all(rec_at[i] < rec_at[i + 1] for i in range(1, n_rec)):
        return {"error": "recital anchors are not in document order"}
    if not all(art_at[i] < art_at[i + 1] for i in range(1, n_art)):
        return {"error": "article anchors are not in document order"}
    if rec_at[n_rec] > art_at[1]:
        return {"error": "the last recital does not precede the first article"}

    recitals = {}
    for i in range(1, n_rec + 1):
        end = rec_at[i + 1] if i < n_rec else art_at[1]
        text = strip_tags(raw[rec_at[i]:end])
        recitals[i] = re.sub(r"^\(%d\)\s*" % i, "", text)

    articles = {}
    for i in range(1, n_art + 1):
        end = art_at[i + 1] if i < n_art else None
        text = strip_tags(raw[art_at[i]:end])
        if i == n_art:
            text = text.split(ARTICLE_TAIL_CUT)[0].strip()
        articles[i] = text

    return {"recitals": recitals, "articles": articles}


# --------------------------------------------------------------------------- actors

SUBJECT = re.compile(r"([^.;:]{0,60}?)\s+shall\b")


def forms(word):
    """The surface forms of one head, so that singular and plural are one actor.

    THE FIRST VERSION OF THIS FUNCTION WAS A BUG AND IT IS RECORDED RATHER THAN REPAIRED
    IN SILENCE.  It tested presence in the recitals with `head[:-1]` whenever the head
    ended in `s`, which turns `authorities` into `authoritie` and finds it nowhere.  The
    single most commanded party in several acts was therefore rejected as "absent from
    the recitals": 60 occurrences of `authorities` in the deforestation regulation's
    recitals, 90 in the GDPR's, 30 and 21 occurrences respectively as the subject of
    `shall` in their articles.  Every rate in results-run1-plural-bug.json was computed
    with that rule.  F-111.
    """
    out = {word}
    if word.endswith("ies") and len(word) > 4:
        out.add(word[:-3] + "y")
    elif word.endswith(("ses", "xes", "ches", "shes")):
        out.add(word[:-2])
    elif word.endswith("s") and not word.endswith("ss"):
        out.add(word[:-1])
    if word.endswith("y") and len(word) > 2:
        out.add(word[:-1] + "ies")
    elif word.endswith(("s", "x", "ch", "sh")):
        out.add(word + "es")
    else:
        out.add(word + "s")
    return out


def lemma(word):
    """The shortest surface form, used as the key so `state` and `states` are one actor."""
    return min(forms(word), key=lambda w: (len(w), w))


def derive_actors(recitals, articles, threshold=3):
    """The parties this act's own binding half commands, in this act's own words.

    Rule fixed in PREDICTIONS.md: head of the noun phrase before `shall` in the articles,
    at least `threshold` times, not on the stop list, and occurring at least once in the
    recitals.  Everything the rule saw is returned, including what it rejected and why,
    because the rejections are where the reader's disagreement will land -- and in the
    first run they were where the instrument's own error was.
    """
    heads = {}
    for text in articles.values():
        for m in SUBJECT.finditer(text):
            words = m.group(1).split()[-5:]
            if not words:
                continue
            head = re.sub(r"[^a-z]", "", words[-1].lower())
            if head:
                key = lemma(head)
                heads[key] = heads.get(key, 0) + 1

    recital_text = " ".join(recitals.values()).lower()

    kept, rejected = [], []
    for head, n in sorted(heads.items(), key=lambda kv: (-kv[1], kv[0])):
        if n < threshold:
            continue                                    # not a recurring subject
        if head in STOP_HEADS or any(f in STOP_HEADS for f in forms(head)):
            rejected.append({"head": head, "n": n, "why": "stop list"})
            continue
        alternation = "|".join(sorted(map(re.escape, forms(head)), key=len, reverse=True))
        # (?i) IS LOAD-BEARING AND ITS ABSENCE WAS THE SECOND BUG.  The heads are lowercased
        # at derivation and the presence test below runs against a lowercased copy of the
        # recitals, but directed() searches the recitals in their original case.  Without
        # this flag `commission` never matched `the Commission`, `state` never matched
        # `Member States`, and `issuer` never matched a sentence beginning `Issuers` -- so
        # the instrument matched only the lowercase junk heads (`product`, `sector`, `a`)
        # and none of the actual parties.  In the agricultural markets regulation that is
        # 0 lowercase occurrences of `commission` against 111 in any case.  It is why the
        # ten-occurrence sensitivity check collapsed to 0.0 for eight acts whose surviving
        # actors were `commission` and `state`: those were exactly the actors it could not
        # see.  Every rate in results-run2-case-bug.json was computed without it.  F-112.
        pattern = r"(?i)\b(?:%s)\b" % alternation
        if not re.search(pattern, recital_text):
            rejected.append({"head": head, "n": n, "why": "absent from the recitals"})
            continue
        kept.append({"head": head, "n_shall_subject": n, "pattern": pattern})
    return kept, rejected


# --------------------------------------------------------------------------- register

def register(recitals, articles):
    out = {}
    for name, corpus in (("recitals", recitals), ("articles", articles)):
        joined = " ".join(corpus.values())
        out[name] = {w: len(re.findall(r"\b%s\b" % w, joined, re.I))
                     for w in ("shall", "should", "must", "may")}
        out[name]["words"] = len(joined.split())
        # Which divisions carry a `shall`, so a reader can go and look at them.
        out[name]["divisions_with_shall"] = sorted(
            i for i, t in corpus.items() if re.search(r"\bshall\b", t, re.I))
    return out


# --------------------------------------------------------------------------- directed

SENTENCE = re.compile(r"(?<=[.;:])\s+(?=[A-Z(‘])")


def sentences(text):
    return [s.strip() for s in SENTENCE.split(text) if s.strip()]


DIRECTIVE_TAIL = re.compile(r"[^.]{0,80}?\bshould\s+(?:not\s+)?(?:be\s+)?(?:\w+ly\s+)?([a-z]+)")


def directed(recitals, actor_patterns):
    """Session 81's grammar, unchanged, over whatever actor list it is handed.

    A recital is directed where one of its sentences names an actor and then, within 80
    characters and without crossing a full stop, says `should <verb>`.
    """
    # Occurrence counting is Session 81's: at most one hit per actor per sentence, so a
    # sentence that commands two different actors counts twice.  An earlier version here
    # stopped at the first actor in a sentence, which would have made `occurrences` mean
    # something different from last night's 136 while `count` stayed comparable.
    hits, per_actor, occurrences = {}, {}, 0
    for i, text in recitals.items():
        found = []
        for sentence in sentences(text):
            for name, pattern in actor_patterns:
                for m in re.finditer(pattern, sentence):
                    d = DIRECTIVE_TAIL.match(sentence[m.end():])
                    if d:
                        found.append({"actor": name, "verb": d.group(1), "sentence": sentence})
                        per_actor[name] = per_actor.get(name, 0) + 1
                        break
        if found:
            hits[i] = found
            occurrences += len(found)
    return {
        "recitals_directed": sorted(hits),
        "count": len(hits),
        "occurrences": occurrences,
        "per_actor": per_actor,
        "detail": {str(k): v for k, v in hits.items()},
    }


# --------------------------------------------------------------------------- encouraged

def encouraged(recitals, articles):
    def n(corpus):
        return len(re.findall(r"\bencourag(?:e|es|ed|ing|ement)\b",
                              " ".join(corpus.values()), re.I))
    return {"recitals": n(recitals), "articles": n(articles),
            "recital_only": n(recitals) > 0 and n(articles) == 0}


# --------------------------------------------------------------------------- run

def measure_act(source):
    celex = source["celex"]
    path = RAW / ("%s.html" % celex)
    if not path.exists():
        return {"celex": celex, "error": "not fetched"}
    raw = path.read_text("utf-8", "replace")
    corpus = build_corpus(raw)
    if corpus is None:
        return {"celex": celex, "error": "no ELI anchors"}
    if "error" in corpus:
        return {"celex": celex, "error": corpus["error"]}

    recitals, articles = corpus["recitals"], corpus["articles"]
    kept, rejected = derive_actors(recitals, articles)
    d = directed(recitals, [(a["head"], a["pattern"]) for a in kept])

    # Sensitivity, not a second result.  The derived actor list admits junk -- heads like
    # `processing`, `lodged`, `certification` that are noun-phrase heads and not parties --
    # and junk inflates the rate.  Raising the threshold from three occurrences as the
    # subject of `shall` to ten is a mechanical way to ask whether the ranking of acts
    # survives a stricter list, without any hand-cleaning, which would be judgement
    # applied after seeing the answer.
    strict_kept, _ = derive_actors(recitals, articles, threshold=10)
    strict = directed(recitals, [(a["head"], a["pattern"]) for a in strict_kept])

    out = {
        "celex": celex,
        "stratum": source["stratum"],
        "adoption_year": source["adoption_year"],
        "domain": source.get("domain"),
        "title": source.get("title"),
        "n_recitals": len(recitals),
        "n_articles": len(articles),
        "register": register(recitals, articles),
        "actors_kept": kept,
        "actors_rejected": rejected,
        "directed": d,
        "rate": round(100.0 * d["count"] / len(recitals), 1) if recitals else None,
        "strict": {
            "n_actors": len(strict_kept),
            "actors": [a["head"] for a in strict_kept],
            "count": strict["count"],
            "rate": round(100.0 * strict["count"] / len(recitals), 1) if recitals else None,
        },
        "encouraged": encouraged(recitals, articles),
    }
    return out, corpus


def main():
    manifest = load_json(MANIFEST)["sources"]
    in_population = [s for s in manifest if s["http_status"] == 200 and s["has_eli_anchors"]]

    results, corpora, dropped = [], {}, []
    for source in in_population:
        got = measure_act(source)
        if isinstance(got, dict):
            dropped.append(got)
            continue
        record, corpus = got
        results.append(record)
        corpora[record["celex"]] = corpus

    by_celex = {r["celex"]: r for r in results}
    if REFERENCE not in by_celex:
        raise SystemExit("the reference act %s is not in the population -- refusing to report"
                         % REFERENCE)

    # ------------------------------------------------------------------ calibration
    ref = by_celex[REFERENCE]
    observed = {
        "recitals": ref["n_recitals"], "articles": ref["n_articles"],
        "shall_recitals": ref["register"]["recitals"]["shall"],
        "shall_articles": ref["register"]["articles"]["shall"],
        "should_recitals": ref["register"]["recitals"]["should"],
        "should_articles": ref["register"]["articles"]["should"],
    }
    if observed != CALIBRATION:
        print("CALIBRATION FAILED -- the cut does not reproduce Session 81's GDPR figures.")
        for k in CALIBRATION:
            mark = " " if observed[k] == CALIBRATION[k] else " <-- differs"
            print("  %-18s expected %6d  observed %6d%s" % (k, CALIBRATION[k], observed[k], mark))
        raise SystemExit("refusing to measure 62 other acts on a cut that has moved under me")

    # ------------------------------------------------------- the bridge to Session 81
    gdpr_corpus = corpora[REFERENCE]
    s81 = directed(gdpr_corpus["recitals"], S81_ACTORS)
    bridge = {
        "session_81_fixed_actor_list": {"count": s81["count"], "occurrences": s81["occurrences"],
                                        "rate": round(100.0 * s81["count"] / 173, 1)},
        "session_82_derived_actor_list": {"count": ref["directed"]["count"],
                                          "occurrences": ref["directed"]["occurrences"],
                                          "rate": ref["rate"]},
        "recitals_only_S81": sorted(set(s81["recitals_directed"])
                                    - set(ref["directed"]["recitals_directed"])),
        "recitals_only_S82": sorted(set(ref["directed"]["recitals_directed"])
                                    - set(s81["recitals_directed"])),
    }

    payload = {
        "measured": "2026-09-06",
        "calibration": {"expected": CALIBRATION, "observed": observed, "passed": True},
        "population": {
            "probed": len(manifest),
            "in_population": len(in_population),
            "measured": len(results),
            "dropped": dropped,
        },
        "bridge_to_session_81": bridge,
        "acts": sorted(results, key=lambda r: (r["stratum"], r["adoption_year"], r["celex"])),
    }
    (HERE / "results.json").write_text(json.dumps(payload, indent=1) + "\n")

    # corpus.json is the committed evidence: the text every number came from.
    dump_json(HERE / "corpus.json",
              {c: {"recitals": {str(k): v for k, v in d["recitals"].items()},
                   "articles": {str(k): v for k, v in d["articles"].items()}}
               for c, d in corpora.items()}, gzipped=True)

    print("calibration passed on %s" % REFERENCE)
    print("measured %d acts, dropped %d" % (len(results), len(dropped)))
    for d in dropped:
        print("  dropped %s: %s" % (d["celex"], d["error"]))
    print("\nbridge on the GDPR: S81 fixed list %d recitals, S82 derived list %d recitals"
          % (bridge["session_81_fixed_actor_list"]["count"],
             bridge["session_82_derived_actor_list"]["count"]))


if __name__ == "__main__":
    sys.exit(main())
