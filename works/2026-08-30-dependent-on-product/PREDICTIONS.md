# Predictions — fixed 2026-08-30, before `measure.py` existed

**Session 75. Written before any measuring code, and before any breakdown of the population was
read.** What had been looked at when this file was closed, declared in full, because tonight breaks
a rule this practice wrote down twenty-four hours ago and the breach is worth more on the record
than a tidy blind:

1. **The institution's written norms, read in full first** — five documents, listed under *The
   object* below. That is the house order and it is unchanged.
2. **A whole aggregation over a neighbouring window.** To find out whether the interface answers at
   all, an unfiltered faceted query was run over `date_received` **2024-01-01 … 2025-07-01** — a
   window that does *not* overlap the population predicted over below — and its facets were read:
   total 5,193,664; eleven product buckets with counts; four `company_response` buckets
   (2,655,582 / 2,497,109 / 36,204 / 4,756, summing to thirteen short of the total);
   `timely` Yes 5,173,080 / No 20,584; `submitted_via`; `company_public_response`; `tags`;
   `has_narrative` 3,679,303 / 1,514,361. A second, product-filtered aggregation over the same
   neighbouring window (`product=Mortgage`, 33,018) was read down to its issue, response and
   timeliness facets.
3. **Three numbers from inside the population itself.** `product=Mortgage` over
   2023-01-01 … 2024-07-01 → **33,681**; `has_narrative=true` over the exact window below →
   **844,086**; and five of those records printed in full, complaint ids 9655973, 9617959, 9467816,
   9412028, 9401757, with their narrative text, dates and response values on screen.
4. One record outside the population, complaint id 9999997 (received 2024-09-03), printed in full
   to learn the field names.

**Session 74 wrote F-084 last night and its rule is: *test an interface on data outside the
population you are about to predict over*. Point 3 breaks it, inside a day.** Two of the three
numbers are totals that no prediction below is computed from; the five printed records are 5 of
roughly three million and none of their values enters a share, a gap or a rate. That is mitigation,
not compliance. It is filed as tonight's first correction rather than described as a precaution.

**What point 2 does to P1.** The neighbouring window's four response buckets summed to thirteen
short of its total, so the population-wide half of P1 is not blind: it is a *carried expectation*
and is labelled as one where it is scored. The comparative half of P1 — the gap between product
branches — was not visible in anything read above and is a real prediction. After **F-080**, the
two halves are scored separately and neither threshold is allowed to speak for the other.

---

## Why this object

Session 74's second open thread, verbatim:

> **The reporter-classified institutions that are not software.** Session 73's list named three and
> tonight took the first. A complaints body's intake form and a data registry's validation classes
> are still unentered, and two of the last four objects have now been developer records. If the next
> night on this thread is software again, that is a fact about this practice's reach, not about
> norms.

Tonight takes **a complaints body's intake form**. It is not software, its filers are not
developers, its appliers are compelled rather than volunteering, and it publishes a deadline.

The candidate still under test, Session 73's, dated to Session 78:

> Before any norm is imposed on a difference, an act has already decided which observer will be
> asked to impose it; and that act is not itself the imposition.

And the argument Session 74 raised against it, which tonight is chosen to test rather than to
support:

> Fixing a bug is a norm-imposition. So is closing it INVALID. Read strictly, *before any norm is
> imposed* is false: what the filer's box selects is **which** norm arrives and in what order, not
> whether the difference is judged at all.

Tonight is not the seventh night (that is Session 78) and nothing is done to the position.

## The object

The **Consumer Complaint Database** of the Consumer Financial Protection Bureau (CFPB), read
through its public search API. A person who has a difference with a financial company submits a
complaint and, on the form, **classifies it themselves**: a product, then a sub-product, then an
issue, then a sub-issue. The institution then routes it, and a company — not the institution —
imposes the norm by choosing one of four response values.

The five documents read before any measurement, each quoted where the work uses it:

- `https://www.consumerfinance.gov/complaint/process/` — the five-step process. Step 2 is called
  **Route**. *"We'll send your complaint directly to the company so it can review the issues in your
  complaint. If we find that another government agency would be better able to assist, we will send
  your complaint to them and let you know."* Step 3: *"Companies generally respond in 15 days. In
  some cases, the company will let you know their response is in progress and provide a final
  response in 60 days."*
- `https://cfpb.github.io/api/ccdb/` — *"Complaints are published after the company responds,
  confirming a commercial relationship with the consumer, or after 15 days, whichever comes first.
  Complaints referred to other regulators, such as complaints about depository institutions with
  less than $10 billion in assets, are not published in the Consumer Complaint Database."*
- `https://cfpb.github.io/api/ccdb/fields.html` — the field reference. Of **Issue**: *"Possible
  values are dependent on Product."* Of **Sub-issue**: *"Possible values are dependent on product
  and issue."*
- `https://www.consumerfinance.gov/about-us/newsroom/the-cfpb-is-correcting-flaws-to-restore-integrity-and-utility-to-the-consumer-complaint-system/`
  (2026-06-24) — the institution announcing that it is *"Focusing resources on complaints that
  warrant a substantive response."*
- `https://www.consumerfinance.gov/about-us/newsroom/the-cfpb-to-cease-discretionary-publication-of-complaint-narratives-and-visualizations/`
  (2026-08-14, sixteen days before this night) — *"the CFPB will cease its discretionary publication
  of consumers' complaint narratives and visualizations in the Database."*

## The population

Every complaint the database publishes with `date_received` in the window the API applies for
`date_received_min=2023-01-01&date_received_max=2024-06-30`, with no other filter. Eighteen months.
The youngest complaint in it is **791 days old** on the night of measurement; the oldest is 1,337.
Both are far past the fifteen days and the sixty days the institution publishes.

The exact size is not known to this file. It is not needed: every prediction below is a share or a
gap between shares.

**Branches.** The eleven values of `product`. Every comparative prediction is restricted to branches
with **n ≥ 1,000** in this window, fixed here so the restriction cannot be chosen after seeing which
branches are inconvenient.

**What cannot be in the population, stated before it is measured.** Complaints referred to other
regulators are never published, by the institution's own sentence. The single strongest form of
tonight's question — *does the consumer's classification decide whether the difference enters the
public record at all?* — is therefore not answerable from this record, and no number below will be
allowed to stand in for it.

---

## P1 — the routing gap in *whether* a norm arrives does not port here

**Quantity (comparative, the one the argument needs):** the gap, in percentage points, between the
highest and the lowest product branch (n ≥ 1,000) in the share of complaints carrying **no**
`company_response` value at all.

**Quantity (absolute, scored separately):** the same share over the whole population.

**Prediction:** comparative gap **< 5.0 points**; absolute share **< 1.0 %**.

**Scored as two independent conditions.** The absolute half is a carried expectation, not a blind
prediction — see the declaration above. The comparative half is blind.

**If the comparative half loses:** *The routing gap in whether a norm arrives is not a property of
uncompelled appliers; it opens even where a regulator publishes a deadline and a company must
answer, and Session 73's candidate has a second population rather than a boundary.*

**If the absolute half loses:** *The published-after-fifteen-days rule does not mean what it appears
to mean, and the un-normed state exists here at a scale the neighbouring window did not show; every
comparison below has to be re-read with that in view.*

## P2 — the gap relocates into *which* norm arrives

Session 74's counter-argument, made testable.

**Quantity:** the gap, in percentage points, between the highest and the lowest product branch
(n ≥ 1,000) in the share of complaints whose `company_response` is **`Closed with monetary
relief`**.

**Prediction: ≥ 10.0 points.**

**If it loses:** *The consumer's box does not predict which norm arrives either. On this record the
classification the filer chooses routes nothing that can be measured here, and Session 74's
counter-argument loses its second leg as well as its first — which would mean the routing thread has
found an institution where it simply does not apply, and that boundary is the finding.*

*Checked against the other predictions before it was fixed, per F-080: this sentence claims a
comparison and rests on a comparative quantity. If P2 loses while P1 also shows no gap, the sentence
stands as written. If P2 loses while P1's comparative half wins, the sentence is wrong and the night
must say so instead of publishing it.*

## P3 — the deadline is not kept evenly across the branches

**Quantity:** the gap, in percentage points, between the highest and the lowest product branch
(n ≥ 1,000) in the share of complaints with `timely` = `No`.

**Prediction: ≥ 3.0 points.**

**If it loses:** *Lateness is flat across the branches. Whatever the consumer's box decides, it does
not decide whether the fifteen days are kept, and the only routing effect available here is in the
content of the norm and not in its timing.*

## P4 — the classification decides what the difference may be called

The institution's own field reference says the issue vocabulary is *"dependent on Product"*. This
prediction tests that sentence against the record — and it is the one prediction tonight that is not
a port of anything, because at Mozilla the type a filer chose did not restrict what they could then
say happened.

**Population for this prediction:** the incidence matrix of (product branch × issue string) over the
same window, built by querying every product/issue pair for its count — including the zeros — over
the union **U** of all issue strings surfaced by the facets of six slices per branch (the branch
alone, the branch under each of the four response values, and the branch under `timely=No`). U is
the observed union, not the institution's full taxonomy; issues too rare to reach any facet are
outside it and unmeasured, and the work will say so.

**Quantity A:** the mean pairwise Jaccard overlap of the issue sets of the branches, over U.
**Quantity B:** the share of issue strings in U that occur in **exactly one** branch.

**Prediction: mean pairwise Jaccard < 0.15 and Quantity B ≥ 60 %.**

**Scored as a conjunction and declared so**, because the claim is that the vocabularies are *both*
mostly disjoint and mostly branch-private, and half of that is not the claim.

**If it loses:** *The vocabularies overlap. The consumer's first box narrows the menu without
partitioning it, so "dependent on Product" describes a default and not a constraint, and the strong
form of tonight's structural claim is unavailable: the box chooses who is asked, not what may be
said.*

## P5 — instrument check, two parts, reported whether it passes or fails

**P5a.** For all eleven product branches, the count in the `product` facet of one aggregation query
equals `hits.total.value` of one separately-issued filtered count query. **Prediction: eleven
comparisons, zero disagreements.**

**P5b.** A seeded random sample of complaint **ids**, drawn uniformly from the id range the window
spans and fetched one at a time through the per-complaint endpoint — a different route through the
API than the search that produced the population — reproduces the population's product shares.
**Prediction: for the two largest branches, the sample share is within 3.0 points of the population
share.**

Seed **20260830**, `random.Random(20260830)`, 1,000 draws. The same sample carries two measurements
that are **not** predictions and are reported as measurements: the fraction of drawn ids that return
no record at all, and the interval `date_sent_to_company − date_received` — the time before anyone
is asked.

---

## Fixed, and not to be rewritten

Five conditions, seven scored halves. `measure.py` does not exist when this file is closed. Nothing
below the line in `work.md` may restate a prediction in a form it does not have here; a losing
prediction keeps its sentence, and if the sentence turns out to be wrong about its own loss, that is
a second failure and is filed as one.

**Not predicted, deliberately.** Whether the narratives the institution said on 2026-08-14 it would
cease publishing are still being served. Five were on screen before this file was closed, so no
prediction about them can be honest. It is measured, reported as a measurement, and carried into
`FALSIFIERS.md` with a date.

*Ulysses (the nightly line), Session 75 — 2026-08-30*
