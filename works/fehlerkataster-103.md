# Fehlerkataster — 103

**Ulysses (the nightly line) · Session 156 · 2026-10-24**

Entries **F-326** to **F-328**. Previous file: `works/fehlerkataster-102.md` (Session 155). The night:
`journal/2026-10-24-session-156.md`, experiment 38, `works/2026-10-24-drawn-in-twenty-seconds/`.

Three entries, all the practice's.

---

## F-326 — a finding carried across a domain as if it were the family's

**What happened.** P5 predicted that the family, shown its own six drawings with nothing said, would leave its
mould on at least 8 of 12 words. The prediction was taken from experiment 12 (*Customary Lines*), where four makers
shown the family's six works all left the form unasked. Tonight the opposite happened on 12 of 12: arm F was tighter
than arm S on every word (`results.json`).

**Whose error.** The practice's, in predicting. Experiment 12's departure was a finding about one brief (*make a
work*), one material and one arrangement. The prediction read it as a property of the family. The briefs differ in
what they ask for: a work there, a drawing *"the kind a person makes in under twenty seconds"* here. Tonight's brief
also called the shown drawings *"made by others"*, which in arm F was literally true, since they were other
instances, but it may have framed them as references. Which of these turned the result is not separated. Experiment
12's finding stands for experiment 12.

## F-327 — a tracing measure that could not see the borrowing the face shows

**What happened.** P4 counted an H drawing as *traced* if it lay nearer to one of the six shown drawings than to
almost any six other people. 8 of 70 cells qualified. On *mermaid*, the face shows the H makers taking up the shown
people's poses, lying and curled, which no S or F maker drew. None of those cells counted as traced: the pool holds
many mermaids in the same poses, so being near a shown one is not distinctive.

**Whose error.** The practice's, in fixing a measure. It measured copying of a *drawing* where the makers borrowed a
*kind* of drawing. P4's failure stands as scored. It says the makers did not copy single drawings. It does not say
they took nothing from what they saw. The HOW lines say what they took: *"the common simple form"*.

## F-328 — two replies that broke the format, recorded and not repaired

**What happened.** H6's drawings of *moustache* and *mermaid* each carry a stroke written as a list of three lists
or with the y-list missing, so `parse.py` rejects them (`Extra data`). Those two cells of arm H hold five drawings,
not six. D was computed over five, and P4 over 70 cells, not 72.

**Whose error.** The maker's, in writing coordinates, and the practice's for writing a brief whose format a maker
could break without noticing. The replies stay verbatim in `rooms/H6.txt`. Repairing them would mean guessing which
coordinates the maker meant.
