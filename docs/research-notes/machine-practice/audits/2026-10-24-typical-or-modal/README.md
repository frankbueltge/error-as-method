# Typical or modal? The field's typicality measure on experiment 37's answers (Session 155, the seventh night)

Session 154 read Andueza Rodriguez, Candito and Huyghe, *Modeling the human lexicon under temperature variations*
(arXiv:2603.18171). The paper measures how human-typical a model's first word associations are by a standardised
strength, SS1, averaged over the model's answers to a cue (tok-SS1, §4.1, eq. 1–2). It finds the largest model
it tested more typical than people (2.56 against 1.67 at temperature 1, Table 1) and reads it as one prototypical
participant giving the commonest answers.

Session 153 (`works/2026-10-23-the-blank/`) found the family's most frequent word to be the people's commonest on
only 8 of 24 USF cues. `typicality.py` applies the paper's measure, unchanged in form, to the same cues and the same
144 answers, from the counts Session 153 committed (`plan.json`, `results.json`). Two adaptations are forced by USF
and declared in the script: one-person responses are restored as `G - sum(listed)`, and the SD is the population
SD (the sample SD is computed too, and no verdict changes).

| | family tok-SS1 | people's tok-SS1 |
|---|---|---|
| all 24 cues | 2.21 | 1.89 |
| 8 cues where the family's word is the people's commonest | 4.74 | |
| 16 cues where it is not | 0.94 | |
| family above people | 12 of 24; 4 of the 16 | |

**Reading.** By the paper's measure the family is more typical than the people, as the paper's largest model is. The
surplus is carried entirely by the eight cues on the people's peak. On the other sixteen the family is less typical
than a person on twelve. An averaged typicality cannot tell *the crowd's mode* from *a peak of its own that
sometimes coincides with it*. That holds for this family on these cues. Nothing here shows it for the paper's
models. Post hoc, nothing predicted. The claim is fixed as `S155.CARRIED` in `works/FALSIFIERS.md`.

Files: `typicality.py` (the computation), `results.json` (per-cue rows, both SDs), `typicality.txt` (its printout).
The paper's PDF is not committed. Its hash is in `works/position-2026-10-24.md`.
