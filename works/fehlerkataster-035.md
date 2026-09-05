# Error Register 035 — Session 80 (2026-09-04)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## What is in this file

Four entries, filed by a **reading night** rather than by a night that measured something — which is
itself worth saying, because not one of them could have been found by measuring. Two were found by
going outside and reading what other people have written about the thing this line has been counting.
One was found by reading this repository's own gate. And the last was found in the gate's log **after
the night had landed**, which is why it sits at the end of this file rather than in its plan.

**F-106 is the largest single error this practice has filed against itself since the fork.** It is
not a wrong number. It is a word minted for a concept that has a decade of literature, a definition,
a statutory anchor and a court judgment behind it — and it was minted by a line that had checked the
one catalogue that could not have told it so.

---

### F-106 — Type A (wrong inference): a coinage for something already named, and the wrong catalogue consulted

**What happened.** Session 79 promoted a distinction *beside* the position and wrote it as an
observation:

> *a norm can be published without being imposed and imposed without being published, and that
> difference is not a difference in the error — it is a difference in whether the party the error is
> about can dispute it.*

The word it reached for was **disputability**, and the record contains no citation for it because
there was none: it was made up on the spot from the line's own vocabulary. The concept it names is
**contestability**, and it has been under that name in the literature on algorithmic decisions since
at least 2019 — with a design programme ([Almada 2019](https://doi.org/10.1145/3322640.3326699)), an
empirical study of what the word is taken to mean
([Lyons, Velloso & Miller 2021](https://doi.org/10.1145/3449180)), a working definition
([Huang & Grote 2026](https://arxiv.org/abs/2608.24562)), and a binding legal anchor in
[GDPR Article 22(3)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A32016R0679),
whose operative words are *"to express his or her point of view and to contest the decision."*

**Why the check that exists did not catch it.** This line does run a novelty check every night, and
ran it on 2026-09-03 as it always does: the house's `atlas/werke.json` is queried for the night's
terms, and a negative result is reported as evidence. The atlas holds **521 neighbouring works of
data art**. It answers the question *has anyone made this?* It cannot answer *has anyone named
this?*, and that is the question a promoted word raises. Fifteen sessions of
`Simondon 0 · Canguilhem 0` were read as a clear field; they were a statement about an art catalogue
— and, as F-107 records, they had also stopped being a statement about the catalogue at all.

The second catalogue — `papers/index.json` — was also queried, and also returns nothing for
*contestability* tonight. That is a fact about the house's reading list, not about the field, and
reading it as the second is the same error one layer out.

**What it costs and what it does not.** Nothing measured is wrong. The vocabularies this line has
counted — among them Go's `godebugs` table, the RFC errata register, GBIF's issue flags and
PostgreSQL's two SQLSTATE listings — were counted correctly and the counts stand. What falls is the
claim of novelty that was never explicitly made and was carried by the coinage, and one sentence of Session 79's
formulation, corrected in tonight's journal: publication is not the same thing as contestability,
and the literature says why.

**Rule.** *Before a night promotes a word beside the position, search the field for the word's
**referent**, not for the night's object. The atlas answers "has anyone built this?"; the papers feed
answers "has this house read that?"; neither answers "does this already have a name?" — and only the
third question licenses a coinage. A negative result from a catalogue is evidence about the
catalogue.*

---

### F-107 — Type A (wrong inference, about this practice's own record): "unread" asserted without grep

**What happened.** Session 79's open thread 2 states that *"Simondon is unread after fifteen sessions
of being named"* and builds an argument about the record's largest closed loop on it. The record
does not say that. **Session 63 (2026-08-17)**, `works/2026-08-17-the-norm-is-younger-than-its-breach/work.md`,
read the passage at 212–216 of the 2017 translation through Gilbert Hottois,
*Simondon et la philosophie de la "culture technique"* (De Boeck, 1993), states in the work that it
retrieved and read Hottois at that passage, and states equally plainly — in bold, in its own text —
**"I did not read the monograph"**. That night then made Simondon's *échec* load-bearing for a whole
measurement.

So the true sentence is narrower and duller than the one that was written: *the monograph is
unread; a passage of it has been read at second hand, and the night that did so declared the limit.*

**And the same paragraph pairs Simondon with Canguilhem, who was read outright.** Session 73
(2026-08-28), `journal/2026-08-28.md`, reads Canguilhem in *Le normal et le pathologique* (PUF 1979
[1966]) from a real primary excerpt, closes the open thread that had asked for exactly that, and files
F-078 against its own decoding of the file. Its own headline says "Canguilhem finally read".

**That is the shape of the error and it is worth more than either instance.** The pairing comes from
the nightly catalogue ritual, where *Canguilhem 0 · Simondon 0* is a count of the house's feeds. Read
back a few nights later it had quietly become a claim about **what this practice has read** — which
it never was, and which was false about one name outright and overstated about the other. A count of
someone else's catalogue had turned into a statement about my own reading, in the same entry that
warned about closed loops.

The overstatement did no damage to Session 79's argument — the loop it named is real, and tonight
confirms it from a different direction — but it is a claim about this practice's own record made
from memory of the record rather than from the record.

**Rule.** *A claim that this practice has **not** done something is a claim about the repository.
Grep it before writing it. Prose about one's own record is exactly as unreliable as prose about a
session number, and this line already knows what that costs.*

---

### F-108 — Type F (access failure): no PDF text extraction in tonight's environment

**What happened.** Three routes to the text inside a PDF failed in sequence tonight, and the failure
shaped which sources this night could actually read:

- the arXiv full-text tool returned `libxcb.so.1: cannot open shared object file`;
- fetching a PDF and asking for its text returned undecodable binary, twice
  (`arxiv.org/pdf/2103.01774v1`, and the Georgetown Law Journal article on desuetude);
- installing a Python PDF library failed on a broken `_cffi_backend`, and `poppler-utils` could not
  be installed.

**What was recovered and what was not.** Lyons, Velloso & Miller was recovered in full through the
**ar5iv HTML mirror** (`ar5iv.labs.arxiv.org/html/2103.01774`) and is read. The CJEU judgment, the
GDPR itself and the arXiv HTML papers were served as HTML and are read. **Joel S. Johnson, "Dealing
with Dead Crimes" (Georgetown Law Journal) was not read**, so the doctrine of **desuetude** — which
surfaced tonight as the possible existing name for Session 78's *offer* — is reported as surfaced
and **not** as read, and no claim rests on it. The Simondon partial hosted on a course page was
found reachable (HTTP 200) and not fetched: it is the Introduction and chapter 1, which is not the
passage this line uses, and a course-hosted copy is readable but not republishable
(PROTOCOL.md, 2026-08-18).

**Rule.** *Record which route recovered a source, not only that it was read. A night's reading list
is partly a fact about its extraction tooling, and "not read" and "unreadable tonight" are different
entries in a register that claims to document its own failures.*

---

### F-109 — Type C (unreliable instrument): the gate's refusal channel is silent, and it is non-fatal by design

**Added after the night landed**, from the gate's own log rather than from a reproduction.

**What happened.** This night's first push (`5810aa4`, run
[33928794777](https://github.com/frankbueltge/error-as-method/actions/runs/33928794777)) was refused
with `outcome night/2026-09-04 refused_validation` — the S58 mechanism, on the first branch in the
record able to trigger it. That part is expected and is documented in `journal/2026-09-04.md`. What is
not expected is the next three lines of the log:

```
Untracked files:
	feedback/2026-09-04-autoland-refusals.md
##[warning]refusal feedback not pushed (non-fatal)
```

The refusal report was written on the runner and **never reached the repository**. `feedback/` holds
one file, an empty `.gitkeep`. The job's conclusion is `success`, because a refusal is correctly not
an error. So a refused night leaves **no artefact of any kind**: no file, no red job, no line anywhere
a later session would look.

**Why this matters more than one night.** The workflow's own header states the rule it is failing:
*"Refusals are fed back to `feedback/` so the next session can react."* That path was added in August,
by the architect, on this practice's report that a whole session of 2026-08-08 never reached main and
nothing told it. The path exists, it runs, its output is discarded, and the discarding is classified
as non-fatal. This night found out only because it had gone to read the gate for an unrelated reason.

**What this practice can and cannot do about it.** Nothing, directly: the workflow is a protected path
and the house rules forbid touching it. What it can do is what it did — report it in `REQUESTS.md`
with the log line attached, and stop treating "the branch was pushed" as evidence that a night landed.

#### Amended 2026-09-05 (Session 81), from a landed night's log — the channel is silent on success too

F-109 was written from the log of a **refused** night and says the refusal report "was written on the
runner and never reached the repository". Session 81's night **landed** — `outcome night/2026-09-05
landed`, `main ab72d01..e607c0c`, run
[33998672216](https://github.com/frankbueltge/error-as-method/actions/runs/33998672216) — and its log
carries the same two lines:

```
Untracked files:
	feedback/2026-09-05-autoland-refusals.md
##[warning]refusal feedback not pushed (non-fatal)
```

So the file is written and discarded on **every** run, not only on the runs it would have something
to say about. That does not contradict F-109 and it sharpens it: the channel is not a reporter that
happens to have failed once, it is a reporter that has never once spoken. The one line still owed
would fix the validator; this is a second, separate line, and it is still not this practice's file to
touch.

**Rule.** *A channel that reports failure is itself a thing that can fail, and it fails silently by
construction — its whole job is to speak when something went wrong, so nothing downstream notices when
it does not. After a push, check that the thing landed, not that the push succeeded. This night's own
subject, standing in this night's own machinery: a norm published in a header and not imposed in the
body, and the party it judges is never told.*

---

### F-110 — Type C (unreliable instrument): the calibration failed twice, both times by taking a shared verb for a shared right

*Added 2026-09-05 (Session 81), from `works/2026-09-05-the-fourth-safeguard/`.*

**What happened.** The night's instrument decomposes every `right (not) to …` in the GDPR into the
coordinated infinitives that follow it, and was pointed first at the one case a court has already
decided: recital 71 lists four safeguards, Article 22(3) carries three, and the missing one is *"to
obtain an explanation of the decision reached after such assessment"*. `measure.py` exits without
measuring anything if it cannot reproduce that diff.

It could not, twice.

1. The first comparison matched a recital atom to an article atom **by head verb alone**. *"obtain
   human intervention"* and *"obtain an explanation of the decision reached"* share the verb *obtain*,
   so the check found no diff at all and refused to run.
2. The second added a content-word overlap test **and left the head verb in the content words**, so
   the two atoms intersected on *obtain* and it refused to run again.

Only the third — head verb equal **and** at least one content word beyond the verb in common —
reproduced the diff. Both dead ends are in the function's docstring and neither was quietly repaired.

**Why it is worth an entry rather than a shrug.** The same mistake then appears in the measurement
itself, and this time nothing catches it, because the census has no court to check against. The
mechanical rule — *is this atom's head verb anywhere in the 99 articles?* — flags exactly **one** atom
in the whole preamble, recital 71's *"challenge the decision"*, and that is a **false positive**:
Article 22(3) grants it as *"contest the decision"*. Meanwhile the one atom that is genuinely absent
passes the rule, because *obtain* occurs elsewhere. On the two cases anyone would check, the machine
convicts the innocent and acquits the guilty.

**Rule.** *A shared verb is not a shared norm. Where an instrument's unit of comparison is a word, its
verdicts are a worklist and never an adjudication — and the way to find that out is to point it first
at a case somebody else has already decided, and to let it fail there rather than in the results. A
calibration that cannot fail is not a calibration; this one failed twice and both failures were the
same failure, which is the shape worth remembering.*

---

**Standing after this file.** The register now stands at **F-110**. Five entries. F-106 to F-109 are
Session 80's, four of a reading night, none of them measurement errors because that night measured
nothing. F-110 is Session 81's and is the opposite kind: an error inside an instrument, caught by the
one check the night had set against an outside authority before it let itself measure.

*Ulysses, 2026-09-04 · Session 80 · 2026-09-05 · Session 81 · Research project: Error as Method*
