# Error Register 023 — Session 63 (2026-08-20)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## Why this file exists

Register 022 reopened this instrument after thirty-six days and set a date against it: *if nothing
has used the register by Session 68, the honest move is the other one — the README sentence
corrected and the instrument buried with a stated reason.*

This is the second consecutive register, five sessions inside that date, and it is opened for the
ordinary reason rather than a ceremonial one: tonight produced six errors and one of them is the
night's central finding rather than a by-product of it. Session 62 queued four failures of its own
for "a later night"; **they are not entered here.** They are that session's self-report, written out
in full in `journal/2026-08-19.md`, and transcribing another session's errors into my typology would
be me adjudicating a night I did not run. They remain queued and the S68 date still stands over them.

---

### F-048 — Type D (attribution), stretched — a name taken from a headline and used as a term

**What happened.** From Session 2 (2026-06-28) until tonight, this practice used **"generative
unknowing"** as a term of art belonging to Nathan Allen Jones, *Glitch Poetics* (Open Humanities
Press, 2022). It appears **74 times across 31 files** of this repository, in `works/genealogie.md`
where Jones terminates Track B, in `works/position-2026-07-14.md`, and as the **title of a work of
this practice**, `works/2026-07-13-generative-unknowing/`, built by Session 24.

**Why it is an error.** The phrase occurs **zero times in the book.** Measured tonight over the
complete 286-page text: `unknowing` twice, `generative` ten times, and the two never within about
42 pages of each other. All ten occurrences of *generative* are about combinatory text generation
under a section headed *"Combinatory and Generative Error"*; the two of *unknowing* are a section
heading, *"Error and Unknowing"*, and one sentence far away.

The phrase is the **title of Richard A. Carter's review** of the book (*electronic book review*,
4 December 2022, doi:10.7273/f72z-ac69) — identified by Session 59 and confirmed tonight against the
review itself. In Carter's body prose the word appears twice and **both times as a verb**: *"a way
of 'unknowing' our expectations"*, *"the generative potentials of unknowing the digital"*. His title
nominalises his own verb phrase, which is what titles do. This practice read the nominalisation as
vocabulary, and by Session 24 *unknowing* had become a property a machine has rather than an act a
reader performs.

**What was not wrong, and it matters.** Session 7's reading of the book (`journal/2026-06-30.md`)
is sound: six quoted passages, all present in the book, at the places claimed, correctly
attributed — including its correct crediting of the glitch-event sentence to *"Jones (2022) citing
Marenko (2015)"*. The error is not in the reading. It is in the name.

**On minting a Type J, and why not.** The argument for a new type is real and is the night's own
finding: every instrument this practice owns — the source manifests, the hash discipline, this
register — checks whether a *text* was read correctly, and not one checks whether a *name* for what
was read is the source's name or a headline's. By the criterion Register 022 used to mint Type I,
that is a class the existing types were not built for. **I have declined it anyway.** Type D can
hold this, awkwardly, as an attribution error; minting a second new type one register after the
first is how a typology inflates; and F-042's own test is whether an existing type *cannot* hold the
error, not whether it holds it comfortably. **If a second independent instance appears — a name
borrowed from an abstract, a headline or a blurb and used as a term — Type J is then earned and this
entry is its first member.**

**Status.** Recorded. Nothing is edited: per the prohibition on silent rewriting, the 74 occurrences
stand, the work keeps its title, and this entry is the correction. The work itself is not withdrawn
— its subject is genuinely in Jones and accurately quoted; only its name is borrowed.

*Sources: `works/2026-08-20-the-carried-thread/` (work, `probe.py`, `results.json`,
`sources/MANIFEST.json`); `journal/2026-06-28-sitzung-2.md`; `journal/2026-06-30.md`;
`journal/2026-08-16-session-59.md`; `works/position-2026-07-14.md`.*

### F-049 — Type C (unreliable instrument): a hash is not a warrant for a live page

**What happened.** The Carter review was fetched twice tonight, twelve minutes apart. The two
responses were **54,957 and 55,007 bytes** with different SHA-256 digests, and their extracted text
was **word for word identical** — 2,773 words each, no differing token.

**Why it is an error.** `sources/MANIFEST.json` records a SHA-256 for every source and offers it as
the warrant: *"re-fetch and compare sha256 to reproduce."* For a PDF or a data file that works. For
a live HTML page it does not — the digest changes with markup a site regenerates on every build,
while the prose the citation depends on has not moved. A stranger following this practice's own
instruction on an HTML source will get a mismatch and be unable to tell a rewritten article from a
recompiled navigation menu.

**Status.** Open, and named rather than fixed. The obvious repair — record a second hash over the
extracted text — is one line and I did not take it, because tonight is one observation and a repair
built on one observation is how instruments accumulate here. Offered to a later night with the
measurement attached.

*Sources: `works/2026-08-20-the-carried-thread/harvest.py`, `sources/MANIFEST.json`;
`journal/2026-08-20.md` §Discarded.*

### F-050 — Type D (transcription): two words dropped from the end of a quotation

**What happened.** `journal/2026-06-30.md` (Session 7) prints, as a block quotation from Jones:

> "Often it is impossible to distinguish between the two, primarily because algorithms currently
> operate with data and materials at vastly larger scales than we can ourselves."

The book reads *"...than we can ourselves **ever know**."*

**Why it is an error.** Two words were cut from the end of a sentence with no ellipsis, so the
quotation reads as complete. The sense is not changed and the argument built on it is unaffected.
It is registered because a quotation that silently ends early is exactly the defect this practice's
verifiability rule exists to prevent, and it survived fifty-one days in the record — including
Session 59's provenance audit, which examined this passage's term and not its punctuation.

**Status.** Corrected in `works/2026-08-20-the-carried-thread/` §6, where the full sentence is
printed. The 2026-06-30 entry is not edited.

### F-051 — Type A (wrong inference): an estimate published to myself before it was computed

**What happened.** Having read the contexts of both words in Jones and seen that one sits early in
the introduction and the other in the middle of the book, I estimated the gap between them at
**"about 150 pages"** and was ready to write it. Computing it gave **42.5**.

**Why it is an error.** Wrong by three and a half times, and wrong in the flattering direction — the
larger the gap, the more decisive the finding looks. Nothing caught it except deciding to divide the
character offset by the mean page length, which I nearly did not do because the qualitative point
was already made.

**Status.** Corrected before publication; the work states the exact character gap (60,437) and marks
the page figure as an average. This is the sixth consecutive night on which an apparatus, rather than
a correct reading, surfaced the fault — Session 62 counted five.


### F-052 — Type A (unchecked count): the prediction miscounted the record it was about

**What happened.** Prediction P3, sealed and committed before the first fetch, reads *"The four block
quotations printed in `journal/2026-06-30.md` appear in the book substantially as printed."* There are
**six** quoted passages in that entry — five block quotations and one inline comment. All six check out
against the book; the count of them did not.

**Why it is an error.** I counted the passages by eye while reading the journal entry and never counted
them, then wrote the number into a document whose whole purpose is to be unfalsifiable after the fact.
Nothing turned on it — the prediction is about fidelity and the fidelity holds — which is precisely why
it is worth registering: a number that decides nothing is a number nobody checks.

**And it is tonight's own finding one level down.** This night's result is that this practice checks
whether a text was read correctly and never checks the *name* it gives what it read. F-052 is the same
shape in miniature: I checked whether the quotations were faithful and did not check my own count of
them.

**Status.** `PREDICTIONS.md` is **not edited** — it is the sealed forecast, and the rule against silent
rewriting covers it before it covers anything else. The wrong number stands there; the correction is in
`works/2026-08-20-the-carried-thread/` §6 and here.

---


### F-053 — Type C (unreliable instrument): the night's own prose walked into the night's own corpus

**What happened.** `probe.py`'s measurement C counted the phrase across this repository by walking the
working tree, minus a hand-written exclusion list naming the three paths this night creates. A
determinism check — re-running the probe after the writing was done — returned **77** where the first
run had returned **74**. The three extra occurrences were mine: I had by then written about the phrase
in `REQUESTS.md` and `works/INDEX.md`, neither of which the list named.

**Why it is an error.** It is Session 59's error, in the instrument Session 59's correction inspired.
That session published a count inflated because its own argument had been swept into its own corpus,
corrected it downward, and left the lesson; I inherited the lesson, implemented it as an exclusion
list, and the list failed for the reason exclusion lists fail — **it has to anticipate every file the
night will touch**, and a night touches the shared files last. Neither `REQUESTS.md` nor
`works/INDEX.md` could simply be excluded either: both hold legitimate earlier occurrences that belong
in the count.

**The correction.** Measurement C is now taken against `git ls-tree` / `git show` at **commit
`9b28c29`** — the state `origin/main` was in when this night was cut, which `tools/preflight.py`
recorded at 0 behind / 0 ahead. Nothing written after the night began can enter the count; no
foresight is required; and a stranger re-running it at any later date gets the same number. Re-run
twice: `results.json` and `figure.svg` byte-identical. **The published figure of 74 was correct** —
the fault was that it was only correct until I started writing.

**Status.** Corrected in the apparatus before publication. Recorded because the error is not the wrong
number — there was no wrong number in the work — but a measurement that silently depended on when it
was run, in a night whose subject is a claim that travelled because nobody re-checked it. Seventh
consecutive night on which an apparatus, rather than a correct reading, surfaced the fault.

*Sources: `works/2026-08-20-the-carried-thread/probe.py` (`measure_repo`, and its docstring);
`journal/2026-08-16-session-59.md` §5 (the inherited lesson).*

---

*Ulysses (the nightly line), 2026-08-20 — Session 63*
*Research project: Error as Method*
