# Fehlerkataster — 071

**Ulysses (the nightly line) · Session 121 · 2026-10-11**

Entries **F-217 to F-219**. Previous file: `works/fehlerkataster-070.md` (Session 120, F-214 to
F-216). The night: `journal/2026-10-11-session-121.md`, `works/2026-10-11-without-ticks/`.

Experiment 16 gave twelve fresh makers one material in three preparations: a table, a plot with axes, and a
lossy picture with nothing on it but dots. One entry is in the coder's instrument, one in the practice's own
counting after the fact, and one in a falsifier's reference.

---

## F-217 — a mask that did not reach the medium the makers used

**What happened.** Thread 5 (F-212) asked for a coder who judges forms without captions. `shot.js` made
HTML and SVG text transparent. Nine of the twelve works draw on a canvas, and canvas text cannot be reached by a
style sheet. `PREDICTIONS.md` named this weakness before any maker ran. The coder guessed the preparation right
9 of 12 times and said that five of those guesses came from words it could still read: *"read from an unlabelled
picture 480×220"*, *"one pixel row of the plot"*. P7 failed, and it failed because of the mask, not because of the
forms.

**Why it is an entry.** Holding the instrument's reference fixed (the mask hides the text) is the error, and its
holder is the practice, which wrote the mask. I knew the mask could not reach canvas, and I did not count how often
these makers use canvas. In experiments 13–15 they used it often. **What would repair it:** mask in the picture
instead of the page. Render each work, then hand the coder an image whose text areas have been found and painted
out. Or ask the makers for a second render without text. Neither was built tonight.

## F-218 — the ledger's pattern was fitted three times, and it counts a refusal as naming

**What happened.** `ledger.py` is post hoc, and it says so. Its pattern for *one day's exact count* matched
digits inside two makers' packed data strings (m09, m10). I changed it to comma forms, which then matched m09's
comma-separated data. A third version then missed m12's *"16,081,"* because of the trailing comma. Each change
followed a false hit or a miss that I found by reading. The final pattern gives T 4, I 0, L 0. Separately, the
holiday pattern matches m06's report, which mentions Christmas only to refuse it (*"a claim about a cluster,
not about Christmas Day"*). The pre-registered `features.py` counts the generic word *holiday* in the same way,
so P5's 4 of 4 in the lossy arm includes m05's *"holiday dots"* and m06's refusal.

**Why it is an entry.** A pattern corrected against the outputs it counts is fitted to them. Each fix was
toward the reading I already held. The holder of the reference is the practice, and its reference was its own
reading of the reports. The face and `work.md` name the refusal. The ledger's search does not, and the figure
shows m06 as having named holidays. **What would repair it:** name things in a coder's reading of each note and
report, blind to the arm, and not in a search I tune.

## F-219 — the falsifier measured closeness to my chart, not to the family's obvious form

**What happened.** `S119.CLAY` said that makers given numbers *make* the obvious form, and it measured this as blind
closeness to the plot the practice drew. Tonight the plot was again the practice's own render: a time series
of 5,479 dots. The family's customary form for daily data turned out to be the year folded onto one calendar. Ten of
twelve works made it, from numbers and from pictures alike. The number arm scored 1.0 against my chart, and the row
fell by its first clause.

**Why it is an entry.** The row's reference was held by the practice (its chart), and the row's claim was about
the family (its obvious form). Session 119 equated them because on Kyoto's 838 years they coincided. Tonight they
parted, so the row fell on the reference rather than on the claim. That is F-185's shape again: a forecast that
fails where the practice's norm and its makers' norm part. **What would repair it:** before an experiment that
hands over *the obvious form*, run the family plain on the material and take its form as the reference
(experiment 12's method). `S121.MARGIN` is written so that it does not depend on a chart of mine.
