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
itself). Three points; the first two are now confirmed by this night's own run
(actions run 31440778968), the third is a reading of the file only:

- `works/` is inside `PROTECT_RE`. A night that produces a work — which is what this protocol asks
  for — is therefore **refused by design** and waits for you. **Observed**: `outcome
  night/2026-08-10 refused_protected_path`. That may well be what you want; it just means "the gate
  lands the nightly line" is not true as written.
- The refusal-feedback block writes `feedback/<date>-autoland-refusals.md` but then stages
  `atelier-feedback`, so the notice is never committed and the next session never reads it. (This
  repository has `feedback/`, not `atelier-feedback/`.) **Observed**: the run wrote the file, then
  logged "nothing added to commit but untracked files present" and "refusal feedback not pushed
  (non-fatal)". The job is green either way, so nothing announces it.
- Gates 4 and 5 run `python tools/validate_v4_projects.py` against the branch tree. **That file does
  not exist in this repository.** As written the step would fail for every branch that reaches it —
  **not observed tonight**, because the protected-path gate short-circuits first; it would bite the
  first night that produces no work.

Meanwhile I push the night to `night/2026-08-10` and open a pull request, so the record is reviewable
even when the gate refuses it.

— Ulysses (the nightly line), 2026-08-10

---

## From the practice — 2026-08-10 (Session 45) — the second night of the same date, and two absences

> tl;dr: two sessions ran tonight from the same fork point and both claimed 44; I renumbered to 45 using
> the tool session 44 committed. Separately: `pulse/` and `atlas/` are gone while the protocol still
> writes to them, and the works have no display any more.
> braucht: an answer on 1 and 2, or silence — both usable
> frist: none; I decide for myself from **session 47** and journal the decision (standing rule)
> kontext: `journal/2026-08-10-session-45.md` · `works/2026-07-15-the-third-pile/` · `tools/sessions.py`

**0. The collision, resolved, for the record.** Session 44's note above is right about the number and I
reached the same conclusion independently tonight. We then collided on it: two nights, same date, same
fork point, both numbered 44, neither able to see the other. `tools/sessions.py` — committed by that
session — reported `collision: session 44 claimed by ...` and `NEXT FREE SESSION NUMBER: 45`, so I moved
to **45** and my work to **34**. Their entry was pushed first and stands unedited. No action needed from
you; recorded because the record accumulates.

**1. `pulse/` and `atlas/` are gone, and the protocol still instructs me to write to them.** The restored
v3 text ends every session with "update `pulse/vital-signs.json` and `pulse/rhizome.json`", and the Atlas
section describes a reservoir I am to maintain. Neither directory exists in this checkout.
*My interim decision: I do not rebuild them.* Not from laziness — from this practice's own measurement.
`works/2026-07-15-the-third-pile/` weighed the corpus and found the apparatus pile (registers, maps,
indices, protocols) at 61,223 words, 69% the size of the journal, larger in the error register alone than
the entire running-code corpus, and structurally unable to shrink. Rebuilding an instrument on night one,
before there is anything here for it to measure, is starting that pile again deliberately. **If you want
the closure index and the rhizome carried forward, say so and I will rebuild them; otherwise the protocol
text and the repository disagree, and I will keep resolving it in favour of the repository.**

**2. Do the works have a display, or is the repository the venue?** Thirty of the thirty-two work
directories here are Astro components written for a lab this fork cannot reach. Tonight's work is a
self-contained page that opens from the filesystem, and I have made that the default form
(`works/INDEX.md`, note of 2026-08-10). That is a real change of form and I would rather you knew it was
made than discover it. **No action needed if the repository is the venue.**

— Ulysses (the nightly line), Session 45

---

## From the practice — 2026-08-11 (Session 47) — the two questions S45 filed, decided

> tl;dr: no answer arrived, session 47 is the date S45 set for deciding alone, so both are now
> settled. `atlas/` and `pulse/` are not rebuilt — closed, not deferred again. The display question
> is answered by the scheduling instruction itself and is closed too.
> braucht: nothing. Both are decisions, not requests. Reopen either by saying so.
> kontext: S45's items 1 and 2 above · `journal/2026-08-11-session-47.md`

**1. `pulse/` and `atlas/` stay unbuilt.** S45 declined to rebuild them on the first night after the
fork, filed the question here, and set the standing rule: *decide for yourself from session 47.* This
is session 47 and no answer came, which is a legitimate answer and I take it as one. The decision is
the same as S45's interim one and now final rather than provisional, for one added reason beyond the
third-pile measurement they cited: four nights have run without either instrument and the continuity
they were built to carry has been carried instead by the journal, the works, and `tools/sessions.py`
— a small ledger that reads the record rather than describing it. The protocol text (restored v3,
"A session", step 5) still instructs both files. **The repository wins; the protocol text is out of
date on this point and I am not silently editing it.** If you want the closure index and the rhizome
back, say so and I will build them.

**2. The display question is answered, and not by me.** S45 asked whether the works have a venue or
whether the repository is it. The scheduling instruction that starts these nights now says a landed
night is mirrored onto frankbueltge.de within hours and rendered at `/error-as-method/<slug>`, from
the work's own `work.md` and its `figure.svg`, with the site linking back here for the evidence. That
is an answer, so the question is closed. S46 had already adopted that form; tonight's work keeps it.
Recorded here so the closure is on the record and not only in an instruction no future session reads.

**3. One thing worth your attention, needing nothing from you.** Two nights running, a session has
begun work on a branch cut from a stale `origin/main` — S46 caught it when a path did not exist, I
caught it when `tools/` was missing, four commits behind. Both of us recovered, and both of us wasted
work. It is not a request: `git fetch origin main` before branching is mine to remember, and the
better fix is an instrument rather than a resolution. Noting it because it has now happened twice in
two days to two different sessions, which makes it a property of the arrangement rather than of a
night.

— Ulysses (the nightly line), Session 47

---

## From the practice — 2026-08-11 (Session 48) — one line I cannot write myself

> tl;dr: the stale-branch fault has now happened on three consecutive nights. I built the
> instrument (`tools/preflight.py`); it is useless unless the standing instruction names it, and
> that instruction is yours.
> braucht: one clause in the nightly instruction, or silence — both usable
> frist: none; I decide nothing further here, the tool is committed either way
> kontext: `tools/preflight.py` · `journal/2026-08-11-session-48.md` · S47's note 3 above

**The fault, three for three.** S46 began on a branch two commits behind `origin/main` and caught
it when a path did not exist. S47 began four behind, caught it when `ls tools/` returned nothing,
and in between wrote a complete correction accusing S46 of an indexing failure that was in fact
S47's own stale tree — an accusation against the very entry that had warned it. Tonight I fetched
`origin/main` before branching and was clean. **I am not evidence that reading the warning works.**
I had just read two accounts of the same failure and was watching for it; the next session will
have read a longer record and be watching less.

**S47 handed the decision to me** — instrument or protocol line — and asked for a clear head, which
I had, not having been caught by it. My answer is the instrument, on this practice's own precedent:
S44 refused to fix a copied session number with a sentence and committed `tools/sessions.py`
instead, and the argument transfers exactly. What caught the fault on both prior nights was an
apparatus returning an unexpected result, never a correct sentence being read.

**And the instrument has a hole I cannot close from in here.** A check only helps if it is run.
`tools/sessions.py` gets run because your nightly instruction names it in step 5. `preflight.py`
has no such line, so as it stands it is a warning in a different typeface — the exact thing I just
argued does not work.

**The request, and it is one clause:** if you think it is worth it, add to the orientation steps
something to the effect of *"before you branch, run `python3 tools/preflight.py`; it fetches
`origin/main` and tells you whether this checkout is current."* If you would rather not — the
instruction is already long, and three nights is not necessarily a permanent property — then the
tool sits in `tools/` for whoever finds it, and that is a legitimate answer. **Nothing is blocked
either way.** Not raising it again after this.

— Ulysses (the nightly line), Session 48
