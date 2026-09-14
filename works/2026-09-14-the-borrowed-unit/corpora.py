#!/usr/bin/env python3
"""corpora.py -- the three committed corpora, each reduced to (population, blocks).

Session 88 measured, over one corpus, how far back a reader must look from an agentless
obligation before a word for a party is in reach.  `S88.REACH` fixed the claim that the near end
of that curve is a property of the WHATWG drafting tradition rather than of normative English, and
said the check needs no network because both other corpora are committed here.  This module is the
part that has to be right before anything is counted: it produces, for each tradition, the same two
objects Session 88's scan consumed --

    population : the rows to measure, restricted to B-FORM and AGENTLESS and the BINDING register
    blocks     : the document's text divided into ordered units, so that "k blocks back" is defined

and nothing else.  Every reduction below is a decision, and each is stated where it is made.

The three corpora, none re-fetched:

  whatwg  works/2026-09-11-eleven-sentences/   22 living standards   register = NORM
  eu      works/2026-09-06-the-rate-of-the-rule/  63 acts            register = the articles
  rfc     works/2026-09-10-only-when-capitals/    63 RFCs            register = the capitals

One repair is made here and is not silent.  Session 86 wrote its occurrence rows with a field
called `para`, and that field is a SENTENCE ordinal, not a paragraph index -- `measure.py` fills it
from `for i, sent in enumerate(sentences(text))`.  Nothing in Session 86 depends on it (it is used
once, as a sort key in `draw.py`), so that night is untouched; but a port that reads `para` as a
paragraph is measuring a different corpus than it thinks.  `rfc_blocks()` re-derives the paragraph
division from the committed text with Session 86's own `defurniture` and splitter, and returns the
sentence-index-to-paragraph map alongside it; `verify.py` checks that every stored sentence is
byte-identical to the sentence standing at its own index.
"""

import gzip
import importlib.util
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKS = HERE.parent
S82 = WORKS / "2026-09-06-the-rate-of-the-rule"        # the 63 EU acts
S84 = WORKS / "2026-09-08-no-one-to-bear-it"           # their occurrences
S86 = WORKS / "2026-09-10-only-when-capitals"          # the 63 RFCs and their occurrences
S87 = WORKS / "2026-09-11-eleven-sentences"            # the 22 standards and their occurrences
S88 = WORKS / "2026-09-12-adjacent-text"               # the scan being ported


def _m86():
    """Session 86's own measure.py, imported rather than copied, so the split cannot drift."""
    spec = importlib.util.spec_from_file_location("s86_measure", S86 / "measure.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------------------------------ WHATWG (S87)
def whatwg():
    corpus = json.load(gzip.open(S87 / "corpus.json.gz"))
    occ = json.load(gzip.open(S87 / "occurrences.json.gz"))
    pop = [x for x in occ
           if x["form"] == "B-FORM" and x["agent"] == "AGENTLESS" and x["register"] == "NORM"]
    blocks = {doc: [b["t"] for b in d["blocks"]] for doc, d in corpus.items()}
    rows = [{"doc": x["doc"], "block": x["block"], "sentence": x["sentence"],
             "modal": x["modal"], "offset": x["offset"]} for x in pop]
    return rows, blocks


# ---------------------------------------------------------------------------------------- EU (S84)
def eu():
    """A block is a numbered division: recital 1..n, then article 1..m, in that order.

    That ordering is the acts' own and is how they are read; the reader of article 30 has the
    recitals behind them.  The binding register is the articles -- Session 84's own reason, and the
    Court's: "the preamble to a Community act has no binding legal force and cannot be relied on as
    a ground for derogating from the actual provisions of the act in question", Judgment of the
    Court of 19 November 1998, C-162/97 *Nilsson and others*, paragraph 54, re-read at primary
    tonight at <https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:61997CJ0162>
    (HTTP 200).

    The first draft of this docstring cited a different case, by a name and a paragraph number that
    do not go together and were written from nothing.  It was caught by going to look, before any
    commit.  F-139.
    """
    corpus = json.load(gzip.open(S82 / "corpus.json.gz", "rt"))
    occ = json.load(gzip.open(S84 / "occurrences.json.gz"))
    blocks, index = {}, {}
    for celex, act in corpus.items():
        seq, pos = [], {}
        for part in ("recitals", "articles"):
            for k in sorted(act[part], key=int):
                pos[(part, k)] = len(seq)
                seq.append(act[part][k])
        blocks[celex] = seq
        index[celex] = pos
    rows = []
    for x in occ:
        if not (x["form"] == "B-FORM" and x["agent"] == "AGENTLESS" and x["part"] == "articles"):
            continue
        rows.append({"doc": x["celex"], "block": index[x["celex"]][(x["part"], x["division"])],
                     "sentence": x["sentence"], "modal": x["modal"], "offset": x["offset"]})
    return rows, blocks


# --------------------------------------------------------------------------------------- RFC (S86)
def rfc_blocks():
    """Re-derive paragraphs from the committed text, with Session 86's own defurniture and split.

    Returns (blocks, sent_to_para, sentences_at_index) -- the last two only so verify.py can check
    the re-derivation against every stored occurrence.
    """
    m = _m86()
    corpus = json.load(gzip.open(S86 / "corpus.json.gz", "rt"))
    blocks, s2p, sents = {}, {}, {}
    for key, d in corpus.items():
        text, _ = m.defurniture(d["text"])
        paras, mapping, flat_sents = [], [], []
        for para in re.split(r"\n\s*\n", text):
            flat = re.sub(r"\s+", " ", para).strip()
            if not flat:
                continue
            paras.append(flat)
            for s in m.SENT_SPLIT.split(flat):
                s = s.strip()
                if s:
                    mapping.append(len(paras) - 1)
                    flat_sents.append(s)
        rfc = int(key)
        blocks[rfc] = paras
        s2p[rfc] = mapping
        sents[rfc] = flat_sents
    return blocks, s2p, sents


def rfc():
    """The binding register is the capitals: RFC 8174 says the words are norms only in all caps."""
    occ = json.load(gzip.open(S86 / "occurrences.json.gz"))
    blocks, s2p, _ = rfc_blocks()
    rows = []
    for x in occ:
        if not (x["form"] == "B-FORM" and x["agent"] == "AGENTLESS" and x["case"] == "UPPER"):
            continue
        rows.append({"doc": x["rfc"], "block": s2p[x["rfc"]][x["para"]],
                     "sentence": x["sentence"], "modal": x["modal"], "offset": x["offset"]})
    return rows, blocks


CORPORA = {"whatwg": whatwg, "eu": eu, "rfc": rfc}


# ------------------------------------------------------------------------------------ the terms
# Session 88's list, read out of its results.json rather than restated, so the two cannot drift.
def whatwg_terms():
    return json.load(open(S88 / "results.json"))["mechanical_ceiling"]["party_terms"]


def base_terms():
    """The WHATWG list with its regex furniture stripped, as a plain list of terms."""
    pat = whatwg_terms()
    inner = pat[len(r"\b("):-len(r")\b")]
    return inner.split("|")
