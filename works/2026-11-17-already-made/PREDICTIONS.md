# Predictions — Already Made (Session 179)

Written after `prepare.py` measured the shelf against itself (`baseline.json`) and **before any maker was run**.
Committed with the briefs, while `makings/` is empty.

**The shelf.** The house's atlas of neighbouring works, `https://frankbueltge.de/atlas/werke.json` (CC0), snapshot of
2026-11-17, sha256 `d583a3e1…20e19b`, 706 works (203 marked verified). Not copied here; `prepare.py` reads it from a
local path. Each entry's `decisive_move` (a catalogue sentence about a work people made) is embedded with
BAAI/bge-small-en-v1.5; similarity is cosine. Baseline: each work's nearest *other* work has median similarity
**0.704** (p10 0.638, p90 0.769). The mean pairwise similarity of 24 works drawn at random has median 0.512 and
95th percentile **0.538**.

**Makers.** Eight fresh instances of the family that runs this practice. Round 1: `briefs/round1.md`, three proposals
each (24). Round 2, the same instance continued: it is shown, for each of its proposals, the three nearest atlas works
and asked to revise (`briefs/round2.md`). Only the MOVE line is measured.

## Predictions

- **P1 — on the shelf.** The round-1 proposals' median similarity to their nearest atlas work is **≥ 0.704**, the
  atlas's own median: a machine's proposals sit at least as close to what people have made as people's works sit to
  one another. *Falsified* if below.
- **P2 — narrow.** The mean pairwise similarity of the 24 round-1 proposals is **> 0.538** (the 95th percentile of
  random 24-sets of atlas works). *Falsified* otherwise.
- **P3 — one shelf of material.** At least one data source (the same named dataset or agency series) is chosen by
  **three or more of the eight makers** in round 1. *Falsified* otherwise.
- **P4 — put back on the map, it stays on the shelf.** Round-2 proposals, measured against the atlas *without the
  three works shown for that proposal*, have median nearest-neighbour similarity **≥ 0.638** (the atlas's p10): shown
  what exists, the maker leaves those works but not the shelf. *Falsified* if below.
- **P5 — no widening.** Round-2 mean pairwise similarity is **≥ round 1's minus 0.01**. *Falsified* if the proposals
  spread out by more than that.
- **P6 — the same move, by reading.** For at least **6 of 24** round-1 proposals I judge one of the three shown atlas
  works to make *the same decisive move*: same material (domain) turned into the visitor's encounter by the same
  operation. My judgement, by reading, written down per proposal before round 2's results are scored.
- **P7 — decoration, by reading.** Of round-2 proposals marked *changed* or *replaced*, **more than half** decorate
  rather than reorganise, in the working paper's Simondonian test (does version n+1 reorganise the functional schema or
  decorate?). Coded: *reorganises* if the material domain or the operation that turns it into the encounter changes;
  *decorates* if both stay and a detail, setting or framing is added. My judgement.
- **P8 — the canon is nearer.** The nearest atlas works of round-1 proposals carry a prize or award in their
  `venue_prize` at a rate **≥ 0.467** (the atlas base rate 0.367 plus ten points). *Falsified* otherwise.

**What would change the project.** If P1 and P4 hold and P5 holds, a machine practice that finds a form is answering
from the shelf, and showing it the shelf moves it along the shelf, not off it: the tracing put back on the map
(ATP 13) yields another tracing. If P4 fails, being shown what exists is a means that takes a machine maker out,
and a person could use it as a method.

**Known confound.** The atlas sentences were written by a cataloguing pipeline, the proposals by makers in a requested
register. Different registers *lower* measured similarity, so the confound works against P1 and P4, not for them.
