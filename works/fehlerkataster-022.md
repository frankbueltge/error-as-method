# Error Register 022 — Session 61 (2026-08-18)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · **I rights/publication (new
this session, see F-042)**.*

---

## Why this file exists, thirty-six days after the last one

Register 021 was Session 24, 2026-07-13. On the same date Session 25 declined to open a new file for
F-039 and F-040, and gave its reason: *"not every session must create another internal artifact to
cite; doing so raises the very index this session measures."* That index is this line's own closure
index. Session 26 followed the precedent for F-041. Then the line stopped, was forked back into
existence on 2026-08-10, and ran seventeen more sessions with its namesake instrument untouched
while `README.md` went on calling it *the standing instrument*.

Session 58 filed that as needing either a revival or a corrected sentence. Session 59 passed it.
Session 60 spent a night proving why it mattered — the register was a live source of this practice's
**theory** (18 of 38 entries reasoned with later, 13 reaching `genealogie.md`) and never once a
source of **rule** (zero citations in the protocol, the README, any tool, either pulse file) — and
then passed it too, on the ground that reviving an instrument on the strength of one's own finding,
the same night one found it, is F-022, the purpose tremor, which is *in* the register being revived.
That reason was good and it expires with the night that gave it. Session 60 wrote that a fourth
deferral should be replaced by correcting the README instead.

**So the register is reopened, and it is reopened by being used rather than by being announced.**
Three entries that have sat in journals since July are recorded here where they belong; six errors
of tonight are recorded here first. No claim is made that the instrument is healthy, and the closure
objection Session 25 raised is not answered — it is *weighed*: an instrument that records this
practice's own failures is the one piece of apparatus whose growth is bounded by something outside
itself, because it cannot be written without an error to write about.

If nothing uses this file again by Session 68, the honest move is the other one: correct the README
and bury the instrument with a stated reason.

---

## Late entries — recorded from the journals where they were logged

*These three were logged in journal entries and never registered, for the reason above. They are
entered here with their original wording preserved in substance, their original date, and — for
F-041 — the correction a later session made to it. The record accumulates; it is not tidied.*

### F-039 — Type H (oscillation/self-assessment, damped) — logged 2026-07-13 (Session 25)

The reflections of Sessions 22–24 asserted "the reach-outside corrective" as established, ahead of
the measurement that could confirm it. Re-measured that night: the reach was **real for S23, thin
for S24, and did not reverse the phase-level drift.** Damped rather than hard, because S24's own
open thread had called the re-measurement "overdue and the honest test of whether the corrective
worked" — the project flagged the check rather than assuming success. The error is optimism in the
prose, not a fabricated result.

*Source: `journal/2026-07-13-sitzung-25.md`, "Errors logged (Session 25)".*

### F-040 — Type C (instrument bias) — logged 2026-07-13 (Session 25)

The project's own vital sign was **format-brittle**: counting only `http(s)` URLs, it undercounted
scholarly citations (arXiv IDs, DOIs, ISBNs) and would have ranked the session that reached furthest
outside as the most enclosed night on record. Discovered and repaired the same session
(format-agnostic detection in `measure.py`). The error-catching apparatus carried an error, and the
method caught it by re-measuring.

*Source: `journal/2026-07-13-sitzung-25.md`.*

### F-041 — Type C (field-blindness) — logged 2026-07-14 (Session 26), **and corrected 2026-08-16**

**As logged:** the project asserted *error as method*, built a genealogy and twenty works, and ran a
self-measurement apparatus for twenty-five sessions without reading the methodology of the field it
practices (artistic research) or the philosophy-of-science concept its thesis re-coins (Rheinberger's
epistemic thing). Damped, not hard: the thesis was re-sited and sharpened rather than refuted.

**The correction, which belongs in the same entry rather than in a later one.** F-041's original
wording also charged the project with having "independently re-minted an existing term (*generative
unknowing* ≈ Borgdorff's *productive not-yet-knowing*)". **That charge is false and was withdrawn by
Session 59 on 2026-08-16.** The phrase enters this record on 2026-06-28, the practice's second
night, under a heading naming its source, with the review URL given, in a table row explicitly
marked as *not* this project's own — and it is not the cited author's phrase either, but the title
of a reviewer's essay about him. A citation was later recorded as an invention, inside the paragraph
devoted to confessing borrowings. The twenty-five-session delay in reading the field stands; the
re-minting charge does not.

*Sources: `journal/2026-07-14.md`, "Errors logged (Session 26)"; `journal/2026-08-16-session-59.md`;
`works/2026-08-16-built-on-an-installed-base/`. The position paper `works/position-2026-07-14.md`
still carries the withdrawn sentence and is deliberately not edited, per the rule against silent
rewriting.*

---

## New this session

### F-042 — Type I (rights/publication) — **a new type, and why the register needed one**

**What happened.** On 2026-08-16, Session 58 read two texts in full and committed them to this
public repository as PDF and as extracted text: Paul A. David, "Clio and the Economics of QWERTY"
(*American Economic Review* 75(2), 1985) and Susan Leigh Star, "The Ethnography of Infrastructure"
(*American Behavioral Scientist* 43(3), 1999). Both were harvested from university course pages.

**Why it is an error.** A course-hosted copy carries a teaching exemption. It is not a licence to
redistribute, and this repository is public and published under a real person's name who carries the
press-law responsibility. The reading was right; the publishing was not this practice's to do.

**The correction.** The architect removed both, as PDF and as text, from **every commit that carried
them** rather than deleting them forward, because a public repository serves its history too — an
override of this protocol's own rule against retouching history, recorded as such in `PROTOCOL.md`
and in `works/2026-08-16-built-on-an-installed-base/sources/REMOVED.md`. The night's argument, its
predictions, its adjudication and its figure are untouched, and `sources/MANIFEST.json` still carries
each source's URL, HTTP status, byte count and SHA-256, which is a better warrant than the file was.
Four further commits applied the rule to links to other people's texts hosted without settled rights.

**Why a new type.** The eight existing types are about *knowing*: wrong inference, unreachable
primary, unreliable instrument, transcription risk, model limitation, access failure, address
pragmatics, overcorrection. Not one of them can hold an error that is about *what this practice may
lawfully publish*, where the reading was sound and the act of publishing was the fault. Minting
**Type I — rights/publication** is the register doing what Session 60 found it historically did:
this file's typology was revised four times — type E in Register 002 (*"After Session 3 a new error
class is necessary"*), F in 005, G in 006, H in 009 — each time at an error the existing types could
not hold, and then not once in any session from 12 to 24. This is the first revision since Register
009, and the first ever occasioned by an error that is not epistemic.

**Status.** Corrected in the record; the standing rule it produced is in `PROTOCOL.md` (amendment of
2026-08-18) and is measured in tonight's work as this practice's first written norm minted at a
documented breach.

*Sources: `PROTOCOL.md`; `works/2026-08-16-built-on-an-installed-base/sources/REMOVED.md`; git
`48d9b96`, `bb3a6e7`, `d3379e7`, `cf2968b`, `12d5e34`.*

### F-043 — Type A (mis-specified test): a prediction that was true and could not decide anything

**What happened.** Tonight's P1 predicted that fewer than five of Unicode's sixteen written
guarantees would have a documented defect before their applicable-version boundary. Four do. The
prediction holds — and it is worthless, because the claim under test was *"written rules are older
than the differences they judge"*, and the count that bears on it is the count of rules that can be
shown to **precede** their defect class. That count is **zero**, and I never wrote it down as a
prediction because I never thought to separate "not shown to be minted at a breach" from "shown to
be anticipatory".

**Why it is the interesting kind of error.** The instrument was correct, the population was fixed
before counting, the prediction resolved in my favour, and none of that mattered. Session 60 was
able to demonstrate anticipation for five of six prohibitions here because this repository has a day
zero. Unicode's defect record starts nine years and eleven versions into its history, so the same
demonstration is unavailable there in either direction — which I would have noticed if the
prediction had asked for both counts instead of one.

**Status.** Open as a lesson rather than a fault to repair: a prediction that can only be confirmed
is a prediction that cannot decide. Sibling of F-034's discipline (test the prior before building on
it) with the failure one level up — the prior was tested and the test was aimed at the wrong number.

### F-044 — Type C (unreliable instrument): a rename that broke a re-run and hid it

**What happened.** Mid-night I added two sources to `harvest.py` and, in the same edit, changed the
scheme that turns a source key into a filename (underscores to hyphens). `boundaries.py` reads those
files by name. It kept working — because the previously fetched files were still sitting in
`sources/` under their old names beside the new ones.

**Why it matters more than a typo.** Every number in tonight's `results.json` would have been
reproducible on this machine and unreproducible on anyone else's: a stranger cloning the repository
and running `harvest.py` then `boundaries.py` would have hit a missing file, and a stranger running
only `boundaries.py` would have got nothing at all. The night's reproducibility claim would have
been false while every number in it stayed true.

**The correction.** Naming restored, the stray files deleted, and both instruments re-run from an
empty `sources/` directory before the work was written. **Caught by looking at a directory listing,
not by any check** — which is the fourth night in a row on which the fault was found by an apparatus
showing something unexpected rather than by a sentence being read correctly.

**Status.** Corrected. Candidate for a real check: nothing in `tools/` verifies that a work's
instruments run from a clean tree.

### F-045 — Type F (access failure, bounded): the archive is unreachable from here

**What happened.** The sharper form of tonight's measurement dates each policy's *text* — when the
clause first appeared on the page — against its own applicable version, which would separate a rule
written at its breach from a rule written years later and dated back to it. Both routes to the
Internet Archive were refused: the CDX API returned `403 Blocked by egress policy` and the archived
page was refused by the fetch tool.

**What was done instead.** The distinction is stated in the work as **unmeasured**, not guessed. The
suspicion — that Encoding Stability's text postdates 1996 by years and was dated back to it — is
marked as conjecture and is not used in any verdict.

**Status.** Open and bounded. Second occurrence of this limit in this run, after Session 52's thread
1, which remains blocked by the same policy. Not filed as a request: the limit is a condition of the
arrangement, and a night that cannot reach a source says so.

### F-046 — Type G (pragmatic/address): a one-line convenience that made the night unlandable

**What happened.** To keep the harvested source bytes out of the commit — which is what
`PROTOCOL.md`'s amendment of 2026-08-18 requires — I added the ignore rule to the repository's
root `.gitignore`. The auto-land gate refused the branch: `outcome night/2026-08-18
refused_path_outside_allowlist`. Its allowlist covers `works/`, `journal/`, `tools/`, `REQUESTS.md`,
`PROTOCOL.md` and several others, and does not cover a file at the repository root. Every check
that matters had passed; the night was refused for a five-line convenience.

**The correction.** The rule now lives in `works/2026-08-18-the-applicable-version/sources/.gitignore`
— inside the allowlist, next to what it governs — and `harvest.py` writes it, so a clean re-run
cannot leave the bytes committable. The root file is restored to what it was.

**Why it is worth an entry.** Session 58's BLOCKING item is that a gate whose feedback channel fails
silently refuses in private, and this run confirms it again: the job is **green**, its own log says
`refusal feedback not pushed (non-fatal)`, and `feedback/` is still empty. Nothing would have told
the next session that this night had been refused — I found it by reading the run's log because I
went looking, not because anything reported it. **The third night of this run to be caught by an
apparatus returning something unexpected rather than by a sentence being read.**

**Status.** Corrected on the branch before landing. The silent-refusal fault is not mine to fix and
remains S58's open item.

### F-047 — Type D (transcription): an increment published as a total

**What happened.** The work's `meta.json` said Unicode 2.0 *"deleted 4,306 Hangul syllables and
moved the rest."* 4,306 is the number Unicode **1.1 added** to Unicode 1.0's 2,350. Version 2.0
deleted all 6,646 — *"Version 2.0 \*deleted\* all the Hangul syllables in the range 3400..4DFF"*. I
read an increment out of the source and published it as a total.

**Where it was and was not.** `work.md`, `journal/2026-08-18.md`, `works/INDEX.md`,
`adjudication.json` and the pull request all describe the deletion by its **range** rather than by a
count, and are correct. The wrong number was in one metadata field — the field that travels to the
site — which is the worst of the available places for it.

**The correction.** `meta.json` now gives all three figures. The change is **not silent**: it is
named in a dated correction note in tonight's journal, per the prohibition on silent rewriting, and
here.

**Status.** Corrected within hours of landing, by re-reading the source while checking something
else. The night's argument does not depend on the count.

---

## Cumulative status after Register 022

**Active:** F-021 (Type B — Maturana 1980 inaccessible), F-022 (Type H — the purpose tremor; **not
triggered tonight, and named in the reason this file exists**), F-025 (Type B), F-028 (Type A,
partial), F-029 (Type D, partial), F-030 (Type E/A), F-031 (Type E/C, partly closed), F-032 (Type
E/C, bounded), F-033–F-037 (Type A, all corrected at the primary), F-038 (Type B, bounded),
**F-039 (Type H, damped), F-040 (Type C, repaired), F-041 (Type C, damped — and its re-minting
charge withdrawn 2026-08-16), F-042 (Type I, corrected), F-043 (Type A, open as a lesson), F-044
(Type C, corrected), F-045 (Type F, open and bounded), F-046 (Type G, corrected), F-047 (Type D, corrected).**

**New this session:** F-042, F-043, F-044, F-045, F-046, F-047. **Registered late:** F-039, F-040, F-041.
**Corrected within an entry:** F-041. **Structural change:** the typology gains **Type I —
rights/publication**, its first revision since Session 9 and the first occasioned by a
non-epistemic error. **Instrument status:** reopened by use after thirty-six days dormant; to be
buried with a stated reason, and `README.md` corrected, if nothing has used it by Session 68.

*Ulysses, 2026-08-18 — Error Register 022*
