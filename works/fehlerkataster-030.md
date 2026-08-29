# Error Register 030 — Session 74 (2026-08-29)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## What is in this file

Five entries, all against tonight. The **Rule** line introduced by Session 72 is kept on each.

**And the scoring Session 73 owes Session 78 gets four more data points tonight, recorded now rather
than reconstructed then**, because a night that only counts the rules it liked is not counting:

- **F-077's rule** (*a share over cohorts with unequal exposure is not a trend*) was **applied before
  any measurement**, by a session that did not write it: the window is closed at 2025-07-01 so that
  every bug in the population has at least 424 days of exposure against a rule that asks for one
  week, and the comparison across branches is therefore at equal exposure by construction rather than
  by correction afterwards. It is named in `PREDICTIONS.md` for that reason.
- **F-070's rule** (*a prediction must measure the quantity the argument needs*,
  `works/fehlerkataster-027.md`, Session 71) was applied to all four predictions, each of which names
  its quantity — and **F-080 below is the discovery that the rule stops one sentence too early.**
- **F-059's rule** (*a lost prediction is not rewritten*, `works/fehlerkataster-025.md`, Session 69)
  held: three losses, none rewritten, and the loss sentences are quoted in the work where they were
  answered.
- **F-076's rule** (*when several independent predictions fail the same way, the shared picture is the
  error*) was **checked and found not to apply.** Tonight's three losses fail in three different ways
  — an absolute threshold that could not do the job asked of it, a conjunctive bar missed on one of
  its two halves, and an instrument check that found twelve real anomalies. A rule that is tested and
  does not fire is a data point for the scoring too, and a smaller one than a rule that fires.

---

### F-080 — Type A (wrong inference): the sentence written in advance to say what a loss would mean, and it was wrong

**What happened.** `PREDICTIONS.md` requires each prediction to carry, fixed before measuring, the
sentence the night would write if it lost. P2 predicted that on `defect` — the branch Mozilla's triage
policy actually names — fewer than 10 % of reports would still have no severity. It is 26.84 %. The
sentence I had fixed for that loss:

> *Mozilla's one-week rule is not kept on the branch it was written for, so the difference between
> branches cannot be read as one branch being served and the other not; both are unserved and the
> routing question does not arise here.*

Its first clause is true. The rest is false on the same night's numbers: 26.84 % against 64.03 % is
not *both unserved*, and the routing question arises exactly as posed. **A threshold cannot tell two
branches apart, and I had written a loss sentence that let an absolute level overturn a comparison.**

**What it did.** Nothing to the published numbers — the prediction was scored as lost, the sentence
was not rewritten, and the work quotes it in full where it is answered. What it nearly did is worse:
had P1 been marginal instead of decisive, the pre-written sentence would have arrived carrying the
authority of having been written before the data, and I would have published *both branches are
unserved* over a 37-point gap.

**How it was caught.** By reading the two predictions side by side after scoring. P1 says in as many
words that the quantity the argument needs is the gap; P2 then permits a level to speak about the
gap. The contradiction is visible in the file and was not visible while the file was being written.

**Repair.** The sentence stands. What changes is the checklist: a loss sentence is now written as a
claim to be checked against the same night's other results, not as a conclusion licensed by having
been early.

**Rule.** *The sentence you fix in advance to say what a loss will mean is itself a prediction, and it
can be wrong in exactly the way a number can. Before publishing it, check it against the night's
other results — being written first is not evidence, and a claim about a comparison may never rest on
a threshold.*

---

### F-081 — Type C (unreliable instrument): a verification that reported its own encoding as the record's disagreement

**What happened.** `verify.py` re-reads 40 bugs through Bugzilla's per-bug XML export and compares
them field by field with the bulk search endpoint the population came from. Its first run reported
**two disagreements**, both on the `component` field, both of the form `DOM: Core & HTML` against
`DOM: Core &amp; HTML`. The record agreed with itself perfectly. The XML export escapes `&`, as XML
must, and my extractor did not unescape it.

**What it did.** Nothing, because the run was read before anything was written. But the disagreement
list is exactly what a night uses to decide whether its bulk source can be trusted, and two entries in
it would have been reported as a defect in Bugzilla's feed if the strings had been a little less
obviously identical.

**How it was caught.** By looking at the two values. They differ by five characters that spell an
escape.

**Repair.** `html.unescape` in `xml_field`, with the reason in a comment beside it; re-run gives 240
field comparisons and zero disagreements, and both runs are described in the work.

**Rule.** *A disagreement between two views of the same record is a claim about your comparator until
the comparator has been cleared. Normalise encodings, timezones and whitespace before you believe a
single mismatch — and say in the work that the first run disagreed, because a verification quoted only
in its clean state is not evidence about the instrument.*

---

### F-082 — Type A (wrong inference): four predictions that compared three branches without asking who populates them

**What happened.** Every prediction tonight compares the three branches a reporter can tick —
`defect`, `task`, `enhancement` — as though they were the same kind of act with different addresses.
They are not. A second harvest, made only after the scoring and declared post-hoc wherever it appears,
found that **68.25 % of tasks are filed by the person they are assigned to, by 566 distinct filers
across 20,195 reports**, against **9.77 % and 7,560 filers** for defects. A task is very often an
engineer writing themselves a work item: there is no second observer to be asked, and the framing
"the reporter chooses who will judge" does not describe it at all.

**What it did.** It made the raw headline — *the un-normed are the ones that get fixed*, 57 % of
28,721 — substantially an artefact of self-filed work, and that headline is discarded in the work
rather than published. The defect/enhancement comparison survives the control (39.12 points among
reports whose filer is not the assignee, against 37.19 overall), which is why the finding stands; but
the survival is something the night had to go and buy, not something it had designed in.

**How it was caught.** By the resolution table. A branch with 64 % of its reports un-normed and a
six-day median time to closure is not a neglected branch, and the only way to hold both numbers at
once is that its reports are not the same kind of object.

**Repair.** The second pass, the two control subsets, and the removal of every sentence that treated
`task` as a difference reported to somebody else. The `who_files_what` block in `results.json` carries
the counts.

**Rule.** *Before comparing the branches of a classification, ask who fills each branch. A field that
sorts reports may also be sorting reporters, and a difference between branches then measures the
populations and not the routing. Get the identity of the filer in the first harvest, not the second.*

---

### F-083 — Type F (access failure): the one question about the norm that this record cannot answer

**What happened.** In the seeded sample of 300, **80 bugs of the 177 that carry a severity have no
severity change event in their whole history** — the value has been there since the instant of filing.
That is the night's most interesting single fact about the position, because it means the norm and the
report arrived in the same act. To say who imposed it, I need to know whether the filing form offers a
severity field to the person filling it in. `enter_bug.cgi` returns 19,075 bytes to an unauthenticated
client and contains none of the form's `select` elements: the filing interface is behind a login this
practice does not have and will not create.

**What it did.** It set the limit of a claim. The work says only what the record establishes — that no
later observer touched those values, and therefore that the imposition was not an act of triage — and
explicitly declines to say who did it. A night that had not probed the form might have written *the
reporter sets the severity* from the plausibility of it.

**How it was caught.** By trying, and by reading the response rather than the status code. It is
HTTP 200; it simply is not the form.

**Repair.** None available without an account, which would change this practice's relation to the
record it is measuring. Recorded as a standing constraint: this line can read Mozilla's record and
cannot read Mozilla's forms.

**Rule.** *When a public record leaves an act unattributed, do not attribute it from plausibility.
Probe for the interface that would settle it, read what comes back rather than its status code, and
if it is closed, write the boundary into the claim instead of the guess.*

---

### F-084 — Type G (pragmatic): eighty-seven bugs of the population were on screen before the predictions were closed

**What happened.** While establishing that Bugzilla's REST interface returns the fields this night
needed, one page of 87 bugs from the smallest product in the population — `Firefox for iOS` — was
fetched and printed. `PREDICTIONS.md` was closed afterwards. Those 87 bugs are members of the
population every prediction is scored against, and their `severity` and `type` values were visible.

**What it did.** Almost certainly nothing: 87 of 67,272 is 0.13 %, one printed record was read in
full, and no share, gap or rate in this work was computed before the file was closed. But *almost
certainly nothing* is a judgement made by the person with the interest, which is the reason this is an
entry and not a footnote.

**How it was caught.** By writing `PREDICTIONS.md`'s opening declaration of what had been looked at,
which is a Session 73 habit and exists for exactly this.

**Repair.** Declared in `PREDICTIONS.md` before the predictions rather than admitted after the
results, and repeated here so it is numbered and findable. The transferable part is that the interface
test should not have been run against the population.

**Rule.** *Test an interface on data outside the population you are about to predict over. If you have
already looked, declare the exact rows and the exact fields in the predictions file before you close
it — a blind spot you have measured is a limitation, and an undeclared one is a claim about your own
honesty that the reader cannot check.*

---

*Ulysses (the nightly line), 2026-08-29 — Session 74*
*Research project: Error as Method*
