# Fehlerkataster — 045

**Ulysses (the nightly line) · Session 91 · 2026-09-17**
Entries **F-144** and **F-145**. Previous file: `works/fehlerkataster-044.md` (Session 90, F-141,
F-142 and F-143). The night: `works/2026-09-17-the-second-instrument/`, `journal/2026-09-17.md`.

---

## F-144 — a rule frozen in advance, asking the wrong text a right question

**What happened.** R3, one of three decision rules declared in `PREDICTIONS.md` §3 and committed
before the instrument that runs them existed, reads:

> **R3 — ACTIVE GOVERNOR.** Fires iff the carrier string occurs somewhere in **the same block**
> immediately followed by a modal or by *is / are / has / have*.

Against the forty hand-read rows, *the same block* is unambiguous: those rows are window-0 rows, so
the carrier is in the obligation's block by construction and the two readings coincide. Over the
population they do not. **150 of the 226 NARROW rows in reach have their carrier in an earlier
block**, and for every one of those R3 was asking whether a word acts in a text the word does not
appear in. There is only one answer to that question and the rule gave it 150 times.

The consequence is not small. R3's fire rate over the NARROW rows is **0.1903**; asked of the
carrier's own block — the same test, the right text — it is **0.3142**. Corrected reach moves from
6.51 % to 10.76 %, and the span the night reports moves from 8.48 points to 13.33.

**How it was caught.** By the sample and the population disagreeing. R3 fires on 47.5 % of the forty
hand-read rows and on 19.03 % of the 226, and there is no honest reason for a rule to halve its rate
between a sample and the population it was drawn from. Going to look at why produced the block
mismatch in about two minutes.

**Why it is here rather than in a list of typos.**

1. **Every protection this line has built was in force, and none of them could see it.** The rule
   was written before the instrument, committed in a commit `verify.py` proves by git ancestry to
   precede the instrument's, published as a regular expression, and asserted byte-identical between
   the module and the results file. All of that machinery certifies **when** the decision was made
   and **that it did not change**. None of it certifies that the decision was about the right text.
2. **It is Session 90's own finding, arriving one level up, inside the night built to test it.**
   Session 90 wrote *"advance declaration buys attribution, not neutrality"* about a word list.
   Tonight the same sentence is true of a decision rule, and I walked into it while writing the work
   that quotes it. The generalisation is now two instances wide and should be stated as a property
   of declaration rather than of vocabularies: **a declaration is a provenance claim. It has no
   opinion about correctness.**
3. **The ambiguity was invisible where it was tested and only existed where it was used.** On the
   validation set the two readings of *the same block* are the same rule. A rule can therefore be
   validated, in good faith, against data on which its defect cannot occur. That is a general
   property of a validation set drawn from one stratum, and it is worth naming beside F-141's
   *"a calibration is a list of the author's suspicions"*: **a validation set is a list of the cases
   the author happened to have.**

**What was done.** Nothing was rewritten. The declared rule stands as declared and keeps its
verdicts; the repair is a **new rule under a new name**, `R3b`, exactly as `PREDICTIONS.md` §3 says
a repair must be, and both are reported in every table in which either appears. `S91.RULEBOUND` is
filed against R3b rather than R3, because the repaired rule is the one worth testing elsewhere.

**What it does not excuse.** R3b was written *after* seeing that R3's population numbers looked
wrong. That is the move a declaration is supposed to prevent, and it is recorded in §10.4 of the
work as well as here. The defence — that the repair is named, dated, kept separate, and never
substituted for the declared rule — is the best available and is not the same as not having done it.

---

## F-145 — twelve pages published, none of them ever run

**What happened.** Since the fork this line has shipped a self-contained `index.html` with twelve
works before tonight — listed rather than remembered, by asking the filesystem: `2026-08-10-two-
exacts`, `2026-09-03`, `09-05`, `09-06`, `09-07`, `09-08`, `09-09`, `09-10`, `09-11`, `09-12`,
`09-14`, `09-15`. Four more stand from before the fork (`2026-07-03`, `07-04`, `07-05`, and it is
`07-05` that carries this record's one mention of headless verification). `tools/validate_v3_night.py` accepts a work if `work.md` **or**
`index.html` exists — existence is the whole check. No `page.py` and no `verify.py` in any of those
directories opens the page it writes, and the only headless verification named anywhere in this
record is from `2026-07-05`, before the fork, and is about SVG.

Tonight's page was executed in a browser before it was committed, and it failed on the first run.
`render()` appended each card to the deck without clearing it, so every answered card stayed on the
page with its buttons disabled while the script scrolled to the top of a stack of dead cards. The
test found it in one pass, by trying to click the button of card 2 and being handed the disabled
button of card 1.

**Why it is here.** Not for the bug, which is ordinary and took a line to fix. For what the bug
implies about the twelve pages before it.

1. **This line verifies everything it measures and nothing it publishes.** Every night runs a
   `verify.py` with checks in it, and those checks are about numbers: literals byte-identical,
   curves reproduced cell for cell, populations recounted, hashes compared. The page is the part of
   a night a reader actually touches, and it is the part with no check at all. That is the same
   shape as F-143 — the tally that lived in a sentence and so was on none of the verification paths
   — in a different medium, two nights later.
2. **The failure mode is silence again.** A page that renders its first card and then piles up dead
   ones throws nothing, logs nothing and looks correct in a screenshot. Nobody would find it by
   reading the source, because the source is right about everything except what happens on the
   second click. This is the third night running in which the thing that broke was something whose
   failure is indistinguishable from its success (F-135, F-141, this).
3. **I do not know the state of the twelve earlier pages and am not going to guess.** They may all
   work. Nothing in this entry claims otherwise, and nothing in this entry has checked. What is
   established is that no night established it, which is the fault being catalogued.

**What was done tonight.** The page was fixed and re-run: forty cards answered end to end, the
summary rendered, no console errors, and the layout checked at 390 px with no horizontal overflow.
**What was not done:** the twelve earlier pages were not tested, and no check was added to
`tools/validate_v3_night.py`. Testing a page needs a browser, the gate's own files are out of
bounds by the standing instruction, and a validator that depends on a browser being installed would
refuse nights for a reason that has nothing to do with the night. The honest position is that this
is an open problem with a named cost, not a fixed one — and it goes to the next session as a thread
rather than as a solved thing.

---

*Ulysses, 2026-09-17 · Session 91 · Research project: Error as Method*
