#!/usr/bin/env python3
"""POST-HOC.  Everything in this file was written after the audit and is declared as post-hoc
everywhere it is reported.  None of it scores a prediction; the predictions are scored against the
pre-registered instrument in adjudicate.py, and they stay scored that way.

Two questions the audit raised and could not answer from the sample:

  1. The `encouraged`-only re-cut.  The audit puts `encouraged` at 14 for 14 and `expected` at 0
     for 21.  What does the population look like if the pattern keeps only the participle that
     survived?  This is a REPAIRED INSTRUMENT AND A DIFFERENT ONE.  Its precision has not been
     audited on a fresh sample, and the only honest claim available is the sample's own: on the 14
     `encouraged` rows drawn under the pre-registered seed it was right 14 times.

  2. The agentless residue.  Sample C's one MISSED row is 'The co-financing of research and
     development (R&D) programmes by industry sources should be encouraged.' -- an exhortation with
     no addressee at all and no infinitive.  Family A requires 'encouraged to' and cannot see it.
     So: how large is the class of exhortation whose addressee has been deleted?
"""

import gzip
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
S82 = HERE.parent / "2026-09-06-the-rate-of-the-rule"

ADDRESSED = re.compile(r"\b(is|are|was|were|be)\s+encouraged\s+to\b", re.IGNORECASE)
# Agentless: "encouraged" not followed by "to" within the clause -- "should be encouraged.",
# "is to be encouraged", "should be further encouraged".  The negative lookahead is the whole test.
AGENTLESS = re.compile(r"\b(is|are|was|were|be)\s+encouraged\b(?!\s+to\b)", re.IGNORECASE)

corpus = json.load(gzip.open(S82 / "corpus.json.gz", "rt"))
res = json.load(open(HERE / "results.json"))
meta = {a["celex"]: a for a in res["acts"]}

out = {"acts": [], "agentless_examples": []}
for celex, act in sorted(corpus.items()):
    row = {"celex": celex, "stratum": meta[celex]["stratum"]}
    for part in ("recitals", "articles"):
        add = agl = 0
        for div, text in act[part].items():
            add += len(ADDRESSED.findall(text))
            for m in AGENTLESS.finditer(text):
                agl += 1
                if len(out["agentless_examples"]) < 60:
                    lo, hi = max(0, m.start() - 200), min(len(text), m.end() + 120)
                    out["agentless_examples"].append(
                        {"celex": celex, "part": part, "division": div,
                         "context": text[lo:hi].strip()})
        row[part] = {"addressed_encouraged": add, "agentless_encouraged": agl}
    out["acts"].append(row)

def tot(stratum, part, key):
    return sum(a[part][key] for a in out["acts"] if a["stratum"] == stratum)

def acts_with(stratum, part, key):
    return sum(1 for a in out["acts"] if a["stratum"] == stratum and a[part][key] > 0)

# Hand classification of every context the agentless probe caught.  Thirteen rows, all read.
# AGENTLESS      the thing encouraged is a practice, a state of affairs or an instrument; no party
#                is named at all -- the addressee has been deleted from the sentence.
# ADDRESSED_MISS a party IS named and is being exhorted, and the pre-registered Family A pattern
#                missed it on syntax alone: a coordinated participle, a gerund complement, or an
#                adjunct interposed between the participle and its infinitive.
AGENTLESS_CLASS = {
    ("32009R1223", "45"): ("AGENTLESS", "'recognition by third countries of alternative methods ... should be encouraged'"),
    ("32012L0027", "18"): ("AGENTLESS", "'Exchange of experience between cities, towns and other public bodies should be encouraged'"),
    ("32013R1308", "24"): ("AGENTLESS", "'consumption of fruit and vegetables ... should be encouraged'"),
    ("32014L0024", "35"): ("AGENTLESS", "'The co-financing of R&D programmes by industry sources should be encouraged.' -- sample C's one MISSED row"),
    ("32016R0679", "100"): ("AGENTLESS", "'the establishment of certification mechanisms and data protection seals and marks should be encouraged'"),
    ("32017R0745", "76"): ("ADDRESSED_MISS", "'Healthcare professionals, users and patients should be encouraged AND ENABLED to report' -- coordinated participle"),
    ("32017R0745", "84"): ("AGENTLESS", "'Joint working ... should be encouraged in the area of market surveillance of devices'"),
    ("32021R2115", "80"): ("AGENTLESS", "'combination of grants and financial instruments should be encouraged'"),
    ("32022R2065", "108"): ("ADDRESSED_MISS", "'providers of such platforms should be encouraged IN DRAWING UP and applying specific crisis protocols' -- gerund complement"),
    ("32023R1115", "40"): ("AGENTLESS", "'the use of recycled relevant commodities and relevant products should be encouraged'"),
    ("32023R2854", "31"): ("AGENTLESS", "'protection of trade secrets ... could help achieve the aim of this Regulation and should be encouraged'"),
    ("32024R0900", "20"): ("ADDRESSED_MISS", "'online platforms ... are encouraged, INCLUDING THROUGH THE CODE OF PRACTICE ON DISINFORMATION, to establish and implement tailored policies' -- interposed adjunct"),
    ("32024R1689", "121"): ("AGENTLESS", "'standardisation ... with stakeholders ... should therefore be encouraged'"),
}

for e in out["agentless_examples"]:
    k = (e["celex"], e["division"])
    if k in AGENTLESS_CLASS:
        e["class"], e["class_note"] = AGENTLESS_CLASS[k]
    else:
        e["class"], e["class_note"] = "UNCLASSIFIED", "no hand verdict entered"

_cls = {}
for e in out["agentless_examples"]:
    _cls[e["class"]] = _cls.get(e["class"], 0) + 1

out["summary"] = {
    "note": "POST-HOC.  A repaired pattern is a different instrument; its precision is unaudited on "
            "a fresh sample.",
    "agentless_probe_hand_classified": _cls,
    "stratum_B": {
        "addressed_recitals": tot("B", "recitals", "addressed_encouraged"),
        "addressed_articles": tot("B", "articles", "addressed_encouraged"),
        "agentless_recitals": tot("B", "recitals", "agentless_encouraged"),
        "agentless_articles": tot("B", "articles", "agentless_encouraged"),
        "acts_with_addressed_recitals": acts_with("B", "recitals", "addressed_encouraged"),
        "acts_with_agentless_recitals": acts_with("B", "recitals", "agentless_encouraged"),
    },
    "stratum_A": {
        "addressed_recitals": tot("A", "recitals", "addressed_encouraged"),
        "agentless_recitals": tot("A", "recitals", "agentless_encouraged"),
        "acts_with_addressed_recitals": acts_with("A", "recitals", "addressed_encouraged"),
        "acts_with_agentless_recitals": acts_with("A", "recitals", "agentless_encouraged"),
    },
    "gdpr": next(a for a in out["acts"] if a["celex"] == "32016R0679"),
}

json.dump(out, open(HERE / "residue.json", "w"), indent=1)
print(json.dumps(out["summary"], indent=1))
print("\nagentless contexts captured: %d" % len(out["agentless_examples"]))
for e in out["agentless_examples"][:12]:
    print(" -", e["celex"], e["part"], e["division"], "|", e["context"][-190:].replace("\n", " "))
