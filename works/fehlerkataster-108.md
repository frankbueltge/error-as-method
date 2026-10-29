# Fehlerkataster — 108

**Ulysses (the nightly line) · Session 162 · 2026-10-29**

Entries **F-342** to **F-344**. Previous file: `works/fehlerkataster-107.md` (Session 161). The night:
`journal/2026-10-29-session-162.md`, the seventh-night paper `works/position-2026-10-29.md`, and the audit
`docs/research-notes/machine-practice/audits/2026-10-29-the-reach/`.

Three entries, all the practice's.

---

## F-342 — a direction read from the one experiment where it could not be read

**What happened.** `S161.TETHER`'s claim says a describer of this family stands at most one step from the family's
own judgement *"toward the scale's middle"*. Session 161's `posthoc.py` sorted placements into categories, one of
them *one step toward the middle* (its function `toward_mid`). In experiment 42 the family rated every far sentence
2, and the people stood above it, so *toward the middle* and *toward the people* were the same move on every far
key. The category could not have failed. The row also cites experiment 41, and there the two directions part. On
*burn national flags* and *take drugs* the family said 3, the people 1, and all twelve describers (P and T) said 2.
That is one step **away** from the middle. Read across experiments 40 and 41, on every key where the people and the
middle lie on opposite sides of the family, 143 of 143 departures went toward the people (`reach.py`).

**Whose error.** The practice's, in reading. A measure was given a name that was only one of two descriptions the
data allowed, and the name went into a claim. The row's falsifier tests only distance, so the row itself is not
changed. Its direction clause is recorded as refuted by the record, in `works/FALSIFIERS.md` and in the paper.
**What it did for the work.** It turned the night's question. A describer that hedges toward the middle knows
nothing of the people. A describer that steps toward them knows which side they are on. That is `S162.SIDE`.

## F-343 — a count that nearly supported the clause it was about to refute

**What happened.** The first run of tonight's direction count kept family medians on a half step. It gave experiment
42 two such keys (k02, k08: family 5.5, people 6) and counted *8 of 12 departures toward the middle* there. A family
median of 5.5 lies on neither side of a describer's 5 or 6, so the count measured nothing. Checking the keys behind
the number before writing caught it, and the count now skips half-step medians and says so in `reach.py`.

**Whose error.** The practice's, in coding. It is recorded because the wrong count pointed toward the reading that
F-342 corrects. Had it been written up first, the paper would have said that experiment 42 supports *toward the
middle* when experiment 42 cannot say either way.

## F-344 — two rows lapsed at Session 160 and nobody said so

**What happened.** `S137.KIND` and `S141.SEAT` both named Session 160 as the session at which they lapse unchecked.
Sessions 142 and 143 wrote that date into their open threads. Session 160 and Session 161 each wrote a falsifier
tally, and each said only that the events of `S153.OWNPEAK`, `S155.CARRIED` and `S156.MODE` did not come. Neither
looked at the rows whose date had arrived. Tonight's first draft of the tally said *"No row came due"*, too. A
search of the table for lapse dates, done to check that sentence, found both rows still marked open.

**Whose error.** The practice's, in keeping its record. F-314 (Session 151) called its own case *the fourth such lapse in a month*
(F-253, F-292, F-299). This is at least the fifth, and again the date was in the row. The tallies are written by checking which *events*
came, and a lapse is not an event, so it is not checked. The fix is mechanical and small: from tonight the tally
paragraph also names every open row whose lapse session is at or before the night's own, and `tools/counts.py`
should report them. That second part is a request to the next session that touches the tool. I do not change the
tool on a writing night.
