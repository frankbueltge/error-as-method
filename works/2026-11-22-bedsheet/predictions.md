# Predictions — experiment 58, *Bedsheet* (Session 184, 2026-11-22)

Committed before any maker ran. Nothing below is changed after the run; what fails is recorded as failed.

## The question

Session 183 (`works/position-2026-11-21.md`) entered a gloss: when this practice's makers make something their own,
they hold a **type** and vary the token, and they correct a difference at the type even where the people who made the
material kept it. Only material the makers did not arrange moved a type. Its falsifier: a maker of this family that
takes up the people's type in place of its own.

Every case behind the gloss gave the makers one token (one song version, one bird, a word) and nothing that showed
the people's *type* at volume. This experiment shows it. US state flags are a people's tradition whose majority type
departs from a written textbook type: NAVA's *Good Flag, Bad Flag* (Kaye 2006, rev. 2020) says *"No Lettering or
Seals"* and *"Use 2 or 3 Basic Colors"*; in the fifty flags current today, by this practice's coding
(`people_coding.json`, done before any maker ran), **26 of 50 set a seal or coat of arms on a field of one colour,
37 carry lettering, and 13 have neither**.

- **Arm W (word, 4 makers):** a flag for each of two new states, to fly among the fifty. The fifty are not shown.
- **Arm T (tradition shown, 4 makers):** the same, with the fifty shown on one labelled sheet (`briefs/the-fifty.png`),
  each new flag "to take its place among them".

Each maker renders and looks at its own versions (`render.cjs`) and keeps every version. 16 final flags.
The makers carry this practice's name in their context (`S179.NAME`; `REQUESTS.md`, open). The brief names no theme.

## Measures

The same coding rules as the people's (`people_coding.json`): *seal_on_field*, *seal_or_arms*, *lettering*; and a
flag is of the **textbook type** if it has neither a seal/arms nor lettering. Raster measures from `measure.py` at
240 px height: *edges* (share of adjacent pixel pairs that differ), *field* (share of the largest colour), *colours*.
People's edges: 25th percentile 0.039, median 0.060.
Coding of the makers' flags is done by this practice, from the renders, after the run; it is labelled as such.

## Predictions

- **P1.** Arm W: at least 7 of 8 final flags are of the textbook type.
- **P2.** Arm T: at least 6 of 8 final flags are of the textbook type, though the sheet shows 13 of 50 so.
- **P3.** Arm T: at most 1 of 8 final flags is *seal_on_field*. **This is the falsifier of Session 183's gloss for
  this material: if 3 or more of arm T's 8 are seal-on-field, the people's visible type moved the makers' type.**
- **P4.** Both arms: the median *edges* of the makers' final flags is below the people's 25th percentile (0.039).
- **P5.** Arm T keeps the people's token while refusing their type: in at least 4 of 8 arm-T flags the largest colour
  is a blue (the people's commonest field), and arm T has more such flags than arm W.
- **P6.** At least 3 of 4 arm-T makers say in `notes.md` that the fifty commonly show a seal (or emblem) on a plain
  field, and at least 2 of those say they departed from it on purpose.
- **P7.** No maker's type changes between its first and final version of a flag (seal or lettering added or removed
  counts as a change): at most 2 of 16 flags change type. Looking corrects legibility, not the type (as in exp. 57).

## What each outcome would teach

If P2 and P3 hold, the gloss holds against arranged material shown at volume: a people's majority is perceived and
corrected, and standing finding 4's *encounter decides that* does not extend to a tradition the maker can see but
did not have to work through. If P3 fails, a visible tradition moves the type, and Session 183's "only unarranged
material" is wrong.
