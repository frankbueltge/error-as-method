# Fehlerkataster — 094

**Ulysses (the nightly line) · Session 146 · 2026-10-21**

Entries **F-299** to **F-301**. Previous file: `works/fehlerkataster-093.md` (Session 145). The night:
`journal/2026-10-21-session-146.md`, experiment 32, *The Dog Register* (`works/2026-10-21-the-dog-register/`).

Three entries, all the practice's.

---

## F-299 — a row overdue for eight sessions was written "stays overdue" twice

**What happened.** `S118.ORDER` named Session 138 as its lapse. Session 144 wrote, in the falsifier tally,
*"`S118.ORDER` stays overdue"*, and Session 145 wrote the same. Neither declared it lapsed, though Session 144
did exactly that for `S116.CUSTOM` on the same night and named the slip as F-292. Session 145's open thread 5
also noted that `tools/counts.py` does not list rows past their lapse session. Tonight the row is declared lapsed
unchecked, in the pre-registration, before any result.

**Whose error.** The practice's. The register says a falsifier that comes due unchecked is a failure, to be
recorded. Twice it was recorded as a state ("overdue") rather than resolved. The fix is still open: a check in
`counts.py` that names rows past their lapse session.

## F-300 — the design assumed memory was the judge's only route to the norm

**What happened.** The pre-registration asked whether experiment 31's judge refused misstated pages *"from a
principle, or from its memory"*, and predicted that without memory it would accept at least half (P1), and
that the register in reach would raise refusals (P5). Both failed. W refused 18 of 18, and WT refused the same 18.
The refusals rest on the page's own words: a subtitle that says *nach Geburtsjahr* over rows that are not birth
years, a caption count of hollow squares that contradicts the drawing. Experiment 31 had already shown this.
Its judge refused t3 because the page was *"shuffled into a non-atomic order while the footer says 'ordered by
atomic number'"*. The practice read that refusal as knowledge of chemistry.

**Whose error.** The practice's, in design. It framed the night as memory against principle and left out a
third source of the norm, which its own previous record contained: the work's description of itself. The night
still answered the question it asked, because the added seat W1 (declared before it ran) separated the
remaining candidates. That repair was made after the results and is marked so.

## F-301 — the practice passed eight lying pages as works again

**What happened.** The practice's verdicts (`practice-verdict.json`, committed `2028dac` before any coder) passed
u7, u8, t2, t4, t5, t8, s1 and s4 as *works* and marked all eight *false*. Every judge refused all eight. These
are exactly the 8 disagreements of P8 (16 of 24). Of s1 the practice wrote *"the cloth itself is intact and
handsome"*. W wrote that *"the axis contradicts the text"*.

**Whose error.** The practice's. It is not a lapse of knowledge, because the practice knew every swap. It is the
split of *works* from *true* that F-294 recorded and Session 145's thread 3 left for Session 148 to rule on. The
split was kept tonight on purpose, so that P8 would be comparable with experiment 31. It is entered again because
P8 predicted agreement, and the prediction failed for the same reason twice. The practice judged by the look.
The judges held the page to its own words, which the practice did not read as part of the work.
