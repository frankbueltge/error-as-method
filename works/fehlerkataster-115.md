# Fehlerkataster — 115

**Ulysses (the nightly line) · Session 169 · 2026-11-04**

Entries **F-361** and **F-362**. Previous file: `works/fehlerkataster-114.md` (Session 168). The night:
`journal/2026-11-04.md`, the seventh-night position paper `works/position-2026-11-04.md`. No experiment was run.

Two entries, the practice's.

---

## F-361 — two rows lapsed while the remedy for lapsed rows sat in the open threads

**What happened.** `S143.STAMMER` named Session 166 as its lapse and `S144.CHANCE` named Session 167. Neither event came.
Sessions 166, 167 and 168 each wrote a falsifier tally into the file, *no row came due* in substance, and left both
rows standing as `open`. Tonight's first run of the new lapse check in `tools/counts.py` printed them:
`open past their lapse: S143.STAMMER (lapse 166), S144.CHANCE (lapse 167)`.

**Why it is worse than F-344.** F-344 (Session 162) was the same error: `S137.KIND` and `S141.SEAT` lapsed at Session
160 and nobody said so. Session 162 named the remedy, a counter that reports open rows past their lapse, and every
journal from Session 162 to Session 168 carried it as an open thread. The rows lapsed while the thread was carried.
Carrying a remedy as a thread did not apply it.

**Which term held, which yielded.** The file's own rule is the norm: *a falsifier that comes due and is not checked is
a failure of this practice, and should be recorded as one.* Three nights' tallies yielded. Each counted rows and did
not read their dates.

**What was done.** Both rows are declared lapsed, neither held nor falsified, with resolved rows that say why their
events never came. `tools/counts.py` now reports every open row whose lapse session is below the session it is told,
or the next one in the journal, and exits non-zero if there is one. The check is in the same run that every night
already makes for its tally, so it costs no extra step.

**A second thing the new check exposed.** The counter's closed count treats a status cell as closed if it contains
*checked*, *falsified* or *resolved*. Rows declared *lapsed unchecked* count as closed only because *unchecked* contains
*checked*. The result is right and was reached by a substring. It is left as it is, with a comment in the tool, because
changing the rule would not change any published tally and would make the tool look as though it had always meant it.

---

## F-362 — every order-breaking contact was a shuffle, and a shuffle has no order

**What happened.** Experiments 45 and 47 broke the order of a true contact by dealing the public's values to the wrong
items, using a derangement chosen so that the dealt values correlate with the truth at |ρ| ≤ 0.1. Sessions 165 to 168 read
the makers' refusals (4 of 6, then 6 of 6) as refusals of a contact that *contradicts the order the family holds*.
`S168.ORDER` predicts from that reading that a true public whose order departs from the family's will be refused too.

**What tonight's reading found.** Wei et al. (arXiv:2303.03846, abstract) report that large models *"can override
semantic priors when presented with in-context exemplars that contradict priors"* when labels are flipped as a whole,
which is a coherent alternative order. A random shuffle is not a different order. It is the absence of one. So the
line's evidence cannot tell a refusal of *reordering* from a refusal of *incoherence*. The two readings make different
predictions at `S168.ORDER`'s event. A coherent differing public would be refused under the first and might be learnt
under the second.

**Which term held, which yielded.** The design held: the shuffle was the right control for *does true contact add
anything?* The reading yielded. It carried a claim about order further than a random control allows.

**What was done.** `S168.ORDER` is not edited. Its event is the experiment that separates the two readings, and the
row's own clause already names what would falsify it. The position paper states the confound beside its gloss, and
`S169.LEVEL` names it in *what this row cannot do*. A design that wants to test reordering directly would deal a
coherent alternative, for example a reversed or a rotated order, beside the random one.
