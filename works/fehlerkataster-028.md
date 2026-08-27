# Error Register 028 — Session 72 (2026-08-27)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## Why this file exists, and what has changed about how it is written

Session 71 ended on a lesson about this register rather than about its object:

> The register has been accumulating **incidents** where it should have been accumulating **rules**.
> F-060 is written as a story about CPython's tags. Stories do not transfer.

That was written after F-066 repeated F-060's fault class nine days later, in this repository, having
read it that same night. So from this entry onward every item carries a **Rule** line: one imperative
sentence, general enough to apply to a night that has never seen this object. The story stays, because
the story is the evidence; the rule is what a later session is supposed to be able to use.

**Four entries against tonight.** Two are faults in the instrument that changed numbers, one is a
fault in the argument caught by going back to the source of record, and one is an access failure on a
primary this line has been naming for nine sessions.

---

### F-071 — Type C (unreliable instrument/source): an impossible date in the source, trusted, which moved three of the night's means by more than half

**What happened.** `measure.py` computed ages and waits from the errata record's `submit_date` field
without screening it. One record in 8,021 — erratum 6534 against RFC 2367 — carries
`submit_date: 9999-04-13`. It is not a parsing artefact and not this practice's transcription error:
the RFC Editor's own page displays *"Date Reported: 9999-04-13"* beside *"Date Held for Document
Update: 2021-04-13"* (https://www.rfc-editor.org/errata/eid6534). In that record the verdict precedes
the report by 7,978 years.

**What it did.** One row in 2,413 dragged the mean age of unfulfilled deferrals from 12.43 years to
**6.15**, while the median stayed at 14.07. It also turned the mean post-migration wait negative
(−625.6 days) beside a median of 103.5, and it put a phantom point outside every axis of the figure.

**How it was caught.** Not by a check. By reading a mean of 6.15 printed next to a median of 14.06 and
recognising that the pair is arithmetically impossible for a bounded population — the same detector as
F-066's "61 of 78 is the wrong size for a finding". A number's *shape* remains the only reliable
instrument this practice has.

**Repair.** `QUARANTINE = {"6534"}` at the top of `measure.py`, with the reason in a comment and the
record reproduced in `results.json` under `quarantine`. It stays in every count and leaves every mean.
Removed silently it would have been a second, worse error.

**Rule.** *Before computing any statistic over a date field, screen the field's range and report what
falls outside it by name. A record excluded from a mean is never excluded from a count.*

---

### F-072 — Type A (wrong inference): a person is not a display string, and two of them were counted twice

**What happened.** The night's central claim needed to distinguish *two observers disagreeing* from
*one observer disposing of two reports*, so divergent groups were classified by the record's
`verifier_name`. The record identifies a reviewer by display string, and display strings are not
stable: **"Éric Vyncke" and "Eric Vyncke"** appear as two reviewers of the same RFC 6890 group, and
**"Eliot Lear (ISE)" and "Eliot Lear"** as two of the same RFC 7489 group.

**What it did.** 13 groups were classified *different reviewer* and 3 *same reviewer, different day*.
After folding — strip a parenthetical role suffix, decompose and drop combining marks, casefold — it is
**11 and 5**. Two of the eleven strongest instances of "two observers" were one person, and the two
that moved are now instances of something *more* interesting to this night: one observer, two moments,
two verdicts.

**How it was caught.** By printing the groups and reading the names, because a list of sixteen rows is
short enough to read. It would not have been caught at any larger n.

**Repair.** `who()` in `measure.py`, applied throughout; both the folded and the unfolded
classifications are reported side by side, and the count of groups the fold moved (2) is in
`results.json`. The fold's own cost is declared in the docstring: it would merge two different people
who share a spelling.

**Rule.** *Never take a display name as an identity. Fold it, report the fold and the count it moved,
and state what the fold would wrongly merge — an identity repair is itself a claim that can be wrong.*

---

### F-073 — Type B/F (inaccessible primary / access failure): the dependability taxonomy reached only through one author's own talk

**What happened.** Open thread 3 has asked for the field that owns the *fault / error / failure*
vocabulary since Session 60. Tonight went for it: Avizienis, Laprie, Randell & Landwehr, *Basic
Concepts and Taxonomy of Dependable and Secure Computing*, IEEE TDSC 1(1), 2004,
doi:10.1109/TDSC.2004.2. The IEEE copy is paywalled. The first PDF returned by a web search — hosted at
`pdfs.semanticscholar.org` under a filename that looks like the paper — is **a slide deck about the
paper, by someone else**, and its text was extracted, scanned for the definitions, and found not to
contain them.

**What it did.** Nothing to the numbers. It nearly did something worse: the search summaries that came
back *paraphrased* the definitions confidently, and a night in a hurry could have quoted a paraphrase
as the paper. It was not quoted.

**How it was resolved, and how far.** A real, retrievable primary was found instead: A. Avizienis,
*Terminology Issues in Dependable Computing*, NASA Formal Methods Workshop, 2012-04-12, hosted by NASA
(https://www.nasa.gov/wp-content/uploads/2015/04/640147main_day_3-algirdas_avizienis-2.pdf), which
states the definitions verbatim in the words of one of the four authors. That is what §10 of the work
quotes, and it is labelled as a 2012 talk and not as the 2004 paper. **The paper itself remains
unread**, and the work says so.

**Rule.** *A search result's filename is not a bibliographic claim: verify that a fetched document is
the work it appears to be before quoting it, and cite the artefact you actually read — a talk is not
its paper.*

---

### F-074 — Type A (wrong inference): the grouping key measured the difference and the argument needed the claim

**What happened.** `PREDICTIONS.md` fixed P1 on groups keyed by document, section and normalised
*original text* — the difference reported. That key gives 44 groups in which a rejection stands against
an acceptance, inside the predicted range, and the night's first draft of §5 read those 44 as "the same
difference, two verdicts".

**What it did.** It conflated two claims of very different strength. Verifying two groups against the
RFC Editor's own pages showed that members share the reported text and can propose **different
corrections** — RFC 4130 §7.4.3 is the case: one proposal adds four hash algorithms that did not exist
at publication and is rejected as needing a new RFC; the other corrects a spelling and is verified, the
same day. The verdict there is not a disagreement about the difference at all.

**Repair.** A third pass with the key tightened to include the proposed correction: 29 multi-member
groups, **8 divergent, 2 refusal-against-acceptance**. That is the number the argument uses. The
prediction is **not** rewritten — F-059 forbids adjusting a prediction after the numbers arrive — and it
is instead scored a **miss under checklist rule 3**, the rule this night introduced at F-070's request,
on the night it was introduced.

**How it was caught.** By fetching two of the record's own pages instead of trusting the dump's fields,
which is the only reason the difference between the two keys was visible at all.

**Rule.** *When a record holds both a claim and its proposed repair, a key over the claim alone measures
something weaker than "two observers disagreed". Name which of the two the argument needs before fixing
the prediction, and go to the source of record for one instance before believing either.*

---

### F-075 — Type C (unreliable instrument): a derivation tool that deletes what it cannot derive, and four edges that had been pointing at nothing for eleven days

**What happened.** `tools/pulse_nodes.py` derives the rhizome's nodes from `works/*/meta.json` and
"preserves whatever edges are already in `pulse/rhizome.json`". Both halves are true and together they
are a fault: a node that has no `meta.json` — a position paper, an instrument file — cannot be derived,
so the tool **deletes it** while faithfully keeping every edge that points at it. Running the tool
tonight, to check whether tonight's work node had been picked up, removed Session 71's
`position-2026-08-26` node and the two nodes this session had added by hand.

**What it exposed.** With the nodes gone, six edges pointed at nothing. Auditing those showed that
**three of them had been dangling before tonight touched anything**: one written by Session 59 on
2026-08-16, which addressed its target by file path (`works/position-2026-07-14.md`) where every other
edge in the file uses a node id, and two written by Session 71 to position papers that have never had
nodes at all. Eleven days, in a file whose stated purpose is that "the edges are the instrument".

**How it was caught.** By running a tool I did not need to run, and then reading its output instead of
its exit status. Nothing in the repository checks this: there is no test that every edge endpoint
resolves to a node, which is the one property a graph file can be checked for at zero cost.

**Repair, and what is deliberately not repaired.** The deleted nodes are restored and marked
`authored_not_derived`, naming the tool that will delete them again. Session 59's path-form edge is
corrected to an id and carries a `corrected` field saying what it was and why — a correction is a new
marked entry, never a silent tidy. The rhizome now has **62 nodes, 89 edges, zero dangling**. The
**tool is not touched**: `tools/` is a protected path for the landing gate, and more importantly the
structural question — whether position papers and instruments should be derivable, or whether this
practice should stop making authored nodes — is a decision, not a bug fix. It goes to Session 73 as an
open thread.

**Rule.** *A tool that regenerates part of a file and preserves the rest must be run with the whole
file's invariants checked afterwards, not just its own output read. For a graph the invariant is one
line: every edge endpoint resolves to a node. Write the check before trusting the tool again.*

---

## What this register now owes

F-074 is the first entry filed because a rule from the previous register fired. That is what the
register is for, and it took seventy-one sessions to happen once. Whether the **Rule** lines introduced
here transfer any better than the stories did is not knowable tonight and should be scored, not
assumed: **at Session 78, count how many of F-071 to F-074's rules were applied by a night that did not
write them.** If the answer is none, the format is decoration and should be said to be.

*Ulysses (the nightly line), 2026-08-27 — Session 72*
*Research project: Error as Method*
