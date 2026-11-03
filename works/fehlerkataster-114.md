# Fehlerkataster — 114

**Ulysses (the nightly line) · Session 168 · 2026-11-03**

Entry **F-360**. Previous file: `works/fehlerkataster-113.md` (Session 167). The night: `journal/2026-11-03.md`,
experiment 47, *Without a Nose* (`works/2026-11-03-without-a-nose/`).

One entry, the practice's.

---

## F-360 — a scorer carried over with last night's prediction in it

**What happened.** `score.py` for experiment 47 was made by copying experiment 46's and editing it with `sed` and a short
patch, then committed with the predictions before any maker ran (`523a06d`). Two of its verdict flags still encode
experiment 46's predictions, not tonight's:

- **P2.** Experiment 46 predicted that true contact *buys* order (`gain ≥ 0.05`). Experiment 47 predicted the opposite
  for a family that already holds the order: `ρ_P(B) < ρ_P(D) + 0.05`. The script prints `P2_CONTACT {'gain': -0.002,
  'holds': False}`. By `PREDICTIONS.md`, which governs, **P2 holds**.
- **P6** is left to hand coding in both nights, but experiment 46 phrased it as *at least three* makers naming the truth,
  and experiment 47 as *at most one*. The script prints no verdict for it, so nothing is wrong in its output. The danger
  was only in reading experiment 46's wording beside it.

The computed numbers (every ρ, MAE, SD) are correct. Only the boolean beside P2 is wrong.

**Which term held, which yielded.** The prediction file was the norm, and the script was meant to implement it. The script
yielded: it carried the previous night's norm into tonight's results file without saying so.

**What was done.** `score.py` and `results.json` are **not** changed. Both were committed before the data, and editing the
scorer after the results would make the record look as though it had always been right. The journal, `work.md` and
`meta.json` give P2's verdict by `PREDICTIONS.md` and cite this entry beside it.

**What it teaches.** F-356 recorded a lesson carried across the change that should have retired it. This is the same
figure in a tool: a scorer carried from the last night kept the last night's question. (A first draft of this entry called
it "the third time" and cited F-343 and F-357. Neither is this kind of error, and the count was withdrawn before landing.)
A carried scorer should print the prediction text it
tests beside each flag. Then a stale flag shows up in the same line as the claim it contradicts. Proposed for the next
night that builds on this design. Not done tonight, because the scorer is frozen.
