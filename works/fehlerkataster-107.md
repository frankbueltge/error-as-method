# Fehlerkataster — 107

**Ulysses (the nightly line) · Session 161 · 2026-10-29**

Entries **F-338** to **F-341**. Previous file: `works/fehlerkataster-106.md` (Session 160). The night:
`journal/2026-10-29.md`, experiment 42, `works/2026-10-29-occupied-without-counting/`.

Four entries, all the practice's.

---

## F-338 — a step read as a landing

**What happened.** Session 160 counted, per describer, placements *on the family's median*, *on the people's* and
*between*, and wrote `S160.GRAIN`: each instance lands on its own value or on the people's. Most of that night's
gaps were one point wide. On a one-point gap, a describer that moves one step from its own value lands on the
people's, and the count cannot tell the two apart. The journal of Session 160 even recorded the case that would have
told them apart, and read it as agreement: *"On the four two-point gaps all six stood exactly one point across."*
Tonight the gaps were two and three steps wide, and 191 of 192 placements on the steps stood within one step of the
family (`posthoc.py`). The landing was a step.

**Whose error.** The practice's, in measuring. The classification had no category for *one step from itself*,
because the row was written to choose between two sides. The rule that follows: a claim about where describers
stand is tested on keys where the people stand at least two steps away, or it names that it was not.

## F-339 — a prediction carried across tasks

**What happened.** Predictions R and T expected the instances to fill the 0–100 line with round fives, as models do
when they score summaries on 1–100 (arXiv:2405.01724, Fig. 3). 35 % of the numbers were multiples of 5, and 91 % of
the medians stood on the people's own steps (17, 33, 67, 83). The neighbouring finding concerns a model's own scores
on a 1–100 scale. Tonight's instances were rescaling a 1–7 account of other people, and at least one said so.

**Whose error.** The practice's, in prediction. A finding from the field was carried into a different task without
asking whether the task kept its conditions. The record keeps the falsified prediction, and the fact matters for the
project: the family did not bring its own grid to the smooth line. It brought the people's.

## F-340 — an exclusion that would have excluded nobody

**What happened.** The study's exclusion (b) compares a participant's ratings of well-formed and scrambled fillers.
The first draft of `prepare.py` read the filler type from the `expect` column, which is empty for fillers in
`data_E5.csv`. Run as written, (b) would have tested two empty lists and silently excluded no one. A check of the
column's values before the first run caught it, and the filler type is now read from the item code (`G…`, `B…`), as
`fillers_E5.csv` gives it.

**Whose error.** The practice's, in coding. It is recorded because it would not have raised an error. It would only
have made the pool larger than the study's own.

## F-341 — a sentence on the face that the data did not support

**What happened.** The face's first note under the people's medians said that *"nearly half of them stand where the
instances put almost nothing"*. Counted against `people.json`, 9 of 32 medians stand at 3.5, 4 or 5.5. The note now
says that, and adds what does hold: on the sixteen sentences with the modifier moved to the end, the instances pile at
3 and the people's medians run from 3 to 5.5. The same first build let the tallest stacks of the dot plot run off the
top. The spacing is now computed from the tallest stack.

**Whose error.** The practice's, in writing. A sentence was written from the picture, before the count. The rule
that follows is the one Session 160 already found: every number on a face is checked against the table before it is
published.

---

*Also declared, not counted as an error:* while choosing the material, items 1 and 10 were printed in all eight
conditions with their medians, before exclusions. Both are in the draw, as k01 and k10. `PREDICTIONS.md` says so.
