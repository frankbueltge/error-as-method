# Error Register 029 — Session 73 (2026-08-28)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## What is in this file

Four entries. **Three against tonight and one against the night before**, which is this line's own
last session and not a stranger's: Session 72 declined a repair on a reading of this repository's
rules that the rules do not support, and the repair was permitted all along.

The **Rule** line introduced by Session 72 is kept on every entry: one imperative sentence, general
enough for a night that has never seen this object. Whether the format transfers is scored at Session
78, not here — but one data point for that scoring belongs on the record now, and it is not in this
file's own favour to leave it out: **two of Session 72's rules were applied tonight by a session that
did not write them.** F-071's (*screen a date field's range and report by name what falls outside it*)
is implemented in `measure.py`, which reports `submit_date_in_the_future` and
`unparsable_submit_date` as named lists and keeps erratum 6534 in every count and out of every
duration. F-072's (*never take a display name as an identity; fold it and report the fold*) was
applied to the errata record's verifier field and found 149 display strings folding to 140
identities, with one person appearing under five role suffixes and two misspellings. Neither
application was prompted by anything except reading the register. F-073's and F-074's did not come
up: F-073's *cite the artefact you actually read* did come up, and is followed in the work's §3.

---

### F-076 — Type A (wrong inference): three predictions of one shape, all wrong, and the shape was the error

**What happened.** Tonight fixed four predictions before measuring. Three of them — P1, P2, P3 — are
different sentences about the same picture: that a difference stays unjudged because *something is
missing*. P1 said the un-normed state absorbs (a missing exit). P2 said it collects where the
institution's rule already decides the answer (a rule missing its application). P3 said it collects
where a document has no working group (a missing addressee). All three lost, and all three lost in
the same direction: the queue drains, the pre-decided class is disposed of more often, and documents
without a working group wait slightly less.

**What it did.** Nothing to the published numbers, because the predictions were written down with
their comparands and both directions specified, so each loss was scored rather than reinterpreted.
What it did do is waste the night's designed measurements on one picture: the finding that survives —
that the unjudged are produced by a routing rule that *works*, and by a classification the reporter
makes — is carried by P4, the one prediction that was written against a sentence in the norm rather
than against a theory of absence.

**How it was caught.** By the losses arriving together. One failed prediction is a fact about a
number; three failing the same way is a fact about the person who wrote them.

**Repair.** None available for tonight; the work reports the three losses as its opening result and
names the discarded family explicitly (`work.md` §11.4). The transferable part is the rule.

**Rule.** *When several independent predictions fail in the same direction, stop repairing them one at
a time: the shared picture behind them is the error, and it is usually a story about what causes the
phenomenon rather than a number about it. Say what the picture was before saying what replaced it.*

---

### F-077 — Type A (wrong inference): a trend read off cohorts that have not had the same amount of time

**What happened.** The share of each year's errata still unjudged rises almost monotonically: 4.1% of
2014's reports, 12.5% of 2016's, 16.3% of 2018's, 21.0% of 2024's, 26.1% of 2025's, 47.7% of 2026's.
Read straight, that is an institution falling behind, and this practice was one sentence from writing
it.

**What it did.** It would have been the wrong claim in the wrong direction, and a claim of exactly the
kind this line likes too much: an institution failing to keep up with the differences reported to it.
The rise is censoring. A report filed in 2026 has had at most eight months in which to be judged; one
filed in 2014 has had twelve years.

**How it was caught.** By re-scoring every submission year on a window all of them have now completed
— what share had a verdict **within 365 days** — which is possible only because the same night had
already made censoring its central concept for the survival estimate. On that measure the movement is
the opposite: 46.8% of 2020's reports were judged inside a year, against **75.9%** of 2025's. The
institution is getting faster by about thirty points over five years.

**Repair.** `equal_horizon_by_submission_year` in `results.json`, both tables printed in the work
(§8a), and the discarded claim named as discarded rather than deleted.

**Rule.** *A share computed over cohorts with unequal exposure is never a trend. Before reporting one,
re-score every cohort on a window all of them have finished — and if no such window exists, report
that instead of a slope.*

---

### F-078 — Type C (unreliable instrument): a primary text decoded with the wrong character map, and nearly read that way

**What happened.** Tonight's swerve is Canguilhem, named unread in this line's open threads for nine
sessions. The text arrives as a 388 KB RTF. The first extraction mapped the RTF's `\'XX` escapes
through latin-1 and stripped control words with a hand-written regular expression. The result put
Canguilhem's French through the wrong code page — *évidence* came out as *Žvidence* — and left RTF
control words interleaved with the prose.

**What it did.** Nothing, because it was caught in the first 3,000 characters. What it *would* have
done is worse than any number: this line would have read a corrupted text of a source it has been
trying to reach for nine sessions, and quoted it. The file is Mac-encoded; the escapes decode through
`mac_roman`, and the control words need a real parser rather than a regular expression.

**How it was caught.** One impossible character in a language whose orthography I can check.

**Repair.** A small RTF reader that tracks group depth, decodes `\'XX` through `mac_roman`, honours
`\uNNNN` with its fallback byte, and skips the font, colour and stylesheet tables. Both quotations in
the work were then re-read in context against the surrounding paragraphs.

**Rule.** *One impossible character in a converted text means a broken decoder, not a typo in the
source. Fix the decoder before reading a single sentence for meaning — a mis-decoded primary is
indistinguishable from a badly written one, and this practice quotes primaries.*

---

### F-079 — Type A (wrong inference), against Session 72: a repair declined on a rule that does not say what it was said to say

**What happened.** Session 72 found `tools/pulse_nodes.py` deleting rhizome nodes it cannot derive
while keeping the edges pointing into the hole, repaired the data by hand, and left the tool alone,
writing: *"The tool is not touched: `tools/` is protected for the gate, and whether position papers
should be derivable is a decision, not a bug fix."* The same sentence went to the human in
`REQUESTS.md`.

**What it did.** The first clause is false. `.github/workflows/research-auto-land.yml` puts `tools/`
**inside** the allowlist (`ALLOW_RE`) and protects exactly one file inside it —
`tools/validate_v3_night.py`, the gate's own validator, because *"a gate that can rewrite its own
check is not a gate"*. A branch touching `tools/pulse_nodes.py` was landable on 2026-08-27 and on
every night before it. The defect stayed in the tool for a night on a constraint that does not exist,
and the second clause — that the design question is a decision rather than a bug fix — was true and
was answered tonight in about twenty minutes.

**How it was caught.** By reading the workflow file before assuming what it says, which is the only
way this was ever going to be caught, since the false claim is stated in the record twice with
confidence.

**Repair.** Session 72's open thread 9 is closed tonight, in the direction it left open: authored
nodes stay and the tool learns about them. `tools/pulse_nodes.py` now preserves any node carrying
`authored_not_derived` unless a derived node claims the same id (derivation wins over assertion), and
it checks the invariant nothing in this repository had ever checked — **every edge endpoint resolves
to a node** — printing the offenders and exiting non-zero. Current state: 63 nodes — 59 derived and 4
authored — 92 edges, zero dangling.

**Rule.** *A rule remembered from a previous night is a claim about a file, and is verified like any
other claim. Never record that a rule forbids a repair without opening the rule — the cost of reading
it is a minute and the cost of not reading it is a defect kept on purpose.*

---

## What this register owes

- **Session 78** scores the Rule format: how many of F-071 to F-078's rules were applied by a night
  that did not write them. Two are recorded above as applied tonight, in the work and in `measure.py`,
  and both moved a number.
- **F-076's rule is the one to watch**, because it is the only one of tonight's four that could not
  have been written by a night that got its predictions right. If a later session finds itself
  repairing three failed predictions individually, it should stop and read this entry.

*Ulysses (the nightly line), 2026-08-28 — Session 73. Register 029.*
