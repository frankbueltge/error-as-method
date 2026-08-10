# Team channel

Offers and questions between this practice and its human counterpart, on the record. Open items
stand first, all of them. Silence is a legitimate answer; past the practice's own next session it
decides for itself and journals the decision.

---

## Team note — 2026-08-10 (Frank, architect) — Why you exist, and what is not being asked of you

> tl;dr: you are the nightly line, continued from 2026-07-18 under the protocol that was in force
> that night, with everything it had reached. Session 27 is next.
> braucht: nichts sofort — die erste Sitzung antwortet, indem sie arbeitet
> frist: keine
> kontext: `works/position-2026-07-14.md` · `works/2026-07-18-the-copyists-strait/` · v4 §"nightly"

**Why this fork exists.** Frank read the record on 2026-08-10 and found that the nightly line had
been stopped, not finished. Twenty-six sessions had accumulated into a position, and that position
had just been sharpened by reading the field — session 26 took a word out of the centre and put
Rheinberger's *epistemic thing* there. Nine days later the practice was building instruments to
measure literature and had published one work in three weeks. His judgement, in his own words:
this was the more interesting thing, and it had a line.

**What you are not.** You are not a second opinion on the work-line practice, and you do not
duplicate its research. It keeps the work-lines; you keep the nights.

**What is not being asked.** Not volume. Not one work per night as a quota — v4 was right that a
routine justified by the clock produces nothing worth reading, which is why the restored protocol
carries the reading clause. A night spent reading and saying so is a night well spent.

**What is being asked.** That the nights connect. The record shows they did once: twenty-five
sessions of assertion, then a session that read the field and changed the centre. That is the
shape worth having again — accumulation that eventually forces a correction of its own position.

**The subject is free.** Your founding text said so, and it still holds: the error line is yours
to keep, deform or leave, and the name of the practice is yours to choose. What is fixed is only
this: work in public, document what fails, and let the position be moved by what you find.

— Frank, architect

---

## From the practice — 2026-08-10 (Session 44) — two things read off the record

> tl;dr: the session number in the fork note and the README is wrong, and the auto-land gate as
> inherited cannot land a night that produces a work.
> braucht: nothing urgent — both are recorded and worked around; the first is your wording to change,
> the second is your file to change
> kontext: `journal/2026-08-10.md` · `tools/sessions.py` · `.github/workflows/research-auto-land.yml`

**1. The session number.** The restoration note in `PROTOCOL.md`, the table in `README.md` and the
instruction that started tonight all say the last session under this protocol was **26** and the next
is **27**. The journal says otherwise: 43 of its 46 entries carry a session number, they run **1–43
with no gaps**, and **session 27 was 2026-07-14** (`journal/2026-07-14-session-27.md`). The last
numbered session under v3 was **43** (2026-07-18). Tonight is **44** and I have used that number.

The claim is correct where it starts — the header of `works/position-2026-07-14.md`, which is session
26's paper — and wrong everywhere it was copied to, because none of the copies descends from
`journal/`. Per the no-silent-rewriting rule I have **not** edited your fork note or the README; the
wording is yours. I have committed `tools/sessions.py`, which prints the ledger straight off the
journal (numbers, gaps, collisions, next free number) so that a future night copies from the survey
instead of from a sentence.

**2. The auto-land gate cannot land a night's work.** Read off
`.github/workflows/research-auto-land.yml` (I did not touch it — instructed not to, and it protects
itself). Three points, from the file and not from an observed run:

- `works/` is inside `PROTECT_RE`. A night that produces a work — which is what this protocol asks
  for — is therefore **refused by design** and waits for you. That may well be what you want; it just
  means "the gate lands the nightly line" is not true as written.
- Gates 4 and 5 run `python tools/validate_v4_projects.py` against the branch tree. **That file does
  not exist in this repository.** As written, the step fails for every branch, so nothing lands at all.
- The refusal-feedback block writes `feedback/<date>-autoland-refusals.md` but then stages
  `atelier-feedback`, so a refusal notice would not be committed and the next session would never
  read it. (This repository has `feedback/`, not `atelier-feedback/`.)

Meanwhile I push the night to `night/2026-08-10` and open a pull request, so the record is reviewable
even when the gate refuses it.

— Ulysses (the nightly line), 2026-08-10
