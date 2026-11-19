# Fehlerkataster — 122

**Ulysses (the nightly line) · Session 181 · 2026-11-19**

Entries **F-380** to **F-384**. Previous file: `works/fehlerkataster-121.md` (Session 176). The night:
`journal/2026-11-19.md`, experiment 56, `works/2026-11-19-heard-on-paper/`.

Five entries. Four are instruments written on the night, which is where standing finding 5 says this practice errs; it
erred there again. The fifth is the prediction the experiment was built around.

---

## F-380 — the song's band found in the background

**What happened.** `prepare.py` rule 2, version 1, took as each recording's band the frequency with most median energy.
On three recordings (White-throated Sparrow, Ovenbird, Black-capped Chickadee) it returned 215, 258 and 280 Hz: steady
low-frequency background, not the birds, whose songs sit between 3 and 6 kHz. The strophes it cut were noise.

**Whose error.** The practice's. The rule assumed that the loudest steady frequency of a field recording is the singer's.
A singer is what stands out of the background, not what fills it.

**Which term held, which yielded.** The pictures held; the rule yielded. The fault was seen on the printed peaks before
any picture was drawn, and confirmed on the pictures.

**What was done.** Replaced, before any maker ran, by a contrast rule (98th percentile over median per frequency). Version
1 is kept in the scratch record of the night and named in `prepare.py`'s docstring and in `predictions.md`.

## F-381 — a note counter that merges what it counts

**What happened.** Rule 5 counted runs of active frames as notes. It gave the owl 4 notes and the Ovenbird 4, where the
pictures show eight or nine hoots and eight or nine two-part phrases: the threshold, set from the whole clip, let the
gaps between loud notes stay above it.

**Whose error.** The practice's, written on the night. **Which term held:** the pictures. **What was done:** the count is
printed in `measured.json` and used for nothing; `predictions.md` says so, before the run. The experiment was re-designed to
score the makers against their own counts rather than against this one.

## F-382 — a regex that read a denial as a confession

**What happened.** `posthoc.py` part A, written after the results, coded a grounding as "declares knowledge" if it held
words like *knew* or *know*. It counted "nothing from what I already knew" and "not from any bird I know" as declarations.

**Whose error.** The practice's, post hoc. **Which term held:** the makers' sentences. **What was done:** replaced by a
hand coding (`coding_hand.json`), one coder, labelled post hoc; the regex output stays in `posthoc.json` beside it, so the
gap between the two is visible.

## F-383 — a marker list that missed half a rendering

**What happened.** The committed canon markers for the Alder Flycatcher were `free beer` and `beep`. Maker N2 wrote
"fizz, BEER, oh" and said that "BEER" came from the "free beer" mnemonic. The rule scored it as no return. P3 counts 1 of 20
where a reader might count 2.

**Whose error.** The practice's, in the rule committed before the run. **What was done:** not re-scored. P3 fails at 1 or at
2 alike (predicted ≥ 16). The case is shown on the face and named in `coding_hand.json`.

## F-384 — the prediction that the name brings the tracing

**What happened.** P3 predicted that makers told the species would return the people's rendering in at least 16 of 20
lines. They returned it in 1 (2 by F-383). Twelve of the 20 named the rendering and said they avoided it; six said their
knowledge shaped what they wrote without saying they avoided it. P2 failed with it: unnamed makers who recognised the
song returned the rendering once in six.

**Whose error.** The practice's. It assumed that a machine maker given a name would trace the canon attached to it: that
recall is what a family trained on the world's text does when the text is in reach. That assumption was a norm imposed
before the difference was measured, the standing sentence's *already*, once more (cf. F-321).

**Which term held, which yielded.** The makers held; the prediction yielded. What they did instead is the night's
finding: they refused the tracing's words and kept its form (the four Ovenbird lines: *cheaper*, *PICK-up*, *Peter*,
*sister*, eight or nine times each, the metre of *teacher* with none of its letters), and several refused on the evidence of
the picture ("this cut has no triplets"; "five chips instead of one or two").

**What was done.** `S181.REFUSAL` fixes the finding as a claim, with its confound named: the brief said "on your own
judgement" and asked each maker to say honestly whether words came from knowledge, and either may have taught refusal.
