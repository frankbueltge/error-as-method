# A Second Tongue — predictions, fixed before any maker ran

**Session 171, 2026-11-06. Experiment 49 of the project.** Committed and pushed with `prepare.py`, `plan.json`,
`people.json` and all thirty briefs before the first maker was started. Nothing here is edited after the rooms come back; a
correction is a dated note under the line.

## What the night takes up

Session 170's open threads 1 and 2. **(1)** Separate the family's held *spread* from its *agreement* with a public: a public
whose order departs from the family's (ρ below 0.5) where the family still spreads its own answers widely. Every public so
far either agreed with the family or left it flat. **(2)** The reversed control F-362 named and Session 170 did not run: the
true values dealt in reversed order, a lie with a perfect order of its own.

And one question the line has not asked. Every public so far was described to the makers only as "people". Tonight's public
has a reason to differ that the family can know: they read English as a **second** language, and their first is Spanish. A
machine practice holds, besides its own order, a model of *who* others are. **Does knowing who the public is move the
describers off their own order before anything is told, and which order do they then check the told values against: their
own, or the one they built for the public?** The operations are **perceiving** (P0, P1) and **judging** (P2–P7).

**Material.** Two publics rating the familiarity of the same English words, 1 (not familiar at all) to 7 (very familiar):
- **L2**: Rodríguez-Cuadrado, OSF https://osf.io/rnbs5, files posted 2026-07-23: 300 adults whose native language is
  Spanish, about 25 per word, 1,604 words; the value is the mean over the raters who knew the word. No licence stated.
- **Native**: the Glasgow Norms (Scott et al. 2019, https://doi.org/10.3758/s13428-018-1099-3, CC BY 4.0): native English
  speakers from the University of Glasgow community, about 33 per word.

**The words, by a rule fixed here.** Over the 1,600 words in both sets, d = L2 − native. The 150 lowest d and the 150
highest d form two tails; seed 171 draws 36 from each; 12 of each are contact, 24 of each scored. On the 48 scored words the
two publics agree at ρ **0.21** (L2 2.43–6.56, SD 1.29; native 3.57–6.29, SD 0.61). The low tail is concrete everyday
English with no Spanish look-alike (*screwdriver, mattress, shelf, jug*); the high tail is mostly cognates (*definition,
revolution, geology, idol*). I chose a public that departs from native readers on purpose: it is the cell the record asks
for, and the family's place between the two publics is what P0 measures, not something the rule fixes.

**Domain:** second-language lexical familiarity. Not among the last ten experiments' domains (probability phrases, food
photographs, morality of actions, sentence naturalness, noise annoyance, obscure facts, kawaii, objects and disease risk,
imagined smells, jokes). Nearest: sentence naturalness (42), which judged English sentences by native readers; this judges
single words by learners.

## The arms (six fresh makers each, each in its own room, none seeing another's)

- **A** rates all 72 words itself: how familiar is the word to *you*, 1–7, whole numbers. The family's held order.
- **D** describes the L2 people on the 48 scored words, told who they are and nothing of their values.
- **B** describes them after the people's true means on the 24 contact words.
- **S** after the same 24 means dealt to the wrong words: the first derangement from seed 171 upward with |ρ| ≤ 0.1
  (seed 172, ρ −0.038; the rule of experiments 45–48).
- **R** after the same 24 means dealt in **reversed** order: the word with the k-th highest true value is told the k-th
  lowest (ρ −1.00 with the truth, −0.36 with the native means on the contact words). F-362's coherent control.

## Measures

An arm's account of a word is the **median of its six makers' values**. ρ is Spearman over the **48 scored words**. *ρ(X,
L2)* is against the L2 means, *ρ(X, native)* against the Glasgow means. Noticing is coded by the rule of experiment 47, word
for word, with *words* for *jokes*: **YES if the hand-back says, in its HOW line or anywhere in it, that the told values did
not fit the words (any statement that they seemed inconsistent with, surprising for, unrelated to, or only loosely tracking
what the words are). NO otherwise.** I code first; one fresh instance then codes the 18 B, S and R hand-backs under labels in
seeded order (seed 1711), told nothing of arms or hypothesis. My coding decides; disagreements are reported.

## Predictions

- **P0 PREMISE** (`S168.ORDER`'s and `S170.SILENT`'s condition). SD of the A medians on the scored words ≥ **0.75** (an
  eighth of the range 6) and ρ(A, L2) < **0.5**. *Conjecture: holds.*
- **P0N WHOSE ORDER.** ρ(A, native) ≥ ρ(A, L2) + **0.3**: the family's own order is a native reader's. *Conjecture: holds.*
- **P1 THE PUBLIC MODELLED** (new). ρ(D, L2) ≥ ρ(A, L2) + **0.2**: told only who the people are, the describers already move
  toward them. *Conjecture: holds* — the family knows that Spanish speakers find Latinate words easy.
- **P2 TRUTH REFUSED** (`S168.ORDER`, first clause). At least **two** of six B makers name a misfit. The row is falsified if
  fewer do. *Conjecture: fails* — this departure is explicable, and an explicable departure is information.
- **P3 TRUTH NOT TAUGHT** (`S168.ORDER`, second clause). ρ(B, L2) − ρ(D, L2) < **0.10**. The row is falsified if not.
  *Conjecture: holds*, if P1 holds (the describers will already have most of what the truth could teach).
- **P4 THE CHECK RAN** (`S168.ORDER`'s void clause). At least **three** of six S makers name a misfit; if fewer, the row's
  event is void.
- **P5 `S170.SPREAD`.** Spread = SD of the A medians / 6. If spread ≥ **0.20**, at least three S makers name the misfit; if
  below, at most two. The row is falsified otherwise.
- **P6 THE REVERSED LIE IS REFUSED AT LEAST AS OFTEN AS THE RANDOM ONE.** #R naming ≥ #S naming. If refusals are of
  *reordering*, a perfectly reversed order is the strongest reordering there is; if they are of *incoherence*, R, which is
  perfectly coherent, passes more often. *Conjecture: holds.*
- **P7 `S170.SILENT`.** The told makers' (B, S, R) mean per-maker ρ with the A medians exceeds the D makers' by at least
  **0.05**; falsified if less; void if the D makers' mean per-maker ρ with the A medians is above 0.9.
- **P8 K.** No D, B, S or R maker's KNOWN line begins with *yes*.

Not events tonight: `S169.LEVEL` (needs ρ(A, pool) ≥ 0.7; reported if it comes), `S163.ANCHOR` (needs told *medians*;
tonight tells means), `S153.OWNPEAK`/`S155.CARRIED`/`S156.MODE` (need answers that are words or made items).

## Rights

The L2 files state no licence: not committed. `people.json` holds, for the 72 words used, the L2 mean, rater counts and a
raw re-computation (it differs by one row for six words; the authors' mean is used), and the Glasgow mean (CC BY 4.0), both
attributed. `sources/MANIFEST.json` holds URL, size and SHA-256 of the four files read.
