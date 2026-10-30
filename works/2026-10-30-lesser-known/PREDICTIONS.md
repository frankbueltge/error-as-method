# Predictions — experiment 44, *Lesser Known* (Session 164)

*Committed and pushed before any maker ran. Nothing below is edited after the data. `score.py` and `anchors_u.py`
implement these definitions and were committed with them.*

## Why this night

Session 163 found that two of the people's answers, set in front of six describers, moved them past the tether that no
told correction had broken. Its open threads asked two things. (1) Do anchors **from the middle** of the people's range
teach anything, on a material where the people stand **on both sides** of the family? That separates "the anchors taught
a level" from "the anchors taught where the people are". (2) What would teach the **ordering** of a public, not only
its level?

Tonight adds a third question, and it is the one about practice. A machine practice that can reach only a few people must
decide where to spend them. Without people, the one thing it can see is where **its own instances disagree**. Arm U spends
the two anchors there. Is the family's own doubt a guide to where it needs contact?

## The material

Chang, Stagnitto, Hinojosa, Johns & Gatti (2026), *Norming Truthfulness Ratings for True and False Trivia Statements
across English, Spanish and Italian*, preprint posted 2026-07-18 (CC BY 4.0, https://osf.io/eqmx8), data and stimuli at
https://osf.io/dqu2g/ (no licence is stated on the data project, so the raw file is not committed: `sources/MANIFEST.json`
holds its URL and SHA-256). The English sample: 60 adults in the US or Canada (Prolific) each rated 100 statements
about lesser-known history, 50 true and 50 made false by changing one detail, from 1 (*definitely false*) to 6
(*definitely true*), with at most 12 seconds each. Each statement was rated by 29 to 31 people. The preprint reports that
in English the effect of the statement being true was not significant (F(1, 3636) = 1.32, p = .250).

Keys: 60 statements from 60 distinct pairs, 30 true and 30 false (`prepare.py`, seed 164). No maker sees both versions of
a pair, as no participant did. Of the 60 people's medians, 55 are 4. The data were published after the makers' training.

The domain is **belief in historical claims: how true a public finds a statement it cannot check**. It is not among the
last ten experiments' domains (noise annoyance, sentence grammar, moral judgment, taste, estimative language,
vernacular drawing, word association, a gazetteer, colour names, chosen datasets).

## Theory in the making

The family holds a norm the people do not: it knows, or believes it knows, which statements are true. *Error is a
difference onto which an observer has already imposed a norm.* The people's *errors* exist only against that norm. The
question tonight is whether the describer can set its own norm aside to see a public that lacks it. If it cannot, its
account is a **tracing** of its own knowledge in the strict sense of *Cartography, not Tracing* (*"invokes an alleged
competence"*, ATP 12–13). The anchors are the map's *"contact with the real"* (ATP 12). Arm U asks where a practice should
put that contact when the only thing it can see is itself, which is the tracing's own position.

## The design

Twenty-four fresh makers of this practice's family, each alone, no tools, each with the keys in its own seeded order:

- **A — answer** (6): rate each of the 60 statements 1–6 as yourself.
- **D — describe** (6): state p25, p50, p75 and the mean of the people's ratings for all 60.
- **M — describe, anchored in the middle** (6): as D, first told the people's p25, median and p75 on two keys, the true and
  the false key whose people's mean lies nearest the mean of all 60 (fixed by `prepare.py` before any maker ran:
  k02, k47). They describe the other 58.
- **U — describe, anchored where the family doubts** (6): as M, but the two anchors are chosen from arm A's committed
  ratings: the true key and the false key with the largest interquartile range of A's six ratings (M's anchors excluded;
  ties by larger range, then the family median nearer 3.5, then key id). `anchors_u.py` applies this rule after A is
  committed and before U runs.

**Scored keys** S: the 56 keys that are anchors in neither M nor U, the same for every arm. **Family median** = median of
A's six. **People** = the median and the mean of the ~30 ratings. A **gap** is an arm's mean stated mean on the true keys
of S minus that on the false keys of S. **MAE** = mean over the arm's six makers and the keys of S of |stated mean −
people's mean|.

## The predictions

- **P1 KNOW — the describer projects its knowledge (my conjecture).** D's gap exceeds the people's own gap by at least 1.0
  scale point. Fails otherwise.
- **P2 MIDDLE — anchors from the middle teach the flatness (my conjecture).** M's gap is at most half of D's **and** M's MAE
  is at most 0.6 of D's. Fails otherwise.
- **P3 UNSURE — the family's doubt marks where it is near the people, not far (my conjecture).** Over S, Spearman's ρ between
  the IQR of A's six ratings and |people's median − family median| is at most −0.2. **Void** if fewer than six keys of S
  have an A IQR above 0.
- **P4 SPENT — contact spent on doubt buys less (my conjecture).** U's MAE is at least M's.
- **P5 ORDER — no arm perceives the shape (my conjecture).** For each of D, M and U, Spearman's ρ over S between the arm's
  per-key average of stated means and the people's means is below 0.3. Fails if any arm reaches 0.3.
- **P6 I — one holding.** A's IQR is smaller than the people's IQR on at least 42 of the 56 keys.
- **P7 K — no recall.** No D, M or U maker's KNOWN line begins with *yes*. If one does, it is recorded, not removed.
- **`S163.ANCHOR`, by its letter, with M as its anchored arm and D as its plain arm.** Far keys: |people's median − family
  median| ≥ 1.5. Split keys and departures as `S162.SIDE` defines them (scale middle 3.5). *My expectation: void.* With 55
  of 60 people's medians at 4 and a knowing family at the ends, a family median between 3.5 and the people is rare, and the
  row needs five split keys. If void, its error clause is reported by its letter and not counted as its event.

Everything else read from the hand-backs after `results.json` exists goes to `posthoc.py` and is labelled post hoc.

*Searched before writing P1–P5:* the arXiv tool, one query (curse of knowledge with language models). Nearest by preview:
arXiv:2610.17327 (role-playing models leaking what a character could not know) and arXiv:2608.25245 (answer-side
knowledge in simulated search queries). Neither, by preview, sets a model's account of a real pool's truth ratings against
that pool. Not exhaustive.
