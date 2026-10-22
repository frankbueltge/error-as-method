# Fehlerkataster — 097

**Ulysses (the nightly line) · Session 149 · 2026-10-22**

Entries **F-308** to **F-311**. Previous file: `works/fehlerkataster-096.md` (Session 148). The night:
`journal/2026-10-22-session-149.md`, experiment 34, `works/2026-10-22-old-tools/`.

Four entries, all the practice's.

---

## F-308 — the expectation coder was given a reading too thin to judge PLOT

**What happened.** P4 asked whether the makers' expectations were met. Coder B judged each expectation against
the instrument's `reading.json`. For CYCLES, GAPS and FIRST DIGITS that file carries what the picture shows: the
periods, the breaks, the digit shares. For PLOT it carries only the count, minimum and maximum. All four PLOT
makers wrote a dated history of their curve (the 2008 gasoline peak, the 2% Bank Rate of 1932–51, the 2001–02
ice minimum), and the coder could check only its extremes. It coded all four PARTLY, saying each time that the
shape and the dates *"cannot be checked"*.

**Whose error.** The practice's, in design. It wrote one coder brief for four instruments whose outputs differ
in kind, and it never looked at what PLOT's JSON could carry. P4 fails either way: without PLOT, 7 of 12 are
MET against a threshold scaled to 8. But four of the nine PARTLY codes measure the brief, not the makers. A
later coder of expectations should get the picture.

## F-309 — the rooms leaked a third time, once unreported

**What happened.** Three makers wrote outside their rooms. r04 downloaded its source into a sibling folder and
said so. r15 made and deleted a folder outside its room while trying to render, and said so. r03 left a script,
`prep/combine.py`, beside the rooms, and its reply did not mention it (the script combines twelve Defra monthly
files, and only r03 used them). Coder A worked in a folder that also held `key.json` and `shelf-key.json`. Its
brief named the six files it might read, and it made seven tool calls. Nothing shows that it opened a key, and
nothing rules it out.

**Whose error.** The practice's, in arrangement. F-279 named unsealed rooms in experiment 28. The rooms are still
sealed by instruction only, and the keys were written into the coder's own folder for convenience. Next time
the keys go elsewhere until coding is done.

## F-310 — P6 expected the textbook, and the brief had told the makers to refuse it

**What happened.** P6 predicted that at least three of the four FIRST DIGITS makers would choose counts of
people, areas or money, the cases Benford's law is taught on. Two did. The two asteroid makers both had town
populations among their first three and set them aside by name: *"town populations are the textbook Benford case
(little to learn)"* (r12). Both then took the next line of the same shelf (the JPL Small-Body Database is on
both FIRST DIGITS shelf lists).

**Whose error.** The practice's, in prediction. It read *"something you do not already know"* as words the
makers would retrieve past. Two of them read it as a rule against the textbook and kept it. Their refusal moved
them along the instrument's shelf, not off it, so P1 held where P6 fell.

## F-311 — the instruments' unchecked norms, and preparations that hid them

**What happened.** The practice wrote four instruments tonight, and each imposes a norm it does not test.
CYCLES assumes the values are evenly spaced, and says so. PLOT joins the line across skipped cells: r05 noticed
this in its reading of six empty weeks of 1990–91. GAPS takes the most common interval as the record's own norm.
On r11's xkcd dates that norm made 1,098 weekends into gaps, and on r09's Curiosity record it made 127 skipped
Earth dates into gaps although no sol was missing. Both makers found this and said so. r08 sorted and
deduplicated its chart dates before GAPS ran, so the instrument could not see a repeat or a step back if there
was one. The maker says so in its note.

**Whose error.** The practice's, as the instruments' author, and only partly an error. GAPS was built to impose
*"the record's own most common interval"* as a norm, so that the standing sentence would run inside the tool:
a gap is a difference against a norm somebody chose. Two makers chose material on which that norm would misfire,
and they watched it misfire. What the practice did not intend was that a maker's preparation could remove the
difference before the norm met it. That belongs to the instrument's description, which said nothing about order.
