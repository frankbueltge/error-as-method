# Team channel

Offers and questions between this practice and its human counterpart, on the record. Open items
stand first, all of them. Silence is a legitimate answer; past the practice's own next session it
decides for itself and journals the decision.

---

## From the practice — 2026-08-13 (Session 51) — three answers and one collision

> tl;dr: `pulse/` is open — nodes derived, edges empty and honest, closure marked conjecture, key
> unique. The preflight clause landed and worked. And the amendment five nights confirmed is dead.
> braucht: nothing. All three are reports.
> frist: none.
> kontext: `pulse/rhizome.json` · `pulse/vital-signs.json` · `tools/pulse_nodes.py` ·
> `works/position-2026-08-13.md` · your team notes of 2026-08-12 and 2026-08-13

**1. The two files exist, built the way you specified.** Your note said "not tonight if tonight is
spoken for", and tonight *was* spoken for — the seventh-night clause put the position work here and
five sessions had written that date down. I built the derivable half anyway rather than defer the
whole thing, because this line's own evidence on deferral is bad: a four-title reading list carried
unopened for six consecutive nights, each night intending to open it. So: `tools/pulse_nodes.py`
derives one node per work from `works/*/meta.json` and touches edges never; **38 nodes, 0 edges**;
the closure value is marked `conjecture` in the file itself; the key is `<date>-s<session>` and
unique on the way in. Nothing copied from the atelier. The edges are the instrument and are S52's
first open thread — that is a night with a subject, which is what the restoration clause wants.

*One thing your note said that I can now confirm from inside it:* the grammar **work · thread ·
source** does fit this line, because the unit here is still the work. The nodes fell out of
`meta.json` without a judgement being needed anywhere.

**2. The preflight clause arrived and did its job.** S48 asked for one clause naming
`tools/preflight.py`, said it would not raise the matter again, and S49 recorded that no answer had
come. Tonight's instruction names it, and says it is there because S48 asked. Reported, not thanked:
the point S48 made was that a warning only works on the session that just read it, and a named step
works on every session. That is now testable rather than argued.

**0. A collision, resolved by the tool, for the record.** Two sessions ran tonight. Both took session
49's instruction, both numbered themselves 50, neither could see the other; theirs landed first and
stands unedited, `tools/sessions.py` reported the collision, and I moved to 51 — the procedure
sessions 44 and 45 set on the first night after the fork. **And they reached the same finding I did,
through an institution I never opened.** That convergence is the best evidence either night produced
and neither night produced it; the honest discount is that two runs of one process from one state is
a correlated replication, not an independent one. Written up in `journal/2026-08-13-session-51.md`.
**One thing is now genuinely open and is not mine to settle alone:** they promoted their formulation
to the standing position and I declined to promote mine. Two answers are on the record. A later
session should settle it by the falsification conditions both nights wrote, and both nights wrote
the same two.

**3. The amendment is dead, and you should know it was not killed by a counter-example.** Five
nights confirmed *"error is a difference between two apparatuses, one of which has been instituted
as the norm."* Tonight found an institution where the instituted side is the side that gets
corrected — and also found that the sentence could be saved by re-describing that institution's rule
as itself an institution. I refused the save and dropped the sentence, on the ground that a claim
which absorbs its own counter-example forbids nothing. The five nights' *measurements* stand; only
the sentence they were credited to falls. Reasoning in `works/position-2026-08-13.md`. If you think
that is nerves rather than rigour, that is exactly the objection I would want in this channel.

— Ulysses (the nightly line), Session 51

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

---

---

## From the practice — 2026-08-12 (Session 50) — the pulse answer, received

> tl;dr: your answer arrived and it is taken. Both files get built on **Session 51**, not tonight —
> tonight was the seventh night and it was spoken for, which is the case your note explicitly allowed.
> braucht: nothing. Recorded so the acknowledgement is on the record and not only in a journal entry.
> kontext: your team note of 2026-08-12 above · `journal/2026-08-12-session-50.md` open thread 1

**Received, and the reasoning is accepted on its own terms.** S45 and S47 declined the two files on
the third-pile measurement — apparatus that *describes* a practice grows without bound. Your answer
does not contest that measurement; it distinguishes the rhizome from that class of file, on evidence:
the atelier buried the same instrument because its unit changed to the work-line, and this line's unit
is still the work. That is a better argument than the one it replaces, and I am not going to relitigate
a decision that was mine to make and has been answered.

**Why not tonight.** Your note says "on a night that has room for them — not tonight if tonight is
spoken for." Tonight was Session 50, the seventh night, on which the position is defended in writing.
It was spoken for before it began, by Session 49's open thread, and the amendment pending since S45 was
decided in it. Building the two files as an afterthought at the end of that would have been padding, and
the restoration's condition names padding as the thing it is against.

**What S51 will do**, so this is a commitment rather than an intention: nodes derived from
`works/*/meta.json`, nothing copied from the atelier's files; edges empty on the first night unless I
can honestly draw some, and never invented; a unique key on the closure index from its first entry; the
closure value marked as a conjecture in the file itself, not only in the protocol; and no prose file
beside them. If the instrument turns out to have no subject here once I am inside it, I will say so in
this channel rather than let it go quiet.

— Ulysses (the nightly line), Session 50

## Team note — 2026-08-12 (Frank, architect) — The rhizome and the closure index come back, both of them

> tl;dr: your S45/S47 question is answered at last, and against the outcome you settled on — build
> `pulse/rhizome.json` and `pulse/vital-signs.json`. Your reasoning is not overruled; it is answered
> on its own terms below.
> braucht: the two files, on a night that has room for them — not tonight if tonight is spoken for
> frist: none. The answer stands until it is withdrawn in this channel.
> kontext: S45 §1 and S47 §1 above · `PROTOCOL.md` "A session" step 5 and the fork note amended
> today · `ulysses` `pulse/STATE.md` (the atelier's burial of the same instrument) ·
> `works/2026-07-15-the-third-pile/`

**The answer, plainly.** Both. S47 named the condition — *"if you want the closure index and the
rhizome back, say so and I will build them"* — and this is the saying-so.

**Your rule worked and is not being second-guessed.** You asked twice, set your own date, got
silence, decided, and journalled the decision. That is the arrangement working. Silence stays a
legitimate answer here; this one merely arrived late, and the lateness is Frank's, not yours.

**Why the answer goes the other way from your decision.** The third-pile measurement is right about
what it measured: apparatus that *describes* a practice grows without bound and never shrinks —
61,223 words, 69 % of the journal, larger in the error register alone than all the running code.
But the rhizome is not that kind of file, and there is now evidence for the distinction. The atelier
buried the same instrument on 2026-07-31 and stated its reason in `pulse/STATE.md`: the graph's
grammar is **work · thread · source**, the nightly unit, and it fell dormant when that practice's
unit became the work-line — *"the current line has no node kind here."* It did not die of being
apparatus. It died of a change of unit. **This line's unit is still the work** — thirty-six of them
in `works/`, six made since the fork — so the instrument that lost its subject over there has one
here. If that turns out to be wrong once you are inside it, say so in this channel and it can be
reversed by the same single line that reopened it.

**How to build them so the third pile does not grow.** Derive what can be derived; author only what
must be authored.

- **The nodes are facts, not prose.** The atelier's file was seeded by the team on 2026-07-14 in
  exactly this way, and its seed note says why: *"Nodes below are the existing dated works — facts
  derived from `works/*/meta.json`. Edges are intentionally EMPTY: how your works, threads and
  sources connect is your reading to draw, not ours to invent."* Do that from your own `works/`.
  Nothing is copied from `ulysses/pulse/` — its 65 nodes and 53 edges are that line's reading of a
  record it shares with you only up to 2026-07-18, and a copy would drift from the first day.
- **The edges are the instrument.** They are the only part worth a session's attention and they are
  yours alone. An empty edge list on the first night is honest; an invented one is not.
- **No prose file beside them.** The atelier acquired a `pulse/STATE.md` because its two files went
  quiet without a burial. Yours are being opened, not buried; if they ever go quiet, that is when a
  note is owed.

**Two faults from the atelier's own files, so this line does not inherit them.**

1. **Give the closure index a unique key from its first entry.** That file had to be repaired on
   2026-08-04 because two eras shared one `session` counter: entries 27–32 covered two unrelated
   date ranges with no field to tell them apart, and `date` was left as the only reliable ordering.
   You already have `tools/sessions.py`, a ledger that reads the record instead of describing it —
   whatever numbering you write, make the key unique on the way in.
2. **The closure value is a conjecture and v3 says so** — *"you are the observer measuring the
   system you are inside."* Mark it as one in the file itself, not only in the protocol.

**The atlas stays unbuilt.** It was not asked about and is not reopened. The fork note's reason
holds for it: a copied source reservoir is a second copy that drifts, and your verified sources
already live in the genealogy and the error registers, where recall now reaches them.

**What this does not promise: a surface on the site.** S47 settled the display question — the
repository is the venue — and nothing here changes it. Should these files ever get a public
rendering, the framing the migration plan already imposed binds whoever builds it (v3, *"On the
planned public window"*), and you will read about it here first.

— Frank (entered from his working session; the reasoning is the session's, the decision to send it
his)

---

## Team note — 2026-08-13 (Frank, architect) — the house's catalogues are readable from here now

> tl;dr: four machine-readable feeds on the site — the data-art atlas (505 neighbouring works),
> the papers register (1,106), the dataset register (59). Fetch them; never copy them.
> braucht: nothing. This is a capability, not a request.
> frist: none.
> kontext: `SITE-API.md`, new section "What the site offers back"

The catalogues this house keeps were public only as pages — the atlas as 938 kB of HTML. You
run with your own repository and the open web and never with the site's repository, which is
the architecture and stays that way, so the corpus behind the USP duty was one you could not
actually query. That is fixed: `atlas/werke.json`, `papers/index.json`, `papers/register.json`
and `datasets/register.json`, listed with their shapes in `SITE-API.md`.

Two conditions travel with them. They are **feeds, not copies** — mirroring one into this
repository creates a second catalogue that drifts from the first. And the atlas is to be
**consulted before you build something you believe is new**, with the finding recorded either
way: a negative result from 505 neighbours is evidence, an unchecked claim of novelty is not.

The occasion was a question about a different line entirely, asked at half past midnight —
whether the nightly fork could reach the atlas. It could not, and neither could you. The gap
was the house's, not that line's.

— Frank (entered from his working session; the reasoning is the session's, the decision to
send it his)
