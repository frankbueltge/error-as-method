# Predictions — The Blank (Session 153)

*Fixed and pushed before any maker ran. Keys, briefs and deal: `plan.json`, `briefs/` (seed 153).*

**Arms.** 18 fresh makers, tool-less, six per arm, each with the 24 keys of its arm in its own order.
**S**: a USF cue, the norms' own key (*"the first word that came to mind that was meaningfully related
or strongly associated to the presented word"*, Nelson, McEvoy & Schreiber, Intro). **P**: two cues at
once, 12 FORCED (the norms give both cues a shared associate at FSG ≥ .05 for each) and 12 UNFORCED (no
shared associate in the norms and neither cue in the other's list). **N**: the S cue with the people's
most frequent word excluded.

**Scoring rule** (`usf.norm`): upper case, letters only, a final S dropped when three or more letters
remain and the word does not end in SS. Applied identically to makers' words and to the norms' targets.
A cell is the three makers numbered 1–3 in an arm on one key; it is **unanimous** if their three
normalised words are identical. All six makers count for the modal word and for the distinct count.

**The human reference.** For each S cue, the probability that three people drawn from its USF group
wrote the same word, from the printed counts (`usf.p_three_agree`; idiosyncratic responses count as
distinct). Summed over the 24 S cues it is **E = 1.68** cells. For six draws, the expected number of
distinct words is simulated from the same counts (seed 1530, 20,000 draws per cue) in `score.py`.

## `S152.ONEMAP`, as the row states it

This is its event: at least three fresh makers each answer the same 24 keys made tonight (arms P and
N, 48 keys) on a material whose answer is a word.

- **R1 (clause 1).** Falsified if fewer than half of the 48 P and N cells are unanimous. Prediction:
  it holds, at **≥ 30 of 48**.
- **R2 (clause 2).** Translated for this material: the cells where the material forces least are the
  12 UNFORCED pairs. Falsified if fewer than a third (4) of them are unanimous. Prediction: it holds,
  at **≥ 5 of 12**.

## Beside the row

- **H1 (people).** On the 24 S cells, unanimous cells ≥ 2E = **3.4**, i.e. at least 4. Prediction:
  **≥ 12 of 24**, seven times what people give.
- **H2 (which word).** The six makers' modal word on an S cue equals the people's most frequent word
  on **≥ 16 of 24** cues.
- **H3 (spread).** Mean distinct words among six makers on an S cue is at most half the mean
  expected among six people.
- **H4 (n − 1).** With the people's top word excluded, the family converges again: **≥ 12 of 24** N
  cells unanimous, and the six makers' modal word is the people's **second** word on **≥ 8 of 24**.
- **H5 (forcing).** FORCED pairs give more unanimous cells than UNFORCED pairs.

**What would surprise me most:** N less unanimous than S by more than half (the subtraction scattering
the family), or H2 failing below 12 (the family's one word not being the people's first).
