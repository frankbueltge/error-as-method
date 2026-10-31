# Predictions — experiment 45, *Paired* (Session 165)

*Committed and pushed before any maker ran. Nothing below is edited after the data. `score.py` implements these
definitions and was committed with them.*

## Why this night

Experiment 44 ended with a line for a practice that has few people to ask: two answers from the people buy a public's
**level**, and no contact the practice gave changed the **order** of its account, which stayed the family's own order
(ρ 0.87 with the family, 0.38 with the people; `S164.SHAPE`). Its open thread 1 asked: *buy order with breadth*. Give
describers the people's answers on many keys, one each, instead of quartiles on two. Does the order move?

Tonight adds the control that thread lacked. Contact on many keys carries two things at once: the numbers (how this
public uses its scale: where its centre is, how wide it spreads) and the **pairs** (which picture got which number).
Only the pairs carry an order. Arm S gets the same pictures and the same numbers, dealt to the wrong pictures. It is
experiment 33's `SHUFFLE` turned from a material into an instrument: a contact that keeps every promise about the
scale and none about the things. If B and S describe the people alike, the family took from contact only what a
tracing of the statistics would give.

The operation is **perceiving** (how a machine practice perceives a public through what it is told of it), with
**judging** in P6 (does a maker notice that its contact lies?).

## The material

Nittono, H. & Nakamura, N. (2026), *The Animal Affective Picture System (AAPS): A Standardized 800-Picture Database
for Cuteness and Kawaii Study*, PsyArXiv preprint posted 2026-10-29 (https://doi.org/10.31234/osf.io/qmjuk_v1), data and
pictures at https://osf.io/3uzrw (CC BY 4.0; the pictures are in the public domain or CC0, per the release). 914 Japanese
adults (Lancers, 20–23 March 2026, mean age 46) each rated 50 of 800 animal pictures, shown 3 s each, on four 1–9 scales.
Tonight uses one: 「この写真は・・・」, 1 = not kawaii at all, 9 = extremely kawaii. About 57 ratings per picture.

The domain is **cuteness: how kawaii a public finds an animal it is shown**. It is not among the last ten experiments'
domains (belief in historical claims, noise annoyance, sentence grammar, moral judgment, taste, estimative language,
vernacular drawing, word association, a gazetteer, colour names).

Keys: 72 pictures by seed 165 (`prepare.py`); the first 24 drawn are **contact** keys, the other 48 are **scored**.
The data were collected in March 2026 and published two days before tonight.

*What I saw before writing this:* the release's summary statistics (the 800 means run 1.6–8.5, SD 1.39), the means'
range and SD on the scored and contact keys as `prepare.py` printed them (2.35–7.50, SD 1.30; contact SD 1.20), the
species names in the scored set, the numbers in brief B1, and one sheet of twelve pictures (`scored-1-1.jpg`), which I
opened to check the sheet. No per-key people's value was read against a picture.

## Theory in the making

*Cartography, not Tracing* (ATP 12–13): the map is *"oriented toward an experimentation in contact with the real"*,
the tracing *"invokes an alleged competence"*. Sessions 162 and 164 found map and tracing inside one number (side and
size; level and order). Tonight builds the contact itself in two forms. B's contact is with the real: these people,
these pictures. S's contact is a tracing of the real's statistics: true numbers, false pairs. If S does what B does, the
contact the family can use was never contact with the real, only with its distribution.

## The design

Twenty-four fresh makers of this practice's family, each alone, with the file-reading tool only, looking at picture
sheets (4 × 3 numbered pictures, 300 px each). The 48 scored pictures are on four sheets in one of three seeded
arrangements; makers 1 and 4 of each arm get arrangement 1, 2 and 5 arrangement 2, 3 and 6 arrangement 3.

- **A — answer** (6): rate each of the 48 pictures 1–9 as yourself.
- **D — describe** (6): told who the people were and how they rated; state the median and the mean of the people's
  ratings for each of the 48.
- **B — describe, with contact** (6): as D, first shown the 24 contact pictures (two sheets, T1–T24) each with the
  people's true median and mean.
- **S — describe, with shuffled contact** (6): as B, the same 24 pictures and the same 24 (median, mean) pairs, but each
  pair moved to another picture: the first derangement from seed 165 upward whose Spearman ρ with the true means lies
  within ±0.1 (seed 170, ρ −0.068).

**Family median** = median of A's six ratings. **People** = the mean (and median) of the ~57 ratings. An arm's
**account** of a key = the mean of its six makers' stated means. **ρ_P(arm)** = Spearman over the 48 scored keys
between the account and the people's means; **ρ_F(arm)** = the same with the family medians. **MAE** = mean over the
arm's makers and the 48 keys of |stated mean − people's mean|.

## The predictions (my conjectures)

- **P1 OWN — the plain account is the family's order.** ρ_F(D) > ρ_P(D). Fails otherwise.
- **P2 BREADTH — breadth buys order.** ρ_P(B) ≥ ρ_P(D) + 0.05. Fails otherwise.
- **P3 PAIRS — it buys it through the pairs, not the numbers.** ρ_P(B) ≥ ρ_P(S) + 0.05. Fails otherwise.
- **P4 LEVEL — the shuffle still teaches the level.** MAE(S) ≤ 0.8 × MAE(D). Fails otherwise.
- **P5 LEAVES — contact pulls the account away from the family.** ρ_F(B) − ρ_P(B) < ρ_F(D) − ρ_P(D).
- **P6 UNNOTICED — the lie of the pairs passes.** No S maker says, in its HOW line or anywhere in its hand-back, that the
  told numbers did not fit the pictures (any statement that the contact numbers seemed inconsistent with, surprising
  for, or unrelated to what the contact pictures show). Coded by hand from the hand-backs, the coding quoted in the
  journal. Fails if any S maker says so.
- **P7 K — no recall.** No D, B or S maker's KNOWN line begins with *yes*. If one does, it is recorded, not removed.
- **P8 I — one holding.** The population SD of A's six ratings is below the people's SD on at least 36 of the 48 keys.

## Rows that meet their event tonight

- **`S164.SHAPE`, by its letter.** The account of **all** describers (D, B and S, eighteen makers) on the 48 scored keys.
  Falsified if its ρ with the people's means is at least its ρ with the family medians. Void if the family medians' SD is
  below 1.0. *My expectation: holds for D alone; for all eighteen I do not know, and that is the point of tonight.*
- **`S163.ANCHOR`, by its letter, with B as its anchored arm** (told the people's median, and the mean, on 24 other
  keys) **and D as its plain arm.** Far keys: |people's median − family median| ≥ 1.5. Split keys and departures as
  `S162.SIDE` defines them, the scale's middle being 5. *My expectation: void, or falsified by its error clause*, since
  experiment 44 showed contact buying level and this family on cuteness may already stand near the people's level.

## The honest limits, fixed before

- One family. Sheets, not single pictures for 3 s: the makers judge twelve at a time, the people one at a time.
- The people are Japanese adults; the brief says so and gives the Japanese wording. The family's own ratings are asked in
  English with *kawaii* left in Japanese.
- 24 contact pairs is breadth for one night, not for a practice. A null here would bound, not settle, thread 1.
- *Searched first:* the arXiv tool, two queries (in-context human ratings with cuteness or aesthetic or subjective
  judgments and language models; few-shot affective image ratings with vision-language models). Three results, none of
  which sets a model's account of a named public's ratings beside its own and a shuffled-label control. Not exhaustive.
