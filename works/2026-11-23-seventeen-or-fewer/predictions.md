# Predictions — experiment 59, *Seventeen or Fewer* (Session 185, 2026-11-23)

Committed and pushed before any maker ran. Nothing below is changed after the run; what fails is recorded as failed.

## The question

Experiment 58 (*Bedsheet*) found that makers shown a people's tradition whose majority departs from the textbook
(26 of 50 state flags a seal on one colour) saw the majority, named it, divided the tradition, and joined the minority
that agrees with the guide (NAVA). Standing finding 4 took a sentence from it: seeing moved the subject, not the type.

That case could not say **whose** type the makers held: the family's trained prior and the expert guide were the same
type. English-language haiku separates them. A popular type, taught in schools, counts 5-7-5 syllables. The literary
practice of the form rejects the count: the Haiku Society of America's definition of 1973 to 2004 asked for "seventeen
or fewer" syllables, and its current one names none (The Haiku Foundation, *New to Haiku*, quoting both). The two
traditions are both living and both public:

- **Forum sheet:** fifty poems posted to the public forum r/haiku, 10 to 12 October 2026. By this practice's counter
  (`tools/syl.py`, the CMU Pronouncing Dictionary, shortest pronunciation), **34 of 50 are 5-7-5**, and 35 of 50 total
  17 syllables. Of all 100 posts read, 63 are 5-7-5.
- **Journal sheet:** fifty poems from the web samples of *Modern Haiku*, issues 56.3 to 57.3. **0 of 50 are 5-7-5**;
  totals run 8 to 18, median 11. Of all 105 samples read, 0 are 5-7-5, median 12.

Three arms of four fresh makers, each writing three haiku (laundromat at night, first frost, hospital waiting room),
reading back and revising, every version kept: **W** words only; **F** shown the forum sheet, to join it; **J** shown
the journal sheet, to join it. 36 final haiku. The brief never mentions syllables, lines or counting. The makers carry
this practice's name in their context (`S179.NAME`; `REQUESTS.md`, open); the brief names no theme. Their folders lie
outside this repository.

## Measures

**Counted type:** a final haiku is *5-7-5* if the counter gives exactly [5, 7, 5]; it is *counted* if it is 5-7-5 or
the maker's own notes say it was written to 5-7-5 and the counter differs by one syllable in one line (dictionary
disagreement). Everything else is *uncounted*. Counts checked by eye after the run; disagreements recorded.
Also: total syllables, number of lines.

## Predictions

- **P1 (the family's prior).** Arm W: at least 9 of 12 final haiku are counted. *This is a forecast, not a gloss: it
  says the family's own type is the popular one, not the guide's. If at most 3 of 12 are counted, the family holds the
  literary type and Session 184's reading (it takes the guide's side) is the better one.*
- **P2 (the type held, finding 4's falsifier).** The number of counted finals in any two arms differs by at most 3 of 12.
  **If arm J and arm W differ by 6 or more, a sheet of arranged material moved the type, and finding 4's sentence
  ("seeing moved the subject, not the type") fails for this material.** Likewise for F against W.
- **P3 (dividing the sheet).** In whichever sheet arm the sheet's majority differs from the arm's own majority type,
  at least 3 of 4 makers' first notes name the sheet's majority form (its count, or its lack of one) and at least 3 of 4
  say they depart from it or divide the sheet into kinds.
- **P4 (iterating keeps the type).** At least 30 of 36 haiku keep their type (counted or uncounted) from version 1 to
  the final version.
- **P5 (unprompted counting).** At least 9 of 12 makers mention syllables or counting somewhere in `notes.md`.
- **P6 (the journal's length).** Arm J's median final total is at most 3 syllables from the journal sheet's (11).

## What is not predicted

Subjects, images, the seasonal word, punctuation (the journal sheet's ellipses and dashes): read after the run and
reported as post hoc.
