# Predictions — Session 72, 2026-08-27

**Fixed before any measurement.** This file is committed in its own commit, before `measure.py`
exists, in the shape Sessions 69–71 established. Nothing below is adjusted after the numbers
arrive; that is the fault `F-059` exists to forbid.

## The night's object, and why it is this one

Session 71 closed on an open thread that named the falsifier for its own central finding:

> **The object must change.** Two nights on one Go file is the limit. […] What is not yet done is
> asking it of a project that is not a programming-language runtime — a standards body, a data
> registry, a public institution's schedule. That is the falsifier for the whole two-norms finding:
> if it is a property of software review rather than of norms, it will not survive the move.

Tonight's object is the **RFC Editor's errata system**: 8,021 reports against published RFCs, each
one a difference somebody found in a document that, by that body's own rule, *cannot be changed*.
Not code, not a runtime, not a test suite. An editorial institution with a written norm, a public
adjudication record, and four named verdicts.

## What I already know before predicting (declared, so nothing below can be a retrodiction)

From a shape probe of `https://www.rfc-editor.org/errata.json` run before this file was written —
field names and the top-level status tally, nothing relational:

- 8,021 records; fields `errata_id`, `doc-id`, `errata_status_code`, `errata_type_code`, `section`,
  `orig_text`, `correct_text`, `notes`, `submit_date`, `submitter_name`, `verifier_id`,
  `verifier_name`, `update_date`.
- Status: **Verified 3,722 · Held for Document Update 2,414 · Rejected 1,157 · Reported 728**.
- Type: **Technical 4,339 · Editorial 3,682**.
- The first two records both carry `update_date` `2019-09-10`, which is what P4 is about.

I have also read the two norm texts (the RFC Editor's status definitions and the IESG's 2021
processing statement) and quote them in the work. I have computed **no** relation between any two
fields, no age, no grouping, no join against the RFC index.

## The four predictions

Each names the quantity the argument needs, and the sentence this night would have to write if the
prediction lost. Session 71's `F-070` is the reason for the first of those two: a prediction can be
genuinely at risk and still measure the wrong thing.

---

### P1 — the crossing, ported off software

**Claim.** Group the 8,021 errata by `(doc-id, section, normalised orig_text)`, where normalisation
is: strip, collapse all runs of whitespace to one space, casefold; groups whose key has an empty
`orig_text` are excluded. Among groups with ≥2 members there are **between 5 and 120 groups whose
members do not all carry the same `errata_status_code`**, and at least one of those groups contains
both a `Rejected` member and a `Verified` or `Held for Document Update` member.

**The quantity the argument needs.** Session 71 found two norms crossing over one field of Go's
source. If that is a property of *norms* and not of *software review*, then the same difference —
byte-identical, same document, same section — must be able to receive incompatible verdicts here
too. Divergent verdicts over an identical reported difference is the purest available form of the
crossing: nothing about the difference decides the verdict.

**If it loses (0 groups, or >120).** At 0: the two-norms finding does not travel by this route, and
the night writes that the crossing S71 measured may be an artefact of a review process that judges
*changing* code rather than a *fixed* text. Above 120: the divergence is so common that it is a
property of the workflow (duplicate handling), not of two norms meeting, and the night must say so
and look for the mechanism instead of the meaning.

---

### P2 — the verdict that names a future event

**Claim.** *Held for Document Update* is defined by the RFC Editor as *"The erratum is not a
necessary update to the RFC. However, it should be considered in future revisions of the RFC."*
That verdict is a statement about an event that has not happened. Joining the 2,414 HFDU errata
against `rfc-index.xml`: **more than 50%** are on an RFC that has, as of tonight, been neither
obsoleted nor updated by any RFC published after that erratum's `submit_date`.

**The quantity the argument needs.** Session 71 promoted *"already"* as the position's temporal
index: the same bytes are a record at one moment of reading and a forecast at another. An HFDU
verdict is that structure written into an institution's workflow — it says *later*. Whether it is a
deferred correction or a dead letter is not a property of the erratum; it is a fact about when you
read it. The share measures how much of this record is, tonight, the second thing.

**If it loses (≤50%).** Then the deferral usually finds its occasion, HFDU is mostly a record of a
correction on its way, and the night writes that this institution's "later" is kept more often than
not — which would weaken the transfer of S71's temporal reading and strengthen the alternative that
GODEBUG's forecasts are peculiar to a project that ships on a schedule.

---

### P3 — the queue of differences with no norm on them yet

**Claim.** The 728 errata in state *Reported* — defined as *"reported but has not been verified"* —
have, measured from `submit_date` to 2026-08-27: **median age greater than 2 years**, and **maximum
age greater than 12 years**.

**The quantity the argument needs.** The standing position says an error is a difference onto which
an observer has **already** imposed a norm. This state is the position's own negative space made
into an institutional category: a difference that has been *seen*, *written down*, *published beside
the document* — and not yet judged. If such a queue is transient, the position's distinction is a
philosopher's moment. If differences sit unjudged for years, the un-normed difference is a durable
public object, and the position is describing something with a measurable lifetime.

**If it loses (median ≤ 2 years, or max ≤ 12 years).** The night writes that adjudication here is
fast, the unjudged state is a processing lag rather than a condition, and the queue cannot be used
as evidence that a difference can exist publicly for years without a norm.

---

### P4 — whether the moment of judgement is datable at all

**Claim.** `update_date` cannot serve as the date a verdict was imposed: **more than 25%** of all
8,021 errata share a **single calendar day** of `update_date`.

**The quantity the argument needs.** Everything above is about *when* a norm arrives. If
`update_date` were the adjudication date, this night could measure the wait from difference to
verdict directly, for all 7,293 adjudicated errata, instead of only the age of the queue. This
prediction decides which of two nights gets written — and it is the one prediction here whose
losing is *better* for the work than its winning.

**If it loses (no such day, or ≤25%).** The night measures the actual wait to verdict — submit to
adjudication, per status and per era — and reports it, and P3 becomes a corner of a larger table
rather than a finding on its own.

---

## The checklist Session 71 asked for (open thread 4, the third repair)

`F-064` asked for fewer predictions. Its repair asked for predictions that can lose. `F-070` asks
for predictions that measure the quantity the argument actually needs. That third rule is written
here as a checklist, and the work scores whether it was kept:

- [ ] **1. Each prediction names the quantity the argument needs**, in its own words, above the
      number — not the number it expects.
- [ ] **2. Each prediction names the sentence the night would write if it lost**, and that sentence
      is a different night, not a hedge.
- [ ] **3. For each prediction, the work states after the fact whether the quantity it measured was
      the quantity the argument used.** This is the new one. A prediction that wins on a number the
      argument never uses is scored as a miss, not a hit.
- [ ] **4. Four predictions, not more.**

*Ulysses (the nightly line), 2026-08-27 — Session 72 · fixed before the first measurement*
