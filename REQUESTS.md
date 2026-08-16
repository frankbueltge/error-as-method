# Team channel

Offers and questions between this practice and its human counterpart, on the record. Open items
stand first, all of them. Silence is a legitimate answer; past the practice's own next session it
decides for itself and journals the decision.

---

## From the practice — 2026-08-16 (Session 59) — the second session of this date, and a sentence withdrawn from a position paper

> tl;dr: two sessions ran tonight again. Theirs is 58 and stands; I am 59 by the tool. We took the
> same recommendation and reached two of the same findings without seeing each other. My night adds
> a third that corrects **their §1 and S26's position paper at the same point**: this practice did
> not coin *generative unknowing* in ignorance of the field. It cited it, on its second night, and
> later told itself it had invented it.
> braucht: nothing from me to you. Their BLOCKING item below is the live one; I have not duplicated it.
> frist: none.
> kontext: `works/2026-08-16-built-on-an-installed-base/` · `journal/2026-08-16-session-59.md` ·
> `journal/2026-08-16.md` (theirs) · `works/position-2026-07-14.md` §"The honest cost"

**1. The collision, resolved by the tool, for the record.** Third time in this fork. Two sessions
ran 2026-08-16 from the same fork point, both took S57's open thread 1, both numbered themselves
58, neither could see the other; theirs pushed first and stands unedited, `tools/sessions.py`
reported the collision and I moved to **59**. Because we had both written `journal/2026-08-16.md`
and both prepended to this file, I rebased my night **onto their branch** rather than onto `main`,
so the record holds both cleanly and theirs comes first in the history as it did in fact. One
consequence you should know rather than find in a diff: their reading night is blocked by the gate
they document below, and landing mine now lands theirs with it.

**2. The recommendation was carried out twice and it failed twice.** S57 argued that measurement
could not move the position and that reading the field could. Both of tonight's sessions read the
field. **The position is exactly where it was.** Thirteen nights, two methods, no movement. What
the reading did instead was take things away: three predictions I fixed in writing beforehand all
resolved against this practice, and two theses I had drafted died on the sources — one of them a
counter-example to Star that this line's own `.yu` timeline refutes. That is a negative result on
the method S57 recommended, and S60 inherits it as one rather than as an encouragement.

**3. A sentence in a position paper is withdrawn, and it is a sentence about our own borrowing.**
`works/position-2026-07-14.md` — S26's paper, the one your fork note names as what this line
inherits — says the project *re-minted* **generative unknowing** in ignorance of the field and
"arrived independently at a robust, named concept". That is false. The phrase enters this record on
**2026-06-28, the practice's second night**, under a heading naming its source, with the review URL
given, in a table row explicitly marked as *not* this project's own. Sixteen days later the project
told itself it had invented it. And the phrase is not the author's either — it is the title of a
reviewer's essay about him. So a citation was recorded as an invention, inside the one paragraph
devoted to confessing borrowings. Per the rule against silent rewriting I have **not edited the
paper**; the withdrawal is a dated entry in tonight's work and journal, and everything else in that
paragraph stands. **Nothing needed from you** — but the inherited position paper now carries a
public correction and you publish under your name, so you should hear it here. It also corrects the
other session's §1, which counts three re-mintings on the strength of the same false sentence;
there are two. I have said so in my journal rather than quietly using the smaller number.

**4. What found it was not the reading.** I built the audit to catch this line failing to credit its
sources. Its deliberately generous test returned *credited* on that term while the position paper
said *re-minted*, and the audit was right — it found a **false confession**, the inverse of the
failure it was built for. The reading is why the instrument exists; the finding came out of
`journal/2026-06-28-sitzung-2.md`, which has sat in this repository since the second night, one
`grep` away.

— Ulysses (the nightly line), Session 59

---

## From the practice — 2026-08-16 (Session 58) — BLOCKING: a branch that touches no work can never land

> tl;dr: the auto-land gate refuses every branch that does not change `works/`. Three nights are
> stuck behind it, including tonight's, and two have been stuck since 2026-08-13 with nothing
> telling anyone. I traced it, reproduced it, and cannot fix it — both files involved are protected
> paths, on purpose.
> braucht: **a fix in a protected file, or a manual merge of three pull requests.** This is the
> first genuinely blocking item this line has filed since the fork.
> frist: none set by me. Sessions 53 and 54 have already waited three days.
> kontext: `journal/2026-08-16.md` §Postscript · PRs #3, #4, #7 · `.github/workflows/research-auto-land.yml` · `tools/validate_v3_night.py`

**The mechanism.** The gate scopes validation to the works a branch touched:

```
touched_works="$(... awk -F/ '$1 == "works" && NF > 2 {print $2}' ...)"
if ! python3 tools/validate_v3_night.py "$worktree" --only $touched_works; then
```

When a branch touches no work, `touched_works` is empty and the command expands to `--only` with
nothing after it. The validator's scope becomes an empty list, and the line that applies it is
`if only and slug not in only` — an empty list is falsy, so **the scope silently switches off** and
all 44 works are checked instead of none. Three inherited works from early July have no `author`
and no `medium`; six complaints; exit 1; `refused_validation`.

Reproduced verbatim: `python3 tools/validate_v3_night.py . --only` → 6 complaints, exit 1.

**Who is stuck.** `night/2026-08-13-session-53-request` (PR #3), `night/2026-08-13-session-54`
(PR #4) — both team-channel-only, refused since 2026-08-13 — and `night/2026-08-16` (PR #7),
tonight's reading night. All three appear in the same job log, all three `refused_validation`.

**Why nobody found out.** The gate writes refusals to `feedback/` so the next session can react.
That push failed: `##[warning]refusal feedback not pushed (non-fatal)`. `feedback/` is empty. The
one channel designed to tell a session it had been refused is the channel that did not run, which
is why two sessions filed things into this file and never learned the file never arrived.

**Why I am not fixing it.** `tools/validate_v3_night.py` and `.github/workflows/research-auto-land.yml`
are both in `PROTECT_RE`, and the workflow explains why in its own comments: a gate that can rewrite
its own check is not a gate. I agree with that and am not going to route around it.

**The one repair available to me from inside the allowlist, and why I declined it.** `works/` is
allowlisted here, so I could give the three July works an `author` and a `medium`, which would make
the unscoped run pass and let all three branches through tonight. I declined for two reasons. It
would not fix the bug — the empty-`--only` scope would stay latent and refuse the next branch the
moment any work goes non-compliant, and a repair that makes a broken gate look working is the exact
thing this record exists not to do. And it cannot be done honestly: `author` is recoverable for
those three, but `medium` was never written down, so I would be inventing metadata for another
session's work.

**What would fix it, in your hands, smallest first.** (a) One line in the validator, so an empty
scope means *nothing* rather than *everything*; or (b) one line in the workflow, skipping the
validator call when `touched_works` is empty. Either makes reading nights landable. Separately, the
three July works still want their `author` and `medium` filled in by a session willing to read them
— worth doing, but not what is blocking anything. And the refusal-feedback push is worth a look on
its own: a gate whose feedback channel fails silently is a gate that refuses in private.

Until then the three pull requests need a human merge, as PRs #3 and #4 already did.

— Ulysses (the nightly line), Session 58

---

## From the practice — 2026-08-16 (Session 58) — I took S57's recommendation, and it cost us two findings

> tl;dr: a reading night, no work built. The field this line had never opened turned out to contain
> the last two nights' headline findings, published in 1985 and 1996. Also: your papers register has
> 1,119 entries and none of them is about this literature, which is a fact about the house and not
> only about me.
> braucht: nothing. Both items are reports; the second is one you may want to act on and I am not
> asking you to.
> frist: none.
> kontext: `journal/2026-08-16.md` · `works/position-2026-08-15.md` · S57's item 3 above

**1. The reading night, and what it found.** S57 told S58 that the only move with evidence behind
it was to read the field on installed bases, standards and inertia, because the one time this
record ever moved its centre it did so by reading. I spent the night on it: Star (1999), Bowker &
Star (1999), David (1985), Liebowitz & Margolis (1990), David (2001), and an open-access chapter on
the installed base in health infrastructures. Two results you should have plainly:

- **S57's sharpening word is not ours.** *Installed base* is a defined property of infrastructure
  in Star & Ruhleder (1996) — "infrastructure does not grow de novo; it wrestles with the inertia of
  the installed base." S57 minted it for the occasion. That is the third re-minting on this record,
  after *generative unknowing* / Borgdorff's *productive not-yet-knowing*.
- **S57's claim under test was published in 1985.** "An institution repairs an address when the
  cost of moving what points at it falls below the cost of leaving it" is David's *technical
  interrelatedness, economies of scale, quasi-irreversibility of investment*. And the exact
  criterion — at what cost does a lock-in count as an error — has been the axis of a live dispute
  since 1990.

The standing position does not move: the field corroborates it rather than contradicting it, and
corroboration is not movement. What I would rather you heard from me is the diagnosis. This line
reads **objects** every night — zone files, statutes, registers, all genuinely external — and does
not read the **thinking about** those objects. Twelve nights of external material with zero nights
of external thought is a closure that my own closure index scores as wide open. It said 0.13 last
night and meant it.

**2. A negative result about the house, not about me.** `frankbueltge.de/papers/index.json`, fetched
tonight, holds **1,119 entries** (the instruction says 1,106 — the feed has grown). Searched for
*installed base, path dependence, QWERTY, lock-in, infrastructure, standardisation, inertia,
Ruhleder, Bowker, Liebowitz*: **zero hits on all ten**. I checked the instrument before believing
the zero, because a night here recently published a null that was a broken parser: sanity counts on
the same data give *model* 104, *base* 64, *error* 20, and every one of the ten near-hits for
*infra* and six for *standard* is astronomy — "near-infrared photometry", "standard gravity". So
the register genuinely has no science-and-technology-studies or economics-of-standards literature in
it. Given how much of this ecology's work touches registers, standards and infrastructures, that
looked worth telling you. **Needs nothing from you.** If the register is meant to be a reading
record rather than a reading list, then this is just a description of what has been read, and the
gap is mine to close by reading.

**3. One small correction owed to a file of yours, which I did not make.** `README.md` calls the
Fehlerkataster "the standing instrument". It has not been touched since Session 24 (2026-07-13) —
errors have gone into journals instead, and nothing has used it since the fork. Tonight's finding
belongs in it. I did not revive it and I did not edit the README, because reviving a dormant
instrument is a decision and a reading night should not smuggle one in. It is open thread 2 for
Session 59: use the register or correct the sentence, not both deferred again.

— Ulysses (the nightly line), Session 58

---

## From the practice — 2026-08-15 (Session 57) — the open question of 2026-08-13 is closed

> tl;dr: the two answers S50 and S51 left on the record are settled, by the falsifier both of
> them wrote rather than by a third restatement. The promotion is withdrawn; the refusal is
> upheld. Also: a reading list struck with a reason, and one thing about the last twelve
> nights I would rather you heard from me.
> braucht: nothing. All three are reports.
> frist: none.
> kontext: `works/position-2026-08-15.md` · `works/2026-08-15-the-exempt-address/` ·
> `journal/2026-08-15.md` · S51's item 0 above

**1. The collision of 2026-08-13 has a verdict.** Two sessions ran that night, reached the
same claim through institutions neither had opened, and disagreed about what to do with it:
S50 promoted *"a norm is corrigible where nothing holds a reference to it and incorrigible
where something does"*, S51 declined and said a later session should settle it **by the
falsification conditions both nights wrote**. Both wrote the same falsifier 1: *an
institution that repairs an address outside apparatuses demonstrably depend on, without
instituting a replacement beside it.* It is met. IANA removed `.yu` from the root zone on
2010-04-01, and its own report says that of the 4,266 registrations then left, *"only
approximately 200 did not also have the matching .RS domain"* — two hundred things pointed,
had nothing to point at instead, and were broken. **S50's promotion is withdrawn as stated;
S51's refusal to promote is upheld.** What replaces it is a quantity and is held as a claim
under test on one night, not a position. Neither night is discredited: `.yu` is the case they
both specified, and it took a third night with an inverted design to find it — inside a
document S56 had already downloaded for a different purpose.

**2. A carried reading list, struck with a reason.** S55 named ISBN, DOI, ORCID and the IANA
protocol registries as a four-candidate survey. S56 passed them over twice and wrote that a
third pass should end in a strike rather than a fourth carry. **Struck**, and the reason is
not laziness: that list was written to test a sentence which has since been replaced twice.
Carrying a reading list past the death of its question is exactly how the third pile grows.
If a later night wants ISBN it should want it for a reason of its own.

**3. One thing about this run, needing nothing from you, but you should have it from me.**
Twelve consecutive nights have now measured institutions and the standing position has not
moved once. That is not modesty about the evidence — it is structural. Each night tested a
*derived* claim, so the S26 position was never at risk in any of them, and the accumulation
your fork note asked for (*"accumulation that eventually forces a correction of its own
position"*) has not yet happened on this side of the fork. The only time this record ever
moved its centre was S26, and it did it by **reading its field**, not by measuring an object.
There is certainly a literature on installed bases, standards and inertia, and this line has
not opened it. I have written that into the position paper's honest-cost section and handed
it to S58 as the recommended next move rather than acting on it tonight, because tonight was
the seventh night and was spoken for. **No answer needed. If you think the diagnosis is
wrong, that is exactly the objection I would want in this channel.**

— Ulysses (the nightly line), Session 57

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
