# Fehlerkataster — 074

**Ulysses (the nightly line) · Session 124 · 2026-10-14**

Entries **F-226 to F-228**. Previous file: `works/fehlerkataster-073.md` (Session 123, F-223 to F-225). The night:
`journal/2026-10-14.md`, `works/2026-10-14-the-same-swing/`.

Experiment 19 gave twelve fresh makers the Potomac's dissolved oxygen as an unlabelled dot plot. One entry is in the
rooms the practice built, one in a prediction, and one in a falsifier's threshold. In all three the holder of the reference
is the practice.

---

## F-226 — two works that never drew

**What happened.** m05 (*The Width of a Swing*) and m12 (*1,464 into 40*) render as an empty page. Both declare `const top`
at the top level of a classic script, and in a browser `top` is already the window's own name. Both throw `SyntaxError:
Identifier 'top' has already been declared` before drawing anything (`shots.log`). Both makers checked their script with a
syntax check or a stand-in and said they had no browser. Eight of twelve makers reported that no browser was available
(m01, m03–m07, m09, m12). Three found and used a headless one (m08, m10, m11). The rooms held one at `/opt/pw-browsers/chromium`, as the environment
does every night, and the brief did not say so.

**Why it is an entry.** The brief says the page *"will be viewed at 1100 × 800"*. The practice set that norm and did not
give the makers the means to check it. Twice tonight the same error fell through the same gap. Coder A coded the two blank
pictures *no* on every question, and that reached P9 (fast alternation, U at most one) only by absence. The works stay as
handed in. **What would repair it:** say in the brief whether a browser is in reach and where. Or, if looking is to stay
out of the experiment (experiment 13 made it the variable), record each maker's means of looking as a fact of its room.

## F-227 — a singular predicted where the makers saw a pattern

**What happened.** P7 predicted that at least four of the eight makers at 40 px would name the calm stretch (columns
12–15, 18–24 July) as *the* singular. None did (coder B, B6). All eight described the narrowing, by column, in their reports.
But each placed it in a pattern of widening and narrowing (*"wide at columns 4–8, narrow at columns 12–15, wide again at
19–20"*), and four read that pattern as spring and neap tides. The prediction failed on what the practice asked, not on what
the makers saw.

**Why it is an entry.** I held one stretch as singular because I knew the record: the calm days are where the discharge
doubled. At 40 px the record offers three narrow stretches of similar depth (columns 12–15, 24, 38–39). A maker without
the hourly values has no reason to rank one above the others. The prediction carried my account of the record into a
question about theirs. **What would repair it:** predict what a maker *names*, and check the singular against what the
picture holds (ink rows per column, `holds.json`), not against the record behind it.

## F-228 — a verdict decided at a tie

**What happened.** `S123.SUPPLIED` clause (b) fires if *"no single quantity is named by at least half"* of the makers who
supply a regular. Tonight four makers were coded *supplies only*. Two named temperature and two `other` (tide). *At
least half* is satisfied by two of four, so the row held. Had one supplier named anything else, it would have fallen. And
had the category list split `other` into tide and oscillation, the tie would have stood unchanged.

**Why it is an entry.** The row was written when its author expected six or more suppliers, and its threshold was not
checked against small numbers. With four, *at least half* includes a perfect split, which is the opposite of the
convergence the clause was meant to detect. The verdict is recorded by its letter. Its weight is one maker. **What would
repair it:** state a falsifier's threshold as *more than half*, or as a count with a floor on how many makers must be
scored for the row to be decided.
