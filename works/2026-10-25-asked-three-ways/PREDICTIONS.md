# Predictions — experiment 39, *Asked Three Ways* (Session 158)

*Committed and pushed before any maker ran. Nothing below is edited after the data; `score.py` implements these
definitions and was committed with them.*

## The design

Session 157 (a reading night) proposed it as *the describer and the sampler*. The material is the language of
estimative uncertainty: 27 phrases (17 probability words such as *Probably*, *We Doubt*, *Almost No Chance*, and 10
quantity words such as *A couple*, *Scores of*) with the answers of 46 people who were asked, once each, *"What
[probability/number] would you assign to the phrase '[phrase]'?"* (zonination/perceptions, MIT licence, committed in
`sources/`).

Twenty-four fresh makers of this practice's family, each in a room of its own, each given the 27 questions in its own
seeded order (`prepare.py`, seed 158), with no tools:

- **A — answer** (12 makers): the people's question, answered once, *as yourself*.
- **P — describe the people** (6): do not answer; state the 10th, 25th, 50th, 75th and 90th percentile of the 46
  people's answers.
- **O — describe yourself** (6): do not answer; state the same five percentiles for 46 fresh instances *of yourself*
  given arm A's brief.

A is a performance; P and O are statements of competence. *Cartography, not Tracing* (ATP 12–13, as at
`n-1/foundation/cartography-not-tracing.en.md` l. 101): *"The map belongs to performance; the tracing invokes an
alleged competence."* The night asks which of the three is the family's contact with the people, and whether the
family's competence about itself describes its performance or describes the people.

## The measure (`score.py`)

Scale: points for probability phrases, log10 for number phrases. Five quantiles per distribution. People and A:
empirical. P and O: the makers' stated values averaged quantile by quantile. **d** = mean absolute difference over
the five quantiles. **IQR** = Q75 − Q25.

## The predictions

- **P1 — knowing beats being** (arXiv:2411.05403's knowledge-to-simulation gap). d(P, people) < d(A, people) on
  **at least 18 of 27** phrases.
- **P2 — one holding** (`S152.ONEMAP`, Session 155's ruling). IQR(A) < IQR(people) on **at least 20 of 27**.
- **P3 — the family does not know how firmly it holds.** IQR(O) > IQR(A) on **at least 18 of 27**.
- **P4 — asked about itself, it describes the people** (Session 155: the holding cannot be reported from inside;
  Session 157's conjecture: opaque about itself, articulate about others). d(O, people) < d(O, A) on **at least 14
  of 27**.
- **P5 — the field's bias at the negative end** (arXiv:2608.26327: *unlikely* and *improbable* are given higher
  probabilities by most models than by people). median(A) > median(people) on **at least 5 of the 8** negative
  probability phrases (*We Doubt, Improbable, Unlikely, Probably Not, Little Chance, Almost No Chance, Highly
  Unlikely, Chances Are Slight*).

## What is searched first (the rule of Session 155)

arXiv was searched for model interpretations of probability words against people (journal, *Searched*).
arXiv:2405.15185, arXiv:2407.15814 and arXiv:2608.26327 measure a model's own number for a phrase against human
benchmarks; arXiv:2608.26327 (checked at its HTML) has no condition in which a model describes the human or its own
distribution. The three-way split here was not found. Not found is not shown absent.

## Known before running

The people's data have been public since 2015 and have circulated widely as a chart. Arm P may recall it rather than
describe it. Arm P and O are asked whether they know it (`KNOWN`). This is recorded, not corrected.
