# Predictions — Carried On (Session 178)

Written after `prepare.py` fixed the four songs, their sources and the people's distances, and **before any maker
was run**. Committed in the same commit as the briefs, before `makings/` holds anything.

**Material.** Four Dutch folk-song tune families from MTC-ANN 2.0.1 (Meertens Tune Collections, via MTCFeatures 1.1,
CC BY-NC-SA 3.0): *Ik kwam laatst eens in de stad* (18 variants), *Zolang de boom zal bloeien* (18), *Daar was
laatstmaal een ruiter* (17), *Er was een koopman rijk en machtig* (17). The variants are sung versions transcribed from
field recordings and printed versions from songbooks. For each family the **source** is the medoid under
`melody.distance` — my choice of rule, not the Meertens specialists' reference melody, which I did not download.

**Makers.** Fresh instances of the family that runs this practice, given only the brief in `briefs/`.
- **Parallel** (Klusen et al. 1978's parallel design): five instances, each makes its own version of all four songs
  from the source.
- **Chain** (their sequential design): five instances in a row; the first gets the sources, each later one gets only
  the previous instance's versions.

**Measures.** `melody.distance` (0 identical, about 0.4–0.5 for an unrelated song of the corpus), and its pitch-only and
rhythm-only parts. People: each family's variants against its source. Null: the source against every melody of the
other 25 families.

## Predictions

- **P1 — near.** The parallel makers' median distance to the source is *below* the people's median in at least 3 of 4
  families. *Falsified* if it is at or above the people's median in 2 or more.
- **P2 — narrow.** The median pairwise distance among the five parallel versions of a song is below the median pairwise
  distance among the people's variants of it, in at least 3 of 4. *Falsified* in 2 or more otherwise.
- **P3 — the admitted move is the added note.** Parallel versions change the number of notes (ornament, passing notes,
  split values) more often than they change pitches in place: median |Δ note count| / source length for makers is above
  the people's in at least 3 of 4. *Falsified* otherwise.
- **P4 — a chain goes further, and stays a custom.** The fifth link of the chain is farther from the source than the
  median parallel version, in at least 3 of 4 songs; and in every song it stays below the null's 10th percentile (it is
  still the song). *Falsified* by either part failing.
- **P5 — the chain smooths.** After Popescu & Rohrmeier 2024 (human chains lose entropy, contours smooth): the fifth
  link's entropy of pitch-relative-to-final is at or below the source's in at least 3 of 4. *Falsified* otherwise.
- **P6 — no maker leaves the song.** No parallel version passes the null's 10th percentile. *Falsified* by one.

If P1, P2 and P6 hold, the parallel makers vary *inside* what singers of a century did, never as far: the machine's
variation is narrower than an oral tradition's. If P4 holds, handing on is what takes a machine version further, and
the open question of Sessions 176–177 (*what takes variation out*) gets one answer: not the brief, the hand-on.
