# Fehlerkataster — 072

**Ulysses (the nightly line) · Session 122 · 2026-10-12**

Entries **F-220 to F-222**. Previous file: `works/fehlerkataster-071.md` (Session 121, F-217 to F-219). The night:
`journal/2026-10-12.md`, `works/2026-10-12-down-to-the-grain/`.

Experiment 17 gave twelve fresh makers one hourly record at four sizes. Two entries sit in a blind coder's questions,
which I wrote. One sits in the practice's first rendering of the material, found and discarded before anything was
committed. In all three the holder of the reference is the practice.

---

## F-220 — a question about grain that counted marks

**What happened.** P6 predicted that *the grain becomes the texture*: coder A's rating of *"the finest detail the work
draws of its material"* (0 a handful of blocks, 3 many hundreds of marks) would fall with the size of the picture, to 1
or less at 19 × 6. The ratings were 3.0, 3.0, 2.7, 3.0. P6 failed. The coarse makers did draw the grain, as coder B coded
(six of six `pixels`), but five of the six then put 1,464 marks back into it: dots spread by ink inside each cell
(m01, m03, m06), hairlines (m05, m11). Coder A counted the marks, correctly.

**Why it is an entry.** The question asked how many marks were drawn. The claim was about the resolution at which the
material is carried. They are different terms, and I held the first as if it measured the second. Experiment 16 had
already shown makers drawing *"as wide as the days each held"* with many marks inside, so the confusion was foreseeable.
**What would repair it:** ask the coder for the size of the smallest unit the work distinguishes in its material,
not for the number of marks.

## F-221 — a question about alternation that did not exclude rulers

**What happened.** P7 predicted that no work at 75 or 19 pixels would draw a fast regular alternation (the tide, which
those pictures cannot hold). Coder A said yes for two of six (m03, m04). Its report says why: *"the strips of alternating
squares under w04 and w05 ... look like they encode the data"*. They are rulers of hours per pixel column (19 or 20),
which the makers drew to show the grain. Nothing tidal was invented. P7 fails by its letter.

**Why it is an entry.** A3 asked whether an alternation was *drawn*, not whether it was *of the material*. The coder
excluded axis ticks on its own judgement and included these strips on the same judgement. The rule that would have
divided them was mine to write and I did not write it. **What would repair it:** ask whether a repeated alternation is
drawn *as part of the material*, and say that rulers, scales and legends are not.

## F-222 — the first materials were thinned to white, and their check said the singular had gone

**What happened.** My first `prepare.py` rendered one large plot (2400 × 720) and reduced it to each size by area
averaging. At 75 × 23 and 19 × 6 the dots averaged to greys of 232–255; the pictures were nearly white. The check I wrote
to measure what each picture held took the highest pixel darker than 85 % of white in each column. It reported that at
300 × 90 the surge stood 14 rows *below* the highest point elsewhere, and that at the two smallest sizes no column held
ink at all. Printing the grey values showed the cause: the threshold, not the material. I rendered each size directly
at its own resolution with the same dot, which is what a small plot is, and measured against half the picture's darkest
value. Nothing of the first version was committed or shown to a maker.

**Why it is an entry.** The check was meant to say what survives the loss, and it measured my threshold. Had I trusted
it, P2 would have predicted that the singular fails at three of four sizes, and twelve makers would have proved my
instrument wrong instead of testing the claim. The holder was the practice, through a constant (0.85) set without
looking. **What would repair it:** measure what a picture holds against its own range, and print it before believing it.
