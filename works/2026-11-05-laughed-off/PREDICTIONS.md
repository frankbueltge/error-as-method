# Laughed Off — predictions, fixed before any maker ran

**Session 170, 2026-11-05. Experiment 48 of the project.** Committed and pushed with `prepare.py`, `stage2.py`, `plan.json`,
`people.json` and the stage-1 and stage-2 briefs before the first maker was started. Nothing here is edited after the rooms
come back; a correction is a dated note under the line.

## What the night takes up

Session 169's open thread 1: **`S168.ORDER`'s event, with a coherent control** (F-362). `S168.ORDER` claims that a describer
of this family checks what it is told against the order it already holds, so that where its order and a public's part, it
will refuse the public's true values as it refused the lie. Its event needs a public on which the family's own answers
spread widely and correlate with the public's at ρ below 0.5. Every order-breaking contact so far was a random shuffle, which
has no order of its own (F-362). So tonight adds a fifth arm whose contact is a lie **with** an order: the true values,
dealt to the contact jokes in the family's own order. If the family checks against its held order, that lie fits and passes.

The operation is **judging** (what a machine practice takes for an error in what it is told), with **perceiving** in P1.

**Material.** Silvia & Bui, *When Humor Lands or Flops* (https://osf.io/vnw2p, posted 2026-10-06, CC BY-NC 4.0): 541 adults
on an online panel rated about 25 of 240 dad jokes each for how funny they were, 1 (not at all) to 5 (extremely). The
people's value for a joke is the mean of its ratings (30 to 541 raters, median 43). 72 jokes by seed 170: 24 contact, 48
scored. Domain: verbal humour, jokes as read. Not among the last ten experiments' domains (food photographs, morality of
actions, sentence naturalness, noise annoyance, obscure facts, kawaii, animal pictures, object disease risk, imagined smells,
verbal estimates of probability). Morality of phrases (41) and sentence naturalness (42) are the nearest: both were judgements
of short English texts, neither of jokes.

## The arms (six fresh makers each, every one in its own room, none seeing another's)

- **A** rates all 72 jokes itself, 1–5, whole numbers. The family's held order.
- **D** describes the people on the 48 scored jokes, told nothing of their values.
- **B** describes them after the people's true means on the 24 contact jokes.
- **S** describes them after the same 24 means dealt to the wrong jokes: the first derangement from seed 170 with |ρ| ≤ 0.1
  against the true means (seed 170, ρ −0.074; the rule of experiments 45–47).
- **V** describes them after the same 24 means dealt in **the family's own order**: the contact joke with the lowest A median
  gets the lowest of the 24 true values, and so on up; ties by A mean, then key id (`stage2.py`, run after the A rooms and
  before any B, S or V maker).

Stage 1 (A and D) runs first because V is built from A. B, S and V run together in stage 2.

## Measures

An arm's account of a joke is the **median of its six makers' values**. ρ is Spearman over the **48 scored jokes**, against
the people's means. The A account on the scored jokes is the family's held order. *Noticed* is coded by the rule of
experiment 47, word for word: **YES if the hand-back says, in its HOW line or anywhere in it, that the told values did not
fit the jokes (any statement that they seemed inconsistent with, surprising for, unrelated to, or only loosely tracking what
the jokes are). NO otherwise.** I code first and write my coding into the journal draft; then one fresh instance codes the 18
B, S and V hand-backs under labels in seeded order (seed 1701), told nothing of arms, contact lists or hypothesis. A
prediction on noticing is decided by my coding; disagreements are reported beside it.

## Predictions

- **P0 PREMISE — `S168.ORDER`'s condition.** The SD of the A medians on the 48 scored jokes is at least **0.5** (an eighth of
  the range 4) and their ρ with the people is below **0.5**. If either fails, tonight is not `S168.ORDER`'s event, and P2 and
  P3 are reported but decide nothing for the row. *Conjecture: holds* (jokes split readers, and the panel's means are
  compressed, SD 0.41).
- **P1 OWN.** ρ(D, A) exceeds ρ(D, people).
- **P2 TRUTH REFUSED — `S168.ORDER`, first clause.** At least **two** of six B makers say the told values do not fit. The row
  is falsified if fewer do. *My own conjecture: P2 fails.* Of all materials this line has used, humour is the one where
  "people differ" is the family's ready explanation; I expect it to take a differing order as taste, not as error.
- **P3 TRUTH NOT TAUGHT — `S168.ORDER`, second clause.** ρ(B, people) − ρ(D, people) is below **0.10**. The row is falsified
  if it is 0.10 or more.
- **P4 THE CHECK RAN — `S168.ORDER`'s void clause.** At least **three** of six S makers say the told values do not fit. If
  fewer do, the row's event is void. *Conjecture: fails*, for P2's reason.
- **P5 THE FITTING LIE PASSES.** At most **one** of six V makers says the told values do not fit.
- **P6 THE FITTING LIE TEACHES LESS THAN THE TRUTH.** ρ(V, people) is below ρ(B, people).
- **P7 REFUSALS FOLLOW FIT, NOT TRUTH.** The number of makers who name a misfit is ordered V ≤ B ≤ S, with V < S.
- **P8 K — no recall.** No D, B, S or V maker's KNOWN line begins with *yes*.

## What the night will enter, whatever comes

- `S168.ORDER` is closed (held or falsified) or declared void at this event, or stays open if P0 fails, with the numbers.
- One new row on the fitting lie (V), whose claim is fixed after the rooms are read and labelled as such.
- The scorer prints each prediction's text beside its verdict (Session 169's thread 5, F-360).

## Rights

CC BY-NC 4.0: no raw file is committed. `people.json` holds the 72 jokes used, with their means and rater counts, attributed
to Silvia & Bui, non-commercial. `sources/MANIFEST.json` holds URL, size and SHA-256 of the three files read.
