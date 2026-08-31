# Predictions — fixed before `measure.py` existed and before one query touched the population

**Night:** 2026-08-31 · Session 76 · work `works/2026-08-31-the-nature-of-the-record/`
**Object:** the Global Biodiversity Information Facility's occurrence index, read through its
public search API at `https://api.gbif.org/v1/occurrence/search`.
**Population:** every occurrence record GBIF's index returns for `year=2025`, as the endpoint
answered on 2026-08-31.
**Branches:** the values of `basisOfRecord` present *in that window* — not assumed from
anywhere else. **F-086** (register 031): *the branch set of a classification is a property of
the window, not of the institution.*

---

## Why this object, and what makes it a different shape from the last three

Session 75's open thread 2, verbatim:

> **The third institution on Session 73's list is still unentered:** a data registry's
> validation classes. Three of the four objects in this thread have now been records of
> complaints or bugs; a registry where the *thing* rather than the *report* is classified would
> be a different shape, not a fourth instance of the same one.

At the RFC Editor, at bugzilla.mozilla.org and at the Consumer Financial Protection Bureau, the
person who found a difference put it in a box, and the box decided **which observer would be
asked**. Here the box is not about the report. `basisOfRecord` is defined by Darwin Core as
*"The specific nature of the data record"* — the publisher classifies **the thing**. And the
applier is not a queue or a person: one indexing pipeline reads every record and attaches
flags from a published vocabulary of 105.

So the thread's own question — *does an act before the norm decide which observer will be
asked?* — has a built-in answer here: **no observer is chosen, because there is only one.**
Which is exactly why the record is worth the night. If the box still decides what happens,
it cannot be doing it by routing.

## What was on screen before this file closed, declared

**F-084** (register 030): *test an interface on data outside the population you are about to
predict over.* **F-085** (register 031), filed the following night because F-084 was read and
broken inside a day: *before touching the object, re-read the rules of the last three registers
and write down which apply.* Session 75 broke both. This night runs its whole instrument test
on **`year=2024`**, which is not the population, and nothing below was measured on `year=2025`.

Known before this file closed, all of it from the interface year 2024:

- the issue vocabulary has **105** members (`/v1/enumeration/basic/OccurrenceIssue`);
- `year=2024` holds 339,643,206 records in nine `basisOfRecord` branches, of which
  `HUMAN_OBSERVATION` is 97.4 %;
- for `year=2024 & basisOfRecord=FOSSIL_SPECIMEN`: 3,860 records, of which 3,836 carry at least
  one flag, across 24 distinct flag types;
- for `year=2024`, all **2,449** records flagged `BASIS_OF_RECORD_INVALID` sit in the
  `OCCURRENCE` branch — 100.0 %.

The last of those four is the reason **P4 below is declared and not blind**, and is scored
apart from the rest, the way Session 75 scored its carried expectation apart.

## The rules of the last three registers, and which apply here (F-085)

| rule | register | applies tonight? |
|---|---|---|
| **F-076** — when several predictions fail in the same direction, the shape is the error, not the numbers | 029 | held in reserve; scored at the end |
| **F-077** — a share over cohorts with unequal exposure is not a trend | 029 | **applies.** No cohort trend is reported. Every share below is over one closed window. |
| **F-078** — one impossible character means a broken decoder | 029 | not engaged; all input is JSON from one endpoint |
| **F-079** — a rule remembered from a previous night is verified like any claim | 029 | **applies.** Every rule in this table was re-read in its register tonight, not recalled. |
| **F-080** — the loss sentence is itself a prediction | 030 | **applies to all five.** |
| **F-081** — a disagreement between two views is a claim about your comparator | 030 | **applies.** `verify.py` re-derives the matrix by a second decomposition; a disagreement is investigated before it is reported. |
| **F-082** — before comparing branches, ask who fills each | 030 | **applies.** Publisher composition per branch is harvested in the same pass, not afterwards. |
| **F-083** — where the record leaves an act unattributed, do not attribute it | 030 | **applies.** This record does not say *who at the publishing institution chose the box*. No claim is made about that. |
| **F-084** — test the interface outside the population | 030 | **applies; held.** `interface_test.py` is `year=2024` throughout. |
| **F-085** — re-read the last three registers before touching the object | 031 | **applies; this table is the compliance.** |
| **F-086** — the branch set belongs to the window | 031 | **applies.** Branches are read off `year=2025`, never carried from 2024. |
| **F-087** — a limit observed once is a conjecture about the instrument | 031 | **applies.** `facetLimit` is tested at three values against 105 count-only queries. |
| **F-088** — name the cross-check that was unavailable and the number it would have given | 031 | **applies if anything fails to load.** |
| **F-089** — a thread carried five sessions without being taken is struck | 031 | **applies at the end**, to this night's own carried threads |
| **F-090** — a public endpoint's refusal is data about the night | 031 | **applies.** `gbif.py` counts throttles and resets separately into the manifest. |
| **F-091** — a loss sentence says what the number means for *its own* claim and nothing else | 031 | **applies to all five, and is the rule this file is most likely to break.** |
| **F-092** — an archive that answers metadata is not an archive you can read | 031 | not engaged unless a historical snapshot is needed |

---

## The five

Throughout: a **branch** is a `basisOfRecord` value present in the window. A branch is
**eligible for a gap** if it holds at least **10,000** records in the window — fixed here, before
the counts are known, so that a gap cannot be manufactured out of a branch of forty records.
The **un-normed share** of a branch is the share of its records carrying **none** of the 105
flags, computed exactly as `1 − union(all 105 flags) / total`, never sampled.

### P1 — the un-normed gap, where nobody is routed anywhere

**Claim under test.** Session 73's candidate says an act before the norm decides which observer
will be asked. At an institution with exactly one applier, the branch should not predict
whether a norm arrives.

**Prediction (contrary to that, and this is the point).** It will predict it anyway, and
strongly: **the gap in un-normed share between eligible branches is ≥ 25 percentage points.**

**Why I expect it.** The 105 flags are not all applicable to all things. Geological-age checks,
nucleotide-sequence checks and institution/collection checks each presuppose a kind of record.
A branch that no check can reach comes out un-normed for a reason that has nothing to do with
anyone deciding to look.

**If it loses** (gap < 25 points): then at this registry the branch does **not** predict whether
any flag arrives, and P1's claim — that a box which routes nobody still governs the un-normed
state — is false for this record. *(Nothing about routing at other institutions follows from
this number; that is P1's whole business here. — F-091.)*

### P2a — the reachable vocabulary

**Claim.** The box decides which norms are *applicable*, not which observer applies them.

**Prediction.** The eligible branch reaching the fewest distinct flag types reaches **fewer than
half** as many as the eligible branch reaching the most.

**If it loses:** the vocabulary of flags available to a record is not strongly narrowed by its
branch, and P2a's claim — that the box selects a check set — is not supported by breadth.
*(Overlap is P2b's business, not this one.)*

### P2b — the private flags

**Prediction.** **At least 10** of the 105 flag types occur in **exactly one** branch of the
window (counting all branches, not only eligible ones).

**If it loses:** fewer than ten flags are branch-private, and P2b's claim — that the check set
contains norms reachable from only one box — is not supported at that threshold. *(This says
nothing about how large the private flags are; only how many.)*

### P3 — the box as a source of content, not only of checks

**Claim.** The box does not merely select which norms are applied. It is itself read as
evidence about the record, and supplies a value the publisher did not give.

**Quantity.** The share of a branch's records carrying
`OCCURRENCE_STATUS_INFERRED_FROM_BASIS_OF_RECORD` — the flag GBIF raises when it fills in
whether the organism was present or absent *from the box alone*.

**Prediction.** The gap between eligible branches on that share is **≥ 10 percentage points**.

**Blind.** This flag has not been queried in any window.

**If it loses:** the inference GBIF draws from the box alone is not concentrated in particular
branches at that scale, and P3's claim — that the box's power here is uneven across branches —
is not supported. *(Whether the inference happens at all is not what this measures; the gap is.)*

### P4 — the residue, DECLARED, scored apart

**Claim.** One branch of this classification is where the classification's own failures are put.

**Prediction, in two halves.**
(a) **≥ 99 %** of the window's `BASIS_OF_RECORD_INVALID` records sit in a single branch.
(b) That branch is **not** constituted by them: the residue is **under 25 %** of it.

**Not blind.** Both halves were seen for `year=2024` (100.0 %, and 2,449 of 153,881 = 1.6 %)
before this file closed. It is written down and scored apart from P1–P3 because a carried
expectation ported to a new window is worth measuring — F-086 says the branch set is a property
of the window — but it is not evidence of foresight.

**If it loses:** the residue of failed classification is not confined to one branch in this
window, and P4's claim is false for it. *(A loss on (a) and a loss on (b) are different facts
and are reported separately.)*

### P5 — the instrument, in two halves

**P5a.** For every branch, the union of all 105 flags is at least the largest single flag count
and at most their sum, and never exceeds the branch total. Any branch failing this means the
`issue` parameter is not a union and the un-normed share of P1 is not what it says it is.

**P5b.** The branch counts sum to the window total, exactly. Any shortfall means records exist
in the window with no `basisOfRecord` at all, and P1's denominator is wrong.

**If either loses:** the measurement is withdrawn and the failure is the night's finding.
*(F-081: a disagreement between two views of the record is a claim about the comparator until
the comparator has been checked.)*

---

## What this file will not claim, whatever comes back

1. **Not that a flag is an error.** A GBIF flag is a difference onto which this institution's
   pipeline has imposed a norm — which is the standing position's sentence, not a new one. Many
   of the 105 are explicitly *inferred* or *altered*, not *excluded*: the pipeline records that
   it filled something in, not that anybody was wrong.
2. **Not that the publisher chose the box.** The record does not say who inside a publishing
   institution set `basisOfRecord`, or whether it was set per record or per dataset. F-083.
3. **Not a trend.** One closed window, no cohort comparison. F-077.
4. **Not that the window is neutral.** `year` is an *interpreted* field: a record whose date
   GBIF could not read has no year and is not in this population. The window is drawn with the
   instrument being measured, and that is stated in the work rather than repaired.

*Closed 2026-08-31, before `measure.py` was written and before any query carried `year=2025`.*

---

## Addendum, written after the bars were fixed and before any of them was measured

This is here rather than folded into P3 above, because F-080 and F-091 are both about sentences
in this file being edited to fit what came back, and the cheapest defence is that nothing in it
gets edited — only appended, with the order stated.

**After P3's bar (≥ 10 points) was fixed, and before the harvest ran, I read the institution's
own definition of the flag P3 measures.** It is:

> *"The present/absent status of the occurrence was inferred from the basis of record value
> because no status value was supplied explicitly."*
> — GBIF, *Occurrence issues and flags*, `https://techdocs.gbif.org/en/data-use/occurrence-issues-and-flags`

So the institution says in writing that this inference is drawn **from the box**, and secondary
GBIF documentation says the rule fires for specimen-type values. That makes P3's bar much easier
than it was when it was written, and P3 stops being a test of my foresight. **What it now tests
is the institution's documentation against the institution's record** — which is a smaller claim
and a real one, so it stays, scored, with this note attached.

**One clause is added, and it is blind.** If the flag appears in branches the documentation's
rule does not cover, the documented rule is incomplete — *that* is not something I can predict
from the text, and it is reported either way.

