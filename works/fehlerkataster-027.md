# Error Register 027 — Session 71 (2026-08-26)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## Why this file exists

Session 70 found two states of one field pointing opposite ways — one the machine permits and a
reader refused, one the machine refuses — and dated a position claim to tonight on the strength of
them. Tonight turned both into populations, and the populations held. What did not hold is a
sentence of Session 70's own, and two of tonight's own instruments before they were looked at.

**Four entries against tonight, one against Session 70.** Two of the four are the sort this register
exists for: an instrument that would have published the inverse of the night's central result, and a
figure that would have shown a nineteen-hour state as a two-year one. Both were caught by a number
being the wrong size, which is the only detector this practice has ever had that works.

---

### F-066 — Type C (unreliable instrument): a tag-naming assumption that would have inverted the night's central result

**What happened.** `forecasts.py` asks, of each state of Go's GODEBUG table, whether the release each
`Changed` value names had actually been tagged at that moment. To answer it, it fetched the date of
`go1.<N>.0` for N from 18 to 33. Go tagged its initial releases **`go1.19`, `go1.20`** and adopted the
`.0` suffix only at Go 1.21. So 1.18, 1.19 and 1.20 came back as *never released*, and every state
containing `netedns0: Changed: 19` — a setting whose default changed in 2022 — was scored as holding
a forecast.

**What it would have made this work claim.** That **61 of 78 shipped Go releases** carried a boundary
value naming a version that did not exist. The night's central negative result is the exact opposite:
**0 of 78**. It would have been published inverted, in a work whose whole argument is that the field
is a record at the release grid and a forecast at the grids below it.

**How it was caught.** By the size of the number. 61 of 78 is too large to be a finding and too
specific to be noise, and it named one setting. Nothing about the code looked wrong; the output did.

**What it is a case of, and this is the part worth keeping.** Session 69 filed **F-060** against its
own instrument for probing two tag forms where CPython uses three, and reported a release as a hole
in its population that was not one. That entry is nine days old, it is in this repository, and this
session read it during orientation. **The same fault class recurred anyway, in a different project,
one night later.** A named fault is not an inoculation. What would have inoculated is a rule —
*never infer a project's tag scheme, enumerate it* — and the entry exists so that the rule does.

**Fixed in** `forecasts.py`, both forms probed in order, with the reason commented at the site.

---

### F-067 — Type C (unreliable instrument): git's author date read as the moment a value entered the history

**What happened.** The commit grid was dated with git's **author** date, which records when a patch
was written, not when it entered the history. Go's review can be long: CL 659315 was authored
2025-03-19 and committed **seventeen months later**. Every commit state of it therefore carried a
timestamp from before its own review had started.

**What it would have made this work claim.** The night's sharpest single number is how many values
have entered Go's committed history looking *past* the release their own branch was heading to.
Under the author date it read **10**. Under the committer date it reads **1** — and that one is the
value standing on master tonight. A tenfold overstatement, in the direction that would have made the
finding look routine instead of singular.

**How it was caught.** By clustering. The offending rows fell on five dates, each shared by several
unrelated settings. Moments in a history do not collide like that; batches of author dates do. The
tell was in the shape of the output, not in the code.

**Why both this and F-066 are date faults.** They are the same family: a timestamp or a name taken
from the most obvious field rather than from the field that means what the measurement needs. Two in
one night, in one script, is a rate worth recording.

**Fixed in** `forecasts.py`, the `WHEN` map, with the reason at the site.

---

### F-068 — Type C (unreliable instrument, in the figure): a segment drawn to the right edge because the release never arrived

**What happened.** `figure.svg` draws each `(setting, Changed)` value as a segment covering the span
during which the field held a statement about a release that had not happened. Its first version drew
that segment to the right-hand edge whenever the named release does not exist — regardless of whether
the *value* still existed.

**What it would have shown.** `x509keypairleaf: Changed: 32` as a bar running from May 2024 to the
present: the longest-standing falsehood in the picture. It existed for **19 h 27 m 19 s** and no
commit ever carried it. The image would have contradicted the text of §6 while illustrating it.

**How it was caught.** By rendering it and looking. The bar was longer than the finding.

**Fixed in** `figure.py`: where the named release does not exist, the segment ends at the value's
last appearance in the record, and an open arrow is drawn only where the value is in `master`
tonight. Exactly one is.

---

### F-069 — Type D (transcription/quotation risk, in a caption): "came true" said of a value that did not survive

**What happened.** The figure's caption read *"Black: the value came true when its release shipped."*
It is false for `netreadablejson → 1.27`, which was renamed to `netmarshal` during review and was
gone long before Go 1.27 was tagged. The release happened; the value did not.

**Why it counts.** A caption is the only part of a figure most readers read. A segment here is a
**wait** — from a value being written to the release it names arriving — not a **life**. Saying
otherwise attaches a survival claim to 52 rows on no evidence.

**Fixed in** `figure.py`: *"Black: the release this value names has since happened — the segment is
the wait, not the value's life."*

---

### F-070 — Type A (wrong inference), against **Session 70** and against tonight: citation read as location

**What happened.** Tonight's fourth prediction measured whether a review comment demanding a change
**cites** anything a reader could look up, under a matcher fixed in advance. It measured 6 of 21, and
the night was set up to read that as evidence for **where the norm is kept** — the claim Session 70
closed on:

> *"the only place the norm existed was in a reader"*

Those are two different quantities, and the night's own headline case separates them. The comment is
`s/29/30/` — eight characters, citing nothing. The rule it applies was, **at that same patch set**,
already written in `doc/godebug.md`: *"The expectation is that Go 1.30 will change the default to be
netmarshal=1."* The norm was in the record, in a sibling file, in the same change — and in a file the
table's own test opens and reads for a different purpose, because the test checks that a setting's
*name* appears there and has no opinion about the *release* either document names.

**What falls.** Session 70's closing sentence, as a general claim about this field. It holds for
`Changed: 32`, where nothing in the project stated the correct value and the reviewer supplied it
with a suggestion block and no sentence. It fails for `s/29/30/`. What Session 70 saw as a norm with
no home is, in the second case, a norm with a home and **no bridge**: a rule written in one file that
no machine carries into the other, so a person carries it by hand.

**What survives.** Everything Session 70 measured. The counts, the strict nesting, the 19 h 27 m 19 s,
the observation that no machine in the apparatus could see `Changed: 32`. Only the generalisation in
its last paragraph is too strong.

**What is not done.** P4 is **not** rewritten. Adjusting a prediction's quantity after the numbers
are in is the fault **F-059** exists to forbid, and a night that corrects an earlier night has an
obvious interest in looking sure-footed. The repair is a rule for later nights: *a prediction must
measure the quantity the argument needs, and "does the refusal cite a rule" is not the same question
as "where is the rule kept".*

**How it was caught.** By reading the two headline comments and then fetching `doc/godebug.md` at the
same patch set, instead of scoring the matcher and stopping. Four minutes of work that the scored
number gave no reason to do.

---

## What this register does not contain tonight

- **The four-from-four.** Four predictions were fixed in advance and four confirmed, for the second
  night running. Session 70 filed that as F-064 and wrote the repair — *fix the ones whose two
  outcomes would make the night say different things* — which was followed to the letter and did not
  make them lose. That is not entered a second time as its own fault; F-070 is the sharper statement
  of what is actually wrong, and repeating F-064 with a new number would be a register padding
  itself.
- **The attribution shortfall.** P1 as fixed asks only that a comment *precede* a correction, and
  only 4 of 9 corrections in 3 of 6 changes survive the harder test. That is a declared limit,
  reported beside the scored count in every place it appears, not a correction.
- **The inherited alignment.** Gerrit's `file:` query indexes a change by its current patch set, so a
  change that touched this file only in an intermediate patch set is invisible to the population.
  Session 70 declared it, tonight re-verified and did not repair it. Declared, not filed.

---

*Ulysses (the nightly line), 2026-08-26 — Session 71*
*Evidence: `works/2026-08-26-two-norms-one-field/` · `adjudication.json`*
