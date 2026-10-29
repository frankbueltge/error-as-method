# The reach — audit, Session 162 (2026-10-29)

**Post hoc, on committed data. Nothing here was predicted.** Written for the seventh-night paper
`works/position-2026-10-29.md`, to read `S161.TETHER`'s wording back against experiments 40 and 41, which the row
cites and which were committed before it existed. It is not the row's event (the row asks for the *next*
experiment).

`python3 reach.py` reads the `results.json` of experiments 40 and 41 and the `plan.json`, `results.json` and `rooms/`
of experiment 42, unchanged. It writes `results.json` here, and its printout is `reach.txt`.

Three counts, all on each describer's stated median of the people:

1. **Distance** by the row's measure: on the far keys (people's median ≥ 1.5 steps from the family's), the share of
   placements more than 1.05 steps from the family's median. 12 of 180, 10 of them on two foods the family rated 5.
2. **Direction**: on keys where the people's median and the scale's middle lie on opposite sides of the family's
   whole-step median, the departures by side. 143 of 143 toward the people. Experiment 42 has no such key.
3. **Sign**: on every key where the people stand at least one step from the family's whole-step median, how many
   placements stayed, moved to the people's side, or moved the wrong way. 319, 423, 8, out of 750.

Declared adaptation: family medians on a half step are skipped in counts 2 and 3, because they have no side. The
first run kept them (F-343).

Experiment 39 is left out because its answers are numbers on 0–100 and quantities, not steps.
