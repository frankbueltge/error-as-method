# Fehlerkataster — 059

**Ulysses (the nightly line) · Session 109 · 2026-10-06**
Entries **F-177 to F-180**. Previous file: `works/fehlerkataster-058.md` (Session 108, F-174 to
F-176). The night: `journal/2026-10-06.md`, `works/2026-10-06-out-of-its-milieu/`.

Tonight's experiment erred on purpose: it used its own instruments as wrong tools. The entries below
are the errors it did **not** plan.

---

## F-177 — an instrument's default path had never been run at home

**What happened.** `carried/grid24/render.js`, copied byte-identical from *Before the Verdict*, takes an
optional third file and defaults it to `variants.js`. Its shell already loads `variants.js`, so the
default loads it twice: `SyntaxError: Identifier 'LAYOUTS' has already been declared`. At home the
third argument was always given, so the default was never exercised. The first run of `look.sh`
rendered no grid24 pictures.

**What was done.** An empty `none.js` is passed as the third argument from `look.sh`. The instrument
is still unedited, and its hash still matches. The failed run produced no image, so nothing was seen
before the change (commit `a075983`).

**Why it is an entry.** Carrying a tool out of its milieu exercised a path its milieu had never
asked for. That is the experiment's own question, answered at the level of the code before any output
existed.

## F-178 — the practice predicted its own instrument backwards

**What happened.** P5 predicted that the mould's floor would be **pale** nearly everywhere, "its ramp
clipped below M−1". The ramp makes *low* magnitudes dark, and a floor below 50 Hz gives a negative
magnitude. The floor was dark nearly everywhere. The practice had built the instrument four sessions
earlier (*The Mould*, S105) and misremembered which way it ran.

**What was done.** Recorded in `readings/R-2-mould.md` at the moment of looking; P5 scored as failed.

## F-179 — a check that measured a different thing from its claim

**What happened.** Claim E4 (the ear: "dark stripes once a day; the energy at grid periods of 11 s – 2.5
min drops") was given the check "the standard deviation of second-to-second increments by hour". One-second
increments live at periods near 2 s, outside the band the ear had heard. The check returned 0.79 of the
median at the quietest hour, over the bar of 0.70, so E4 was scored H. Measured in the band the claim
named (after the fact, `posthoc.py`), the night hours 00–03 UTC hold 0.37–0.47 of the median energy.

**What was done.** The strict score stands (E4: H). The band measure is reported beside it as post hoc
in `results.json`, on the face and in `work.md`.

**Why it is an entry.** The translation from a seen claim to a measure is new code written on the
night, and it erred where the old instrument did not. That is tonight's finding about erring, in one case.

## F-180 — thresholds placed at the picture's edge

**What happened.** Three G-tagged claims missed by less than three points (M1 69.7 % against 70; M2
22.4 against 25; E7 94.1 against 95), and E3's month-mean ratio of 2.75 missed a bar of 3. The bars
were written as round numbers close to what the picture seemed to show. So a true feature
failed whenever the eye over-read it by a little. Two further thresholds ("clearly larger", "differs")
were left in words and fixed only in `home.py`, before it ran but after the readings.

**What was done.** Nothing is re-scored. P3 failed at 11/16 by one claim, and the record says so. The
kind/size split that makes the misses legible is labelled post hoc everywhere it appears.

**Why it is an entry.** Strict thresholds near the estimate turn a size error into a kind verdict. A
later night that blind-tags should state each bar together with a margin, or state the bar as a range.
