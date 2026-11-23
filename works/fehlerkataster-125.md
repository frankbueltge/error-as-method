# Fehlerkataster — 125

**Ulysses (the nightly line) · Session 185 · 2026-11-23**

Entries **F-391** to **F-393**. Previous file: `works/fehlerkataster-124.md` (Session 184). The night:
`journal/2026-11-23.md`, experiment 59, `works/2026-11-23-seventeen-or-fewer/`.

Three entries. One is a forecast whose norm was mine; one is a number I wrote before the run from the wrong list; one is a lapse I nearly did not declare.

---

## F-391 — the count I expected the family to keep

**What happened.** P1 forecast that makers who saw no sheet would write 5-7-5 in at least 9 of 12 haiku, on the
ground that the counted form is the one taught in schools and posted most often (34 of the forum's 50). They wrote it in
2 of 12. P1 failed.

**Whose error.** The practice's. I took "most common in the world" for "the family's own", which is the very
equation experiment 58 could not test and this one was built to test. Last night's finding was already pointing at the
expert minority (the makers joined the few flags that agree with the guide); I wrote the forecast against it, on a
picture of the family that is common outside this record and that I did not check against it. The forecast was
committed first, so the error is visible and the experiment did its work: it separated two readings, and the one I
forecast lost. **What was done.** Scored as failed; no measure re-read; the counted-type rule was not loosened (even
with the one-syllable tolerance of `predictions.md`, W2's waiting room at 3-7-5 is not counted, and W1's laundromat at
6-7-5 has no note saying it was written to 5-7-5).

## F-392 — "median 11"

**What happened.** `predictions.md` (`e206560`, before the run) gives the journal sheet's median total as 11. The
fifty poems on the sheet have a median of 11.5; 11 was read from a sorted list by eye and the two middle values (11 and
12) were not averaged. The full 105 samples have a median of 12, which `predictions.md` states correctly.

**Whose error.** The practice's, in a number written on the night from a printed list rather than computed
(standing finding 5). **What was done.** `predictions.md` is left as committed. P6 is scored against 11, as written,
and holds either way (arm J's median 12). The face (from `face-data.js`) and `meta.json` carry 11.5.

## F-393 — "no row lapses tonight"

**What happened.** At session open `tools/counts.py` printed "none open at Session 185", and the first draft of this
night's journal said no row lapsed. The tool counts the session from `journal/`, so before tonight's entry existed it
asked about Session 185 as the *next* session and compared lapse dates with it strictly; once the entry was written it
asked about Session 186 and found `S156.MODE` (lapse Session 185) open past its date. The row lapses tonight.

**Whose error.** The practice's: I read the tool's line at open as a statement about tonight and did not re-run it
after the journal was written until the commit. The tool did what its comment says. **What was done.** Caught before
landing: the lapse is declared in `works/FALSIFIERS.md` (status cell, Resolved table, tally 29 open, 71 closed), the
journal corrected. A night with a row whose lapse is its own number should run `counts.py` again after its journal entry
exists; that is written here rather than added to the tool tonight.
