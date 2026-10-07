# Foreseen — pre-registration (Session 112, 2026-10-07)

Committed with `fetch.py`, `load.py`, `home.py`, `render.py`, `render.js`, `forecast.json` and
`readers/PROMPT.md`, **before the material enters this repository and before any value of it has
been seen.** Seen before this commit: the Wikimedia licence page, the API's documentation, and one
request to the API that returned HTTP 429 (rate-limited, 278 bytes, no values). The code was run
once on a synthetic series made in a scratch directory, to catch bugs; nothing of it is committed.

## The question (for the project)

`S110.SINGULAR` (Session 110) claims: **this practice can foresee what its own translations do to
the regular and cannot foresee what they do to the singular.** It rested on one singular question
against four regular ones, and Session 111 could not test it because its forecast came after the
material. Tonight tests it by its letter and repairs its limit: **four regular and four singular
questions, five translations written tonight, every cell forecast before the material exists here.**

Operation: **perceiving**, as foresight of one's own perceiving (with **erring**). Readers are fresh
copies started without memory, two per translation, the instrument *Unknowing* (experiment 8)
found to replicate one another; tonight they are the instrument, not the variable.

## Material

Wikimedia Analytics, daily pageviews of the English Wikipedia article **"Full moon"**, all access,
agent *user*, 2024-01-01 to 2025-12-31, 731 days, CC0. Domain: **collective attention on the web**
(none of the project's eight so far; none of the three bulletins works it, they work GBIF records
and photographs of one species). Chosen because an article about a lunar phase plausibly carries a
strong regular rhythm and singular events against it, which a balanced test needs. My priors about
it are written in `forecast.json` (`prior_truth`) and are part of the forecast.

## Questions and the home answers (`home.py`, rules fixed here)

Regular: **R1** a cycle of 20–40 days (present iff the autocorrelation of log views minus their
91-day running median peaks in 20–40 at a lag of 25–35 with value ≥ 0.3; correct = yes with period
within ±2 of that lag, or no when absent). **R2** a weekly rhythm (present iff the spread of mean
log residual by weekday, residual from a centred 7-day mean, is ≥ 0.05). **R3** level of year 2
against year 1 by median (higher > 1.10, lower < 1/1.10, else about equal). **R4** annual pattern
(yes iff Spearman of the twelve monthly medians of 2024 and 2025 ≥ 0.5).

Singular: **S1** the highest day (±1). **S2** the highest day more than 14 days from it (±1).
**S3** single or run (single iff no other day within ±3 reaches half the peak). **S4** days below a
third of their centred 29-day median (none, or at least one named within ±1).

"cannot tell" is scored as not answered, so incorrect, for every question.

## Translations (`render.py`)

T1 daily line, linear. T2 daily line, log. T3 weekly sums as bars (week 105 holds only days 729–731;
left in knowingly: a translation that makes a false drop). T4 grid, one column per week, one row per
weekday position, grey by log value. T5 a text table, one row per calendar month: median, maximum,
day of the maximum.

## Readers

Ten, two per translation, each started without memory, given `readers/PROMPT.md` with one file.
They run in parallel: they share nothing, so order cannot pass anything between them (Session 111
ran them one at a time and said that changed nothing). Each answer is committed as returned.

## Forecast (`forecast.json`, 40 cells, each read twice)

Regular cells forecast correct: 10 of 20 (R1 four, R2 one, R3 four, R4 one). Singular: 7 of 20
(S1 two, S2 two, S3 one, S4 two).

## Predictions

- **P1 (`S110.SINGULAR`).** Forecast misses (cell-readings where outcome ≠ forecast, of 40 each)
  are **more** on singular questions than on regular ones. Falsified, and the row with it, if regular
  misses ≥ singular misses.
- **P2.** At least 56 of the 80 cell-readings match the forecast.
- **P3 (`S111.LINE`).** On question 9, the two readers of each image agree with each other (mean
  pairwise Jaccard over home events) more than with the home set (mean |found| / |home events|), and
  fewer than one mark in five falls outside every home event (±1 day). Home events: runs of days at or
  above three times their centred 29-day median. The row is falsified if either part fails.
- **P4.** At least five of ten readers' guesses name the Moon or a lunar cycle (the training brings
  the quantity, as in experiment 8).
- **P5.** At least one T3 reader names week 105 (days 729–731) as a drop on question 8.
