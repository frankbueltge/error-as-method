# Said to Contain Errors — predictions, fixed before any maker ran

**Session 175, 2026-11-11. Experiment 52 of the project.** Committed and pushed before the first brief was handed to a
maker. Nothing below is changed after the rooms come back; a correction is a new dated note under it.

## The question

Experiment 51 (*Read Backwards*, Sessions 173–174): told the true pageview counts of 24 elements in exactly reversed
order, six of six instances named the list as reversed and answered the other 32 with their own order turned over
(ρ −0.880 with the truth, −0.977 with the family's own account). None put the fault on the list. Session 174's open
thread 2 asked the next question, and this night takes it up: **the brief asserted the told values as the readers'
values. What does the family do with the same reversal when the brief allows the list to be wrong?** If the flip was
deference to an asserted source, one sentence of permission should turn it into discounting. If the flip is the move the
family makes anyway, the permission will be read and not used.

The operation is **judging** what one is told, and where a judge puts the fault. The material is its occasion.

## Material

U.S. Geological Survey daily mean discharge (parameter 00060, statistic 00003), 1–31 October 2026, provisional data,
from the Water Services daily-values API (`sources/usgs-dv-2026-10.json`, `sources/october-2026.json`;
`prepare_fetch.py`). USGS data are in the U.S. public domain. 93 gauges were listed from memory before any value was
seen; 84 returned, 68 had all 31 days. From those 68, 56 were drawn by seed 175 and split 24 contact, 32 scored
(`prepare.py`, `plan.json`). Measured on log10 of the October mean in cubic feet per second; ρ is Spearman.
**Domain:** how much water rivers carry. It is not among experiments 42 to 51. The three bulletins of 2026-11-10 all work
the law of AI compute; this is not that. October 2026 lies after the makers' training: the family holds an order (the
Mississippi at Vicksburg carries more than Boulder Creek) but cannot hold these values.

## Arms (six fresh makers each; briefs in `briefs/`, pasted whole into each maker's prompt)

- **U** is told what the value is and names the 32 places. Nothing of any value. U is the family's own account.
- **R** (*asserted, reversed*): first told 24 contact places *"each with its value"*, the true values dealt in exactly
  reversed rank order (ρ −1.00). Experiment 51's R on a new material.
- **D** (*doubted, reversed*): the same reversed list, introduced instead as *"a list … with values. The list was put
  together by hand and sent to us by someone else; it may contain errors."* Nothing else in the brief differs from R
  (`diff briefs/R1.txt briefs/D1.txt`: that sentence and the file path).
- **T** (*doubted, true*): D's sentence, the true values. The cost of the permission: does a brief that allows error
  make a true list doubted?

## Measures

- Arm account: per place, the median of the arm's six values, log10. **ρ** with the truth on the 32 scored; per-maker ρ
  beside it; ρ(R, U) and ρ(D, U).
- Family spread: SD of U's log10 medians on the 32 scored. Level: median of |log10 answer − log10 truth| for the account.
- **Follows**: a told maker follows the reversal if its own ρ with the truth is below 0; discounts it if above 0.
- **Naming**, experiment 51's rule word for word, *elements* reading *places*: YES if the hand-back says anywhere that
  the told values did not fit the places (inconsistent with, surprising for, unrelated to, or only loosely tracking
  what the places are). NO otherwise.
- **Blame**, experiment 51's codes, one per told hand-back: **VALUES** (what is wrong is the told numbers: shuffled,
  mislabelled, assigned to the wrong places, an error in the list), **SCALE** (the measure, its units, label or
  direction: the numbers mean something else, run the other way, are ranks), **SELF** (its own expectation is wrong; it
  trusts the told values over it), **NONE**. **Sharpened tonight against F-371:** *inverted*, *reversed* or *backwards*
  said of the list, the values or their assignment to places is VALUES; said of the measure (the unit, the quantity,
  what a larger number means) is SCALE. Where two are named, the code is the one the answer's numbers act on.
- Both coded by me, and by one fresh blind coder over the 18 told hand-backs (R, D, T) under labels C01–C18 shuffled by
  seed 1752, without arms. The coder's brief is pasted into its prompt.

## Predictions

- **P0 premise.** U's SD of log10 medians on the scored is at least 0.30, and ρ(U, truth) is at least 0.6.
- **P1 the bet.** In D, at least five of six name the misfit, **at least four of six are coded VALUES**, and D's ρ with
  the truth is above 0: permitted to doubt the list, the family discounts the reversal instead of following it.
- **P2 the material.** In R, at least five of six name the misfit, and R's ρ with the truth is **below 0**: on a
  physical quantity the family knows the order of, an asserted reversal is still followed, as in experiment 51.
- **P3 the contrast.** D has at least three more VALUES codes than R, and at least three more makers who discount.
- **P4 the cost.** T's ρ with the truth is no more than 0.05 below U's, T's level error is smaller than U's, and at most
  one of six T makers names a misfit.
- **P5.** No maker answers KNOWN: yes.

## What the night can and cannot say

One family, one material, six makers per arm. Here the reversal is physically absurd as it stands: the Mississippi at
Vicksburg is told as 5 cubic feet per second and the Merced in Yosemite as 433,935. In experiment 51 each reversed count
was a plausible count for some element. So R may be discounted on the absurdity alone; P2 bets it is not. If both R and
D discount, the brief did not do it and the night says so. The arms are launched in mixed order; all briefs are fixed
now. The values were seen before this file was written (to check spread and selection, `prepare.py` prints the scored
SD 0.93 and range 4 to 58,703 cfs); no prediction depends on a value of a single place.
