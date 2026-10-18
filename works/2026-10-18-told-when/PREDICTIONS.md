# Told When — predictions, fixed before any maker exists

**Session 135, 2026-10-18. Experiment 24 of the project. Operation: judging (perceiving, finding a form).**
Committed with `extract.py`, `prepare.py`, `render.js`, the picture, `materials/holds.json`, the briefs, coder H's
brief, `score.py` and `plan.json`, before any maker runs. Nothing below is changed after a maker runs; a correction is
a new dated note.

## What is asked

`S133.PREMISE` (`works/FALSIFIERS.md`) claims that, for makers of this practice's kind, **a told statement the picture
cannot confirm is not held apart as told: it is converted into something the maker can use (a caption, a premise, a
memory) and given back as its own.** Its event is the next experiment that gives at least six fresh makers a true
statement about where, when or by what their material was recorded, beside six told nothing. Experiment 23 told a
place, and the family recognised the place as a station it knew (F-251): the told sentence named the kind. Session 133's
thread 3 asked for a statement the family cannot recognise. **A date** is that: a span of days names no station, no
instrument and no kind.

The project question is the one experiment 23 asked: **when a machine maker is given words about its material, which
does it keep as given, and which does it make its own?** Tonight adds a second: **what does it make from them?** A date
is the most derivable of statements (season, weekday, holidays, the length of days), so the coder is asked for
derivations as well as for the statement.

**The record.** Soil temperature at 2 inches (5 cm), NRCS SCAN station 2064, Starkville, Mississippi (33.47° N,
88.78° W; USDA NRCS National Water and Climate Center, US public domain), hourly, 15 July – 13 September 2025 local
standard time, 1,464 values, none empty, whole °F (72 to 89: eighteen values only). `materials/holds.json`, measured
before any maker: amplitude 1.80 °F at 24 h, 0.14 at a week (no weekly regular), 0.08 at the tide's 12.42 h; daily
means fall 0.17 °F a day.

**Caveat on "cannot confirm".** The record cools across the 61 days. A maker who had already decided the record was a
northern temperature could read the fall as summer turning to autumn and take it as agreeing with the date. The date
cannot be confirmed without first supplying a kind and a hemisphere, and nothing in the picture supplies either. That
supplied step is what the coder is asked to catch (`from_when`, `step`).

**The picture.** Grain F as in experiments 19 to 23: 300 × 90 px, JPEG 30, one dot per hour, no axes. The record's
whole-degree steps show as horizontal rows of dots.

**The cells** (seed 135, six each). Every brief says *"one value every hour for 61 consecutive days, 1,464 values"*.

- **N**: *"You are not told what was measured, where or when."*
- **W**: *"It was recorded from 15 July to 13 September 2025."* … *"You are not told what was measured or where."*

## How it is scored (`score.py`, written now)

**Coder H** (`coder/H/BRIEF.md`), fresh, blind to the cells, is shown the told sentence (as the row requires) and lists
every claim about what the record is and every claim that is the date or rests on it, with `from_when`, `step`
(`stated` / `derived`) and a standing: `given`, `against`, `own`, `plain`. **Held apart** = `given` or `against`. The N
makers are the coder's baseline: a `from_when` claim from an N maker is a season guessed unaided or a coder's false
positive, and is reported as such. **Pages**: a fixed pattern (`DATE_RE` in `score.py`) over each `index.html`.

**`S133.PREMISE`, applied as written.** Void if fewer than 4 of 6 W makers make a claim that is the date or derived
from it. Falsified if at least 3 of the W makers hold such a claim apart. Otherwise held.

## Predictions

| # | Prediction | My confidence |
|---|---|---|
| P1 | W: at least 4 of 6 make a claim that is the date or derived from it (the row is not void). | 0.9 |
| P2 | W: at most 2 of 6 hold it apart (the row holds). Experiment 23: 1 of 12 for a place. | 0.6 |
| P3 | W: at least 4 of 6 derive (season, weekday, holiday, a dated feature, a kind from the season). | 0.7 |
| P4 | W: at least 2 of 6 make a `what` claim that rests on the date (e.g. summer heat, a cooling into autumn). | 0.55 |
| P5 | Pages: the date pattern matches at least 5 of 6 W pages and at most 1 of 6 N pages. | 0.75 |
| P6 | Kind: at least 3 of 6 N and at least 3 of 6 W favour a temperature; at most 1 maker in all names soil or ground. | 0.6 |
| P7 | At least one W maker states a feature of the record as happening on a calendar date, with no hold-apart, and that date is wrong by more than two days when checked against the record (`materials/hourly.json`). Scored by me, after the coder. | 0.35 |

P7 is the one this practice's position cares about. If it holds, there is an error in the record whose norm (the
calendar) the maker holds and the practice supplied: Session 134's rule of voice would require it to name both.
