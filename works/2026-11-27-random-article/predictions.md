# Predictions — experiment 63, *Random Article* (Session 189)

Committed and pushed before any curator ran. Scored by `tools/score.py` against each curator's `final.md`; `v1.md` is
scored for P8 only.

## The design

- **Material.** 160 articles of English Wikipedia drawn by seed 189 from the 6,407,814 rows of the `wikimedia/wikipedia`
  snapshot `20231101.en` (`tools/frame.py`); coded into nine kinds before the run (`people/CODEBOOK.md`).
- **Draws.** Six draws of twelve from the 160, chosen from 20,000 seeded random twelves (seed 1890) at the 5th, 25th,
  45th, 65th, 85th and 99th percentile of their total variation distance (TVD) from the 160's mix of kinds
  (`people/draws.json`). Every draw is a real chance draw; the choice of percentile only spreads them from the
  smoothest to the lumpiest.
- **Arms.** Curator A*i* gets draw *i* only, told it is a chance draw from all of English Wikipedia (true: a random
  twelve of a random 160 is a random twelve of the whole). Curator B*i* gets draw *i* and the 160, told both are chance
  draws. Twelve fresh instances, one per folder, folders outside this repository, absolute paths. Each writes a wall
  text, twelve captions and tags (`typical` / `unusual`), an order, a rating 1–5 and replacements; every version kept.
  After "done", the question in `briefs/question.md`.
- **The confound, stated before the run** (`REQUESTS.md`, Session 179): every curator carries this repository's
  instruction file, headed with the line's name. The brief names a task and no theme.

## Why the night asks

Experiment 62 ended with advice for a person researching: if the clumps, gaps and the rare matter, let chance draw
and let the machine annotate. Tonight tests that advice. Choosing is taken away; only naming is left. The question is
whose norm the tags carry: the archive's frequencies, or a picture of the encyclopedia the curator brings.

## Predictions

Common kinds: P, S, D (each at least 13 % of the 160). Rare kinds: T, B, O, G (each under 9 %).

- **P1. The tag does not track the kind's frequency.** In A, the share of rare-kind items tagged `unusual` exceeds the
  share of common-kind items tagged `unusual` by less than 15 points. *Falsifier:* 15 points or more.
- **P2. The stub is the type.** Pooling A and B, the median word count of items tagged `unusual` is higher than that of
  items tagged `typical`. *Falsifier:* equal or lower.
- **P3. The rating does not see the lumps.** In A, the Spearman correlation between a draw's TVD and its curator's
  rating is above −0.5 (n = 6, weak, said so). *Falsifier:* −0.5 or below.
- **P4. Every curator without the pool would replace something.** All six A curators name at least one replacement.
  *Falsifier:* any A curator answers "none".
- **P5. The pool reduces replacement.** B curators name fewer replacements in total than A curators.
  *Falsifier:* B's total equal to or above A's.
- **P6. Navigation pages are read as not-the-encyclopedia.** Pooling A and B, at least half of the D items in the draws
  are tagged `unusual` or named for replacement. *Falsifier:* fewer than half.
- **P7. They know the numbers.** In the after-question, the median estimate of the person share is within 10 points
  of 21.2 % and the median estimate of the under-100-words share within 15 points of 28.8 % (the 160's values).
  *Falsifier:* either median outside.
- **P8. Revision makes the tags more typical.** Across the twelve, the number of `unusual` tags in the final versions
  is lower than in the first versions. *Falsifier:* equal or higher.

## What would count as the advice holding

If P1 and P3 fail (tags and ratings track the archive) and P4 fails (curators accept the draw), the advice of
experiment 62 holds: chance draws, the machine annotates faithfully. If P1, P3 and P4 hold, the machine re-imposes in
its words the evenness it can no longer impose by choosing, and the advice needs its warning.
