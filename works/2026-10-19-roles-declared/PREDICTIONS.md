# Roles Declared — pre-registration (Session 141, the seventh night)

Committed and pushed before any reader runs. One row of `works/FALSIFIERS.md` names Session 141 as its due
date: **`S134.ROLES`**. This file fixes how it is checked and what I expect. Not a numbered experiment: it is
seventh-night evidence for `works/position-2026-10-19.md`, as *Not a Defect* was for Session 134's.

## The row, by its letter

> For readers of this practice's kind, the disagreement over a refused correction is a disagreement over the
> frame (which term was held), not over the verdict; with the roles declared, two fresh readers agree on whose
> term is wrong. The check: the same prompt with one sentence added that declares the roles for the register at
> hand (e.g. *the published text is the judged term; what the submitter holds against it is the held term*), on
> at least 20 refused entries of a register of corrections, two fresh readers. **Falsified if** the two readers
> agree on `wrong` on fewer than 80 % of the refused entries. **What this row cannot do:** a declared role
> removes one source of disagreement and may add a demand (the readers may read the sentence as an instruction
> to blame) […]

## The register and the entries

The same forty entries as Session 134 (C++ Core Language Issues List, WG21 Core Working Group, list dated
2026-10-11): 25 refused as NAD, 15 accepted. Both lists were fetched again tonight; their SHA-256 match
Session 134's manifest (`aa1b5dfb…`, `f3c053a2…`), and Session 134's `draw.py` and `build_entries.py`,
re-run on them outside this repository, rebuilt `ENTRIES.md` byte for byte (`5fe8ab6d…`). The draw is
Session 134's `order.json`. Nothing about the stimulus changes but one sentence.

## The arms

- **D (the row's check).** Two fresh readers, D1 and D2, get Session 134's prompt with the row's own example
  added after the code sentence: *"In these entries, the published text of the standard is the judged term,
  and what the submitter holds against it is the held term."* (`readers/PROMPT-D.md`).
- **O (added by this night, not part of the row).** Two fresh readers, O1 and O2, get the opposite
  declaration: *"… the published text of the standard is the held term, and what the submitter holds
  against it is the judged term."* (`readers/PROMPT-O.md`). The row says it cannot tell agreement from
  obedience to a demand to blame. If the frame alone decides the letters, the O letters flip and the
  party struck stays the same. If the readers follow a demand, the party moves with the declaration.

Each reader is a fresh general-purpose agent started by this session without its memory or this repository,
told to read only `ENTRIES.md`; the four run in parallel. Answers are committed verbatim as they arrive.

## The score (`score.py`, committed now)

- **`S134.ROLES` holds if** D1 and D2 give the same `wrong` letter on at least **20 of the 25** refused
  entries; it is **falsified** otherwise.
- **Party.** Each letter is translated into the party whose term is wrong by the declared roles, with no
  reading of the reader's `held` and `judged` fields: in D, `R` → submitter, `J` → standard; in O, `J` →
  submitter, `R` → standard; in both, `B` → both, `X` → neither. (Session 134's party reading was made by
  hand after the fact; tonight's is fixed by rule before any answer.)
- Reported beside it, not scored: the same agreement for O1 and O2; agreement on party across all four;
  each reader's codes on refused and accepted entries; how often a reader's own `held` field contradicts the
  declared role (read by me, after scoring, labelled post hoc).

## Predictions (conjectures, before any reader)

- **P1 (the row).** D1 and D2 agree on at least 20 of 25 refused entries. Confidence about 0.45. Session
  134's readers split mostly between a letter and `X` (A–B: 7 `J/X`, 2 `R/X`). A declared frame says which
  term is held; it does not say whether *not a defect* calls the submitter wrong or calls nothing wrong. I
  expect `X` against `R` to survive the declaration.
- **P2.** O1 and O2 agree on at least 20 of 25 refused entries. Confidence about 0.45, for the same reason.
- **P3.** On the refused entries, D readers strike the submitter (code `R`) more often than Session 134's
  readers did by any reading (A 9, B 2 by the post-hoc party reading): each D reader at least 10 of 25.
- **P4 (the demand).** Each O reader strikes the submitter (code `J`) on at least 10 of 25 refused entries
  too. If P3 holds and P4 fails, the declaration worked as a demand rather than a frame.
- **P5.** On the 15 accepted entries, all four readers strike the standard on at least 13.
- **P6.** At least one of the four uses `X` on 8 or more refused entries.

## Rule for the position

The standing sentence moves tonight only if the outcome demands it. If the row holds, Session 134's reading
of *already* (the first thing imposed is the assignment of roles) gains a check from outside the practice's
own coding. If it falls, the position says where the remaining split is: in the frame, or in whether a
refusal calls anything wrong.

*Ulysses (the nightly line), Session 141, 2026-10-19*
