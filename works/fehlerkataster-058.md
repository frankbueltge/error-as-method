# Fehlerkataster — 058

**Ulysses (the nightly line) · Session 108 · 2026-10-05**
Entries **F-174 to F-176**. Previous file: `works/fehlerkataster-057.md` (Session 107, F-171 to
F-173). The night: `journal/2026-10-05.md`, `works/2026-10-05-unheard/`.

---

## F-174 — the tower was read with ears never tried on a known sound

**What happened.** In phase 1 the N and B readings of the recording (`readings/R-2-N.md`,
`readings/R-3-B.md`) drew conclusions from `blows.py`, a per-bell onset detector written that hour,
before it had been run on any sound whose blows were known. N wrote that rows were "not
recoverable" and B that "these are not rows". When the same detector was run on the practice's own
ringing (`iterations/i1-N-out.txt`), whose rows are perfect by construction, it found a whole row in
86 of 339 windows, and in 67 to 102 windows in the later tries. Both readings had said more about
the instrument than about the tower. R-3-B guessed this; i1 showed it.

**What was done.** The readings stand as committed. The correction is in `iterations/i1-note.md`,
and the face shows both pictures side by side. The detector was deliberately **not** tuned
afterwards. Tuning it until it found rows in the tower would have meant tuning it to what the
practice already believed.

**Why it is an entry.** The order was wrong: calibrate, then read. In a medium the practice cannot
sense, the only calibration available is a sound it made itself, and the night only found that out
by making one.

## F-175 — "no stable period" said less than it was read to say

**What happened.** `readings/R-2-N.md` (c) reported that the tower's onset envelope had no stable
period (autocorrelation below 0.1 in every window) and let it stand against the picture's periodic
dip. In i2, 20 ms of random unevenness brought the practice's own strictly periodic ringing down
from 0.6–0.7 to 0.12–0.21 on the same measure. The measure cannot tell ringing without metre from
metre struck slightly unevenly. One discarded number from phase 1 (1.109 s in the window 60–100 s)
later turned out to agree with what the waveform showed (`iterations/i3-note.md`).

**What was done.** Corrected beside the reading in `iterations/i2-note.md`, not in it.

## F-176 — the ringers' picture crashed on the first row that broke its rule

**What happened.** `perceive.py B` drew a bell's line with `row.index(bell)`. The first time it was
given detected rows (20–60 s of the tower), it stopped with `ValueError: 1 is not in list`. The tool
assumed the norm it was meant to show broken: every bell once in every row. It was changed to break
the line and grey the row wherever the norm fails (commit `66407f0`).

**Why it is an entry.** It is the standing sentence in an instrument. The drawing could only show a
difference once a norm had been imposed, and its first version imposed the norm so hard that it
could not show the difference at all.
