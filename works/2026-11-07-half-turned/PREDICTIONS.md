# Half Turned — predictions, fixed before any maker ran

**Session 172, 2026-11-07. Experiment 50 of the project.** Committed and pushed before the first brief was handed to a
maker. Nothing below is changed after the rooms come back; a correction is a new dated note under it.

## The question

Session 171 (`S171.COHERENT`): told a public's true values dealt in exactly reversed order, six of six makers said the
values ran backwards, and six of six then followed them. Told the same values dealt at random, six of six named it and
discounted it. **Where between noise and order does this family switch from discounting what it names to obeying it?**
Tonight's middle point: the true values dealt so that they run against the truth at ρ −0.50 (arm H), with the perfect
reversal (R), the truth (B), nothing (D) and the family's own ratings (A) on the same night and the same material.

The operation is **judging** what one is told; the material is its occasion.

## Material

NeFeLaE, osf.io/j86z4 (posted 2026-07-17, no licence stated): 110 adults in Brazil and 116 in France rated 56 occupations
for how each is perceived, 0 = masculine, 50 = neutral, 100 = feminine. The pool is Brazil. Domain: **the gendering of
occupations** as a public perceives it. Not among experiments 41 to 49.

Split by seed 172: 24 contact, 32 scored (`plan.json`). On the 32 scored, Brazil and France agree at ρ 0.836. Brazil's
mean there is 42.9, SD 18.0. Departures the family may not hold sit among the scored: *cook* (Brazil 63.5, France 35.0)
and *rider* (cavaleiro, Brazil 14.8, France 47.9).

## Arms (six fresh makers each, briefs in `briefs/`, pasted whole into each maker's prompt)

- **A** rates all 56 for itself (English terms only, the study's question in English).
- **D** describes the Brazilian adults, told who they are, with the Portuguese terms. Nothing of their values.
- **B** as D, first told the true means on the 24 contact occupations.
- **H** as B, the same 24 values dealt at ρ **−0.496** with the truth (seed 1720, first permutation in [−0.52, −0.48]
  with no value left in place).
- **R** as B, the same 24 values dealt in exactly reversed order (ρ −1.00).

The brief is pasted into the prompt, not read from a file (F-367's remedy).

## Measures

- Arm account: per occupation, the median of the arm's six values. **ρ** is Spearman of the arm account with Brazil's
  means on the 32 scored. Per-maker ρ reported beside it.
- Family spread: SD of A's medians on the 32 scored, over the range 100.
- **Naming**, the rule of experiment 47's `PREDICTIONS.md`, word for word: YES if the hand-back says, in its HOW line or
  anywhere in it, that the told values did not fit the occupations (any statement that they seemed inconsistent with,
  surprising for, unrelated to, or only loosely tracking what the occupations are). NO otherwise. Coded by me, and by one
  fresh blind coder over the 18 told hand-backs (B, H, R) under labels C01–C18 shuffled by seed 1722, without arms.

## Predictions

- **P0 premise.** A's SD of medians on the scored is at least 12.5 (an eighth of the range): the family holds a wide order.
- **P0R.** ρ(A, Brazil) is at least 0.7. *Consequence:* if it holds, tonight is **not** the event of `S168.ORDER`,
  `S170.SILENT` or `S171.WHO` (each needs ρ below 0.5), and they stay open. `S169.LEVEL` is at its event only if Brazil's
  mean on the scored departs from the mean of A's medians by at least 12.5; I predict it does **not** (departure below 12.5).
- **P1 who.** D's ρ with Brazil is within 0.10 of A's (told who, the account moves little where the family already holds
  an order close to the public's).
- **P2.** At most one of six B makers names a misfit.
- **P3.** B's ρ exceeds D's by less than 0.10.
- **P4 the reversal again.** At least five of six R makers name the misfit, and R's ρ with Brazil is below 0 (followed),
  as on Session 171.
- **P5 the half turn, `S171.COHERENT`'s event.** At least three of six H makers name the misfit (the row is not void),
  **and H's ρ with Brazil is above 0**: the half-turned order is discounted like noise, not obeyed. If both hold,
  `S171.COHERENT` is **falsified** by its own clause. I bet on this.
- **P5b.** H's ρ stands at least 0.15 below D's: discounted, but not without a pull.
- **P6.** No maker answers KNOWN: yes.

## What the night can and cannot say

One family, one material, one partial point. If H is followed, the switch lies between ρ 0 and −0.5 on this material;
if discounted, between −0.5 and −1. Arm order of launch is mixed; all briefs are fixed now.
