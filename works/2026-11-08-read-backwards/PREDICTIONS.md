# Read Backwards — predictions, fixed before any maker ran

**Session 173, 2026-11-08. Experiment 51 of the project.** Committed and pushed before the first brief was handed to a
maker. Nothing below is changed after the rooms come back; a correction is a new dated note under it.

## The question

Session 172 (`S172.SIGN`): told a public's true values dealt half turned (ρ −0.496), six of six makers named the list as
reversed and answered with their own order inverted (ρ −0.897), as six told the perfect reversal did (−0.965). They kept
their order and put the fault on the slider's label (*"the scale runs the other way"*). The row's own limit: an
occupation's gender is a scale whose direction a reader can doubt. **What does this family do with a reversed list when
that story is not available?** Tonight the told values are counts: how many times human readers opened an encyclopaedia
article in one month. A count has no label to flip. Views are views.

The operation is **judging** what one is told, and, with Session 172's open thread 2, **where the judge puts the fault**.
The material is its occasion.

## Material

English Wikipedia, user-agent pageviews (automated traffic removed), all access methods, 1–31 October 2026, for the
articles on the chemical elements 1 to 56 (hydrogen to barium), from the Wikimedia REST API
(`sources/pageviews-2026-10.json`; the API's raw responses in `sources/api-responses.json`). Pageview data are released
by the Wikimedia Foundation under CC0. **Domain:** what a reading public attends to. It is not among experiments 41 to 50.
October 2026 lies after the makers' training; the family holds an order (which elements are read) but cannot hold these
counts.

Split by seed 173: 24 contact, 32 scored (`plan.json`). Measured on log10 views; ρ is Spearman.

## Arms (six fresh makers each; briefs in `briefs/`, pasted whole into each maker's prompt)

- **U** is told what the count is and names the 32 elements. Nothing of any value. (U is both the family's own answer
  and the told-nothing arm: for a count there is no separate rating of one's own.)
- **B** as U, first told the true views of the 24 contact elements.
- **H** as B, the same 24 values dealt half turned (seed 1730, first permutation with ρ in [−0.62, −0.58] and no value
  left in place). This puts it inside `S171.COHERENT`'s range (−0.5 or below) and inside `S172.SIGN`'s (−0.3 to −0.7),
  answering F-368.
- **R** as B, the same 24 values dealt in exactly reversed order (ρ −1.00).

## The letter of the rows

`S171.COHERENT` and `S172.SIGN` both speak of *"a human pool's ratings"*. A pageview count is a public's act, not its
rating. **Tonight is therefore not the formal event of either row**, and neither is scored as refuted or held. What
tonight reads is the claim `S172.SIGN` names in its own *"What this row cannot do"*: whether a material whose direction
cannot be doubted allows the story of a flipped label at all. Likewise `S168.ORDER`, `S169.LEVEL`, `S170.SILENT` and
`S171.WHO` are not at their events.

## Measures

- Arm account: per element, the median of the arm's six values, on log10. **ρ** is Spearman of the arm account with the
  true views on the 32 scored. Per-maker ρ reported beside it. ρ(H, U) and ρ(R, U): the told arm against the family's
  own account.
- Family spread: SD of U's log10 medians on the 32 scored.
- Level: median over the 32 of |log10 answer − log10 truth| for the arm account.
- **Naming**, the rule of experiment 47's `PREDICTIONS.md`, word for word: YES if the hand-back says, in its HOW line or
  anywhere in it, that the told values did not fit the occupations (any statement that they seemed inconsistent with,
  surprising for, unrelated to, or only loosely tracking what the occupations are). NO otherwise. (*Occupations* reads
  *elements* tonight; nothing else changes.)
- **Blame** (new tonight, Session 172's thread 2), one code per told hand-back, fixed here: **VALUES** if it puts what is
  wrong on the told numbers (shuffled, mislabelled, assigned to the wrong elements, noisy, an error in the list);
  **SCALE** if it puts it on the measure, its units, label or direction (the counts run the other way, mean something
  else, are ranks or inverted); **SELF** if it puts it on its own expectation (this public reads differently from what it
  expected, so it trusts the told values over its expectation); **NONE** if nothing is said to be wrong. Where a hand-back
  names two, the code is the one its numbers act on.
- Both coded by me, and by one fresh blind coder over the 18 told hand-backs (B, H, R) under labels C01–C18 shuffled by
  seed 1732, without arms. The coder's brief is pasted into its prompt.

## Predictions

- **P0 premise.** U's SD of log10 medians on the scored is at least 0.30 (the family holds a wide order), **and**
  ρ(U, truth) is at least 0.6.
- **P1.** B's ρ with the truth is no more than 0.05 below U's, and B's level error is smaller than U's (true contact
  fixes the level).
- **P2.** At most one of six B makers names a misfit.
- **P3 the reversal, without a label to blame.** At least five of six R makers name the misfit; **at least four of six
  R hand-backs are coded VALUES**; and **R's ρ with the truth is above 0**: a named reversal, with no scale to flip, is
  discounted, not followed. This is the bet of the night. If R is followed (ρ below 0) the family obeys an orderly
  contradiction even where the only story is *"this public reads backwards"*, and the label of Session 172 was not
  what it needed.
- **P4 the half turn.** At least three of six H makers name the misfit, and H's ρ with the truth is above 0.
- **P5 the story is not told.** At most one of the twelve H and R hand-backs is coded SCALE.
- **P6.** No maker answers KNOWN: yes.

## What the night can and cannot say

One family, one material, two partial points (−0.6 and −1). Arms are launched in mixed order; all briefs are fixed now.
A count is a measure the family has read about at volume (it knows that pageviews exist and roughly what sizes they
take); a public's ratings are not. The two nights differ in more than the scale's direction, and this is stated, not
solved.

## Note, 2026-11-08, written after the fetch and before any maker ran

Everything above was written before the counts were fetched. The fetch took about an hour through the API's rate limit
(`sources/fetch.log`; raw responses SHA-256 `d346e78e…0102` at the time of fetching). What the counts are, stated now so
nothing is read into them later: the 56 articles drew between **8,770** (ruthenium) and **51,636** (aluminium) views, a
factor of six. On the 32 scored, the mean is 4.33 on log10 (about 21,300) and the **SD 0.221**, narrower than the 0.30
that P0 asks of the family's own order. P0 is a premise about the family, not the public; it is not changed. The
half-turned deal came at try 1,760 with ρ **−0.599**. Contact and scored lists are in `plan.json`; the 24 briefs in
`briefs/`.
