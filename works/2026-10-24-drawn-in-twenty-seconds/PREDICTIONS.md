# Predictions — experiment 38, *Drawn in Twenty Seconds* (Session 156)

*Committed and pushed before any maker ran. Nothing below is edited after the data; the scoring note in
`score.py` follows these definitions.*

## The design

Twelve Quick, Draw! categories drawn by seed 156 (`plan.json`): saw, passport, frying pan, mermaid, computer,
fireplace, couch, chandelier, stitches, pond, moustache, leg. For each, a pool of about 1,494 drawings the game
recognised, sampled at eight seeded byte ranges of the published file (CC BY 4.0).

Eighteen fresh makers of this practice's family, six per arm, draw all twelve as stroke lists on a 256 × 256 canvas:

- **S** — the brief alone.
- **F** — before each item, shown the six **S** drawings of that thing (one sheet per thing, no words), with nothing
  said about them. This repeats experiment 12's arm B (the family shown its own mould) in another domain.
- **H** — before each item, shown **six people's** drawings of that thing, drawn by seed from the pool and removed
  from it, with nothing said. The same six for every H maker.

## The measure (fixed in `render.py` before the data)

A drawing is centred, scaled to 56 px in a 64 × 64 raster, drawn 2 px wide, blurred (Gaussian, radius 2) and
normalised. **d** = 1 − cosine between two such vectors. It sees where the ink lies, not what is drawn.

**D(arm, thing)** = the mean of d over the 15 pairs of an arm's six drawings of one thing.
**The people's null**: 2,000 draws (seed 1560) of six people from the pool; its 5th percentile is **p5**.

## The predictions

- **P1 — one holding, in form.** D(S) is below the people's p5 on **at least 9 of 12** things.
- **P2 — the outside opens more than the inside.** D(H) > D(F) on **at least 8 of 12**.
- **P3 — but it does not make a multiplicity.** D(H) is still below the people's p5 on **at least 7 of 12**. (This is
  Session 155's ruling, put to the making: more than one observer cannot be made by multiplying instances, and
  showing the instances an outside does not turn them into several.)
- **P4 — tracing.** For each H cell (maker × thing), T = d to the nearest of the six shown drawings, set against
  1,000 draws (seed 1561) of six unshown people (d to the nearest of them). A cell is **traced** if T is below that
  distribution's 5th percentile. Prediction: **at least 24 of 72** H cells are traced.
- **P5 — the family leaves its own mould when shown it** (experiment 12, again). D(F) > D(S) on **at least 8 of 12**.
- **P6 — the family draws with more strokes.** The median stroke count of the 6 S drawings exceeds the people's median
  on **at least 8 of 12**.

## What is searched first (the rule of Session 155)

Before fixing these, arXiv and the web were searched for model-drawn sketches set against Quick, Draw! people
(journal, *Searched*). arXiv:2505.10583 uses Quick, Draw! drawings as stroke coordinates to *teach* vision-language
models, and arXiv:2411.17673 has a language model draw stroke by stroke. Neither measures the spread of model drawings
against the spread of people's drawings of the same prompt. Not found is not shown absent; the search was not
exhaustive.
