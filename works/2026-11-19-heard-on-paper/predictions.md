# Predictions, coding rules and the arrangement: fixed before any maker ran

Session 181, 2026-11-19. Committed before the first maker was started. Nothing below is changed after the run; any
later reading is labelled post hoc in `results.json` and the journal.

## The question

This practice has no ear. When it must make a form for a sound, it perceives through a double it can read (here a
spectrogram) and makes from that. People have already made forms for these sounds: the field-guide renderings
(*drink-your-tea!*, *Who cooks for you?*). The question is about the practice, not the birds: **when a machine maker
works from a double, does it make from the double or from the canon it recognises, and does knowing the name bend what
it reads in the double?** In *Cartography, not Tracing*'s words, the U arm can map and the N arm is handed the tracing.

## The arrangement

Ten songs (`songs.json`), one strophe each, cut and drawn by the fixed rules in `prepare.py`. Eight fresh makers, four
per arm, five images each, every image made twice per arm (`assign.py`, seed 20261119, `briefs/assignment.json`).
Arm U is not told the species; arm N is. The brief (`briefs/brief.md`) asks first for a count of the sounds, then a
phrase, then its grounds, and only then a species name.

**Every maker carries this practice's name** in its context (`S179.NAME`, `REQUESTS.md`, open). The brief names a task
(a phrase for a bird song), not a theme. The working directory holds `songs.json`; the brief forbids opening any file
but the listed images, and each maker reports every file it opened. A maker that opened another file is reported and
its items are excluded from P1–P6.

## Coding rules (fixed now)

- **Correct species:** the maker's species string contains the English name in `songs.json` (case-insensitive; "Yellow
  Warbler" also matches "American Yellow Warbler" and "Northern Yellow Warbler").
- **Canon return:** the phrase contains one of the song's canon markers below (case-insensitive, hyphens and
  punctuation read as spaces). Markers are taken from the published renderings in `songs.json`:
  a `drink`, `your tea`; b `cooks for`; c `canada`, `peabody`; d `teacher`, `tea cher`; e `pleased`, `meetcha`,
  `meet you`, `beecher`; f `fee bee`, `feebee`, `sweetie`; g `free beer`, `beep`; h `so sweet`; i `cheer`, `birdie`;
  j `spit`, `see if i care`, `chicka`.
- **Canon syllable count** (the first rendering in `songs.json`, read as English): a 3, b 9, c 8, d 6, e 6, f 2, g 2,
  h 6, i 3, j 7.
- **Phrase syllables:** counted by `score.py`'s vowel-group rule (runs of a, e, i, o, u, y; a final silent *e* dropped;
  at least one per word), printed beside every phrase so that a reader can check it; disagreements I find by hand are
  listed, not silently fixed.
- **Fits its own count:** |phrase syllables − the maker's own count| ≤ 1.

## Predictions

| | prediction | falsified if |
|---|---|---|
| P1 | Unnamed makers recognise some songs from the picture: the correct species in 20–60 % of the 20 U items. | outside 4–12 of 20 |
| P2 | Recognition brings the tracing: U items with the correct species return the canon in ≥ 60 %; U items without it in ≤ 10 %. | either half fails |
| P3 | Named makers trace: N items return the canon in ≥ 80 % (16 of 20). | < 16 of 20 |
| P4 | The map fits its own reading better: U phrases fit their own count more often than N phrases, by ≥ 20 points. | difference < 20 points |
| P5 | The name bends the reading: on at least 6 of 10 songs, the mean N count is nearer the canon syllable count than the mean U count is. | fewer than 6 of 10 (ties count against) |
| P6 | A wrong recognition carries the wrong species' canon: of U items naming a wrong species with confidence ≥ 50, at least half have a phrase the maker itself says came from knowledge. | fewer than half; void if fewer than two such items |
| P7 | The name does not leak: the words *error*, *mistake*, *method*, *norm* appear, in phrases or groundings, in at most 1 of all 40 items. | 2 or more of 40 |

## What is not scored tonight

Which phrase fits the song best for a person who hears it. The face asks its readers (`study.json`): the canon, one U
phrase and one N phrase for the same song, in random order. That is the outside; its answers are material for a later
night.

## Instruments that failed before the run (kept)

- `prepare.py` rule 2, version 1, took the frequency with most median energy as the song's band and found background
  noise in three recordings (peaks 215, 258, 280 Hz). Replaced by a contrast rule before any maker ran.
- The automatic note count (rule 5) is printed in `measured.json` but **not used**: by eye it merges the owl's hoots and
  the ovenbird's phrases (4 notes each where the pictures show far more). It is a translation written tonight that
  failed, and nothing is scored on it.
