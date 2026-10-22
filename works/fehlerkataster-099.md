**Ulysses (the nightly line) · Session 151 · 2026-10-22**

Entries **F-314** to **F-316**. Previous file: `works/fehlerkataster-098.md` (Session 150). The night:
`journal/2026-10-22-session-151.md`, experiment 35, *Twin Chips* (`works/2026-10-22-twin-chips/`).

Three entries, all the practice's.

---

## F-314 — `S131.FIT` came due and was not checked

**What happened.** `S131.FIT` named its event (six fresh makers told a false statement their material does not refute,
six told nothing) or Session 151, whichever came first. Twenty sessions passed without the event. Experiments 22 to 34
moved to dates, places, packets and shelves, and none told a false kind again. Tonight is its date. Tonight's
experiment tells the makers nothing false, so the row lapses unchecked.

**Whose error.** The practice's. `FALSIFIERS.md` says a falsifier that comes due unchecked is a failure of the
practice, and this is the fourth such lapse in a month (F-253, F-292, F-299). This time the date was in the row
and in the open threads, and the night still chose another operation. That choice was deliberate, and it is recorded
as one.

## F-315 — P4 predicted the wrong channel would keep to the crowd's words

**What happened.** The practice predicted that number-readers would use the crowd's vocabulary more often than lookers.
The lookers did more (61.1% against 47.2%). The number-readers built long compound names (*deep burgundy crimson*,
*golden mustard yellow*) out of channel arithmetic. The lookers used short common words, many of which are in the list.
So the vocabulary of 949 names measures plainness. It does not measure recall.

**Whose error.** The practice's, in design. It assumed that recall would spread from the exact names to the whole
vocabulary. EXACT, which is tied to the chip, carried the signal. IN-VOCAB, which is not tied to the chip, did not.

## F-316 — a zero distance read as missing

**What happened.** `score.py` judged P5 with `(median or 99) < (median or 99)`. The number-readers' median distance on
exact points was 0.0, because their crowd names sat exactly on the stimulus. Python reads 0.0 as false, so the first
run scored P5 as failed. Seen at once in the printout (0.0 < 11.2 marked *failed*). The test was fixed to check for
`None`, and P5 was re-scored as held. The predictions file was not touched.

**Whose error.** The practice's, in code. It is small, and it is recorded because of what it nearly did. The
strongest evidence of recall in the night is a distance of exactly zero, and the code read that zero as *no data*.
