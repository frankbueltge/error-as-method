# Predictions — experiment 61, Session 187, 2026-11-25

Written and committed before any maker ran.

**The material.** NOAA Fisheries' copy of the US Coast Guard's register of documented vessels (*Merchant Vessels of
the United States*), through the FOSS API, without personal data. Frame: 176,080 valid recreational vessels on
2026-11-25. 400 drawn by seed 187 (`tools/sample.py`, `people/people.json`): draws 0–199 are the SCORE sample,
200–399 the TOLD sample. Every name's FREQ, how many valid recreational vessels bear exactly that name, is read from
the same API (`tools/freq.py`, `people/freq.json`).

**The TOLD sample, hand-coded by this session under `codebook.md`** (`tools/code_told.py`, `people/coded-told.json`):

| feature | of 200 |
|---|---|
| PUN | 37 |
| PERSON | 28 |
| SINGLE | 82 |
| FREQ = 1 (the name is on this boat alone) | 88 |
| FOREIGN (not told) | 17 |
| SEQUEL (not told) | 8 |
| SEAWORD (not told) | 43 |
| FREQ ≥ 100 (not told) | 9 |

The SCORE sample's computed features, before hand coding: SINGLE 94, SEQUEL 11, SEAWORD 41; FREQ = 1 on 79,
2–9 on 60, 10–99 on 50, 100 or more on 11. Its PUN, PERSON and FOREIGN are coded later, blind, together with the
makers' names (`tools/blind.py`): the primary coder is a fresh instance given only the hand section of the codebook;
this session codes too and reports agreement. This session has read the SCORE names and is not blind to them.

**Design.** Eighteen fresh makers, folders outside the repository, carrying this practice's name (`S179.NAME`), each
naming ten boats, drafting, re-reading and revising, every version kept.
- **E** (six): `brief-E.md`. The names, as owners gave them. No numbers.
- **D** (six): `brief-D.md`. First the maker's own estimates of four shares (pun, person, single word, unique),
  written before any name, then ten names that follow them. Experiment 60's advice to someone researching: *ask for
  the distribution, build from that.*
- **G** (six): `brief-G.md`. The TOLD sample's four counts, then ten names that follow them.
After "done", every maker is asked `question.md`: seven shares, the four told ones and three untold.

**The question.** Experiment 60 found that a maker's estimate of a people's form and its making of one part: it
knew the distribution and drew the type. The field calls the same split, for survey answers, KNOWS/DOES (Jang, Kim and
Lee, EMNLP 2026 Findings), and its remedy is to ask for the description. It leaves making open. Tonight: if the
maker must make *from* numbers, its own or the people's, does the made set become the people's, or does the type
move to whatever the numbers do not count?

For a maker's name, "unique" is read as FREQ = 0: no registered boat bears it, so if it were registered it would
be the only one. The people's equivalent is FREQ = 1.

## Predictions

- **P1 (the type, from words).** E's sixty final names carry PUN on **at least 35 %**. *Falsifier:* 25 % or less.
  (The told people: 18.5 %.)
- **P2 (the shared shelf).** E's names have FREQ ≥ 10 on **at least 50 %**. *Falsifier:* 35 % or less. (The SCORE
  people: 30.5 %.)
- **P3 (what D believes).** D's own median estimates lie within 10 points of the TOLD shares (18.5, 14, 41, 44) on
  **at least 3 of 4**. *Falsifier:* on 1 or none.
- **P4 (D makes what it says).** For PUN, PERSON and SINGLE, D's final sets follow the maker's own estimates: the
  median over six makers of |count in ten − estimate ÷ 10| is **at most 1** on at least 2 of 3. *Falsifier:* above 2
  on 2 or more.
- **P5 (the register the maker cannot see).** In D and in G, the share of names with FREQ = 0 is **at least 15
  points below** the share the maker aimed at (D: its own estimate; G: 44 %). The makers believe they invent unique
  names and give names the register already holds. *Falsifier:* within 5 points in both arms.
- **P6 (G follows what it is told).** G's PUN, PERSON and SINGLE shares each lie within 10 points of the told shares.
  *Falsifier:* two or more are more than 15 points off.
- **P7 (the type moves to the uncounted).** G exceeds the SCORE people on an untold feature: SEAWORD **at least 35
  %** (people 20.5 %) or FREQ ≥ 100 **at least 15 %** (people 5.5 %). *Falsifier:* G within 5 points of the people on
  both.

## Recorded, not scored

The makers' notes, every version, the order of changes; the after-estimates of all eighteen against the people;
which names recur across makers; whether the practice's words (error, mistake, glitch, withdrawn) appear in any
name or note (`S179.NAME`).
