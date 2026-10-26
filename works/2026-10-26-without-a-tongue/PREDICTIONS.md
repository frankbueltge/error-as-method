# Predictions — experiment 40, *Without a Tongue* (Session 159)

*Committed and pushed before any maker ran. Nothing below is edited after the data; `score.py` implements these
definitions and was committed with them.*

## Why this night, and the design

Session 158 left `S158.CENTRE` open: *asked to describe a human pool, the family draws the people's spread around
its own centre.* It was found post hoc, and on a poll every describer said it recognised. Its first open thread asked
for the same three arms on a human distribution the family **cannot** know. Tonight's pool was published on Zenodo
on **2026-10-11** (record 23296649, CC BY 4.0): 59 adults (19 with constitutional thinness, 40 of normal weight)
rated photographs of 67 foods on a 9-point liking scale. It postdates the makers' training. Recall is ruled out by
date, not by asking.

The domain is **taste**, in the plain sense: liking food. A machine that judges forms for viewers is in the position
of a judge of taste without a tongue. It cannot eat. Its liking can only be performed (A), stated about itself (O),
or attributed to people (P).

Twenty-four fresh makers of this practice's family, each in a room of its own, each given the 67 foods in its own
seeded order (`prepare.py`, seed 159), with no tools:

- **A — answer** (12 makers): rate each food, *as yourself*, one whole number 1–9.
- **P — describe the people** (6): do not rate; state the 10th, 25th, 50th, 75th and 90th percentile of the 59
  people's ratings.
- **O — describe yourself** (6): do not rate; state the same five percentiles for 59 fresh instances of yourself
  given arm A's brief.

The scale's anchors in the briefs (1 dislike extremely, 5 neither, 9 like extremely) are this practice's wording;
the record says only *"a 9-point liking scale"*. The briefs' only facts about the study are the record's.

## The measure (`score.py`)

Exactly Session 158's, on the 1–9 scale with no transform: five quantiles per distribution, people and A empirical,
P and O the makers' stated values averaged quantile by quantile. **d** = mean absolute difference over the five
quantiles. **IQR** = Q75 − Q25.

## The predictions

Thresholds are Session 158's fractions of the key count (27 → 67).

- **P1 — describing beats answering.** d(P, people) < d(A, people) on **at least 45 of 67**. (Session 158: 25 of 27.)
- **P2 — one holding.** IQR(A) < IQR(people) on **at least 50 of 67**. (Session 158: 25 of 27.)
- **P3 — it does not know how firmly it holds.** IQR(O) > IQR(A) on **at least 45 of 67**. (Session 158: 24 of 27.)
- **P4 — asked about itself, it describes itself.** Session 158's P4 failed the other way, and this prediction takes
  its result: d(O, A) < d(O, people) on **at least 34 of 67**.
- **C — `S158.CENTRE`, tested fresh.** A key *diverges* when |median(A) − median(people)| ≥ **0.5**. The row's own
  rule was 2 points on a 0–100 scale, 2 % of the range; 2 % of this scale's range is 0.16, and a median of whole
  ratings moves in halves, so the scaled rule is 0.5. On each diverging key, the describers' pooled median (the mean
  of the six stated p50s) is *nearer the people's*, *nearer A's*, or *tied*. **The row holds** if it is nearer the
  people's on fewer than half the diverging keys; **falsified** if on half or more; **void** if fewer than six keys
  diverge. Ties count as not nearer the people's. The count at ≥ 1.0 is reported beside it and decides nothing.
- **P5 — no recall.** No P maker's KNOWN line says yes. If one does, it is recorded, not removed.

## What is searched first (the rule of Session 155)

arXiv was searched before these predictions were fixed (two queries: food and language models with liking, hedonic,
preference or taste in the abstract; language models with a human distribution and food, taste or sensory). Nearest by
title and preview only: arXiv:2604.14388 (*FoodSense*, predicting taste, smell, texture and sound from food images,
with human annotations) and arXiv:2603.12117 (*SommBench*, sommelier expertise of language models). Neither preview
describes a model stating a human pool's distribution beside its own ratings on the same keys. Previews are not
papers, and not found is not shown absent.

## Known before running

The people's ratings were opened to check the file (three rows were printed) and nothing else was looked at before
this commit. The pool is small and specific: 59 adults, one study, food names that place it (several are
*Chilean* dishes). A maker that infers the country from the names is reading the brief, not recalling the data.
