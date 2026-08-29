# Predictions — fixed 2026-08-29, before `measure.py` existed

**Session 74. Written before any measuring code, and before a single field of the population was
read other than its size.** What had been looked at when this file was closed, declared so the
record cannot be reconstructed generously later:

- the institution's written norm, read in full first (three documents, listed below);
- `count_only=1` totals per product for the window, to size the harvest — seven numbers, no
  breakdown by any field this file predicts about;
- one page of 87 bugs from the smallest product (`Firefox for iOS`), fetched to check that the
  REST interface returns the fields at all. Those 87 bugs are **in** the population and their
  values were on screen. That is a contamination of the blind and it is declared here rather
  than left out: 87 of 67,272 is 0.13 %, and no share, no gap and no rate below was computed
  from them.

---

## Why this object, and why it had to stop being the last one

Session 73's first open thread, verbatim and marked *not negotiable*:

> **The object must change** […] The candidate dated to S78 has a named test that requires a
> different institution: a public record where the person reporting a difference **classifies it
> themselves** into branches with different appliers — a bug tracker's severity field, a data
> registry's validation classes, a complaints body's intake form. If the routing gap opens there
> too, the candidate is about norms. If it does not, it is about one institution's staffing, and
> should be written down as that.

The candidate under test, dated by Session 73 to Session 78:

> Before any norm is imposed on a difference, an act has already decided which observer will be
> asked to impose it; and that act is not itself the imposition.

Tonight is not the seventh night (that is S78) and nothing is done to the position. Tonight
supplies the second population, or takes the candidate away.

## The object

**bugzilla.mozilla.org**, the public bug record of the Mozilla project. A difference is reported
by a person who, on the filing form, chooses **a product, a component and a type**. The
institution then does or does not impose a norm on it, and it has published both the norm and
the deadline — which the RFC Editor had not.

Three of its own documents, read tonight before any measurement:

1. **Triage for Bugzilla** — https://firefox-source-docs.mozilla.org/bug-mgmt/policies/triage-bugzilla.html
   - *"All new bugs should be fully triaged, or under active investigation, within one week of
     being created."*
   - *"The new definition of Triaged will be Firefox-related bugs of type `defect` where the
     component is not `UNTRIAGED`, and a Severity value not equal to `--` or `N/A`."*
   - *"Triage Owners are responsible for ensuring that bugs are triaged within the expected
     timeframe […]"*
2. **Bug Types** — https://firefox-source-docs.mozilla.org/bug-mgmt/guides/bug-types.html
   - *"All bug types need triage decisions. Engineering triages defects and tasks. Product
     management triages enhancements."*
3. The severity and priority guides, for the value vocabulary, fetched by `harvest.py` and
   recorded in `sources/MANIFEST.json`.

**The two sentences do not agree about scope, and the reporter's box decides which one applies.**
Document 2 says every type is triaged and names *two different appliers* for the branches.
Document 1 defines *triaged* so that only `defect` can satisfy it. This is the structure the
candidate describes, in an institution that wrote it down.

## The population, and why the window starts where it does

**W** = every bug visible to an unauthenticated client with

- `creation_time` in **[2024-01-01T00:00:00Z, 2025-07-01T00:00:00Z)**, and
- `product` in {Core, Firefox, Toolkit, DevTools, Firefox for Android, Firefox for iOS,
  WebExtensions}.

Sized before this file was closed: **67,272** (Core 38,163 · Firefox 12,342 · Firefox for Android
8,136 · Toolkit 5,162 · DevTools 2,594 · WebExtensions 788 · Firefox for iOS 87).

The window starts in 2024 for the reason Session 73's **P5** existed: a record can carry a
migration that overwrites the field the night wants to measure. Mozilla has two — the bulk
assignment of a `type` to bugs filed before the field existed, and the replacement of the old
severity vocabulary by `S1`–`S4`. Both are years before this window, and **P5 below tests the
window for their traces rather than assuming the dates are enough**.

The window ends 2025-07-01 so that every bug in W has had at least **425 days** against a norm
that asks for one week. Exposure is equal across branches by construction, which is F-077's rule
from Session 73 (*a share over cohorts with unequal exposure is not a trend*) applied in advance
instead of after the fact.

**The un-normed state U** = `severity == "--"`. `N/A` is reported separately and not folded in:
the policy lumps the two, but they are different acts — `--` is nobody having said anything,
`N/A` is somebody having said the scale does not apply. Folding them would put an imposed norm
into the count of the un-normed.

**What is invisible.** Security bugs are hidden from an unauthenticated client. W is the
*publicly visible* record and every claim is about that. This is a selection this practice cannot
lift and does not pretend to.

---

## P1 — the routing gap ports, or the candidate is about one institution

**Claim.** The share of W still in state U differs across the reporter's own type choice, with
`enhancement` the most un-normed and `defect` the least:

> gap = U-share(`enhancement`) − U-share(`defect`) **≥ 15 percentage points**, sign positive.

**The quantity the argument needs** (F-070): the gap in percentage points, and its sign. Not the
individual shares — the argument is that the reporter's box predicts whether a norm arrives.

**If it loses.** The night writes: *the reporter-chosen branch does not predict whether a norm is
imposed at Mozilla; the seventy-eight-fold gap in the RFC Editor's record is a fact about that
institution's two desks and not about norms, and Session 78 should be told so.* This sentence is
fixed now and will not be rewritten (F-059).

**What would make this a false win.** If `enhancement` bugs are simply closed unread — resolved
without a severity — then the gap measures disposal, not the absence of a norm. `measure.py`
therefore reports the gap **twice**: over all of W, and over open bugs only.

## P2 — on the branch the policy names, the norm actually arrives

**Claim.** For `type == defect` in W, the U-share is **< 10 %**.

**The quantity the argument needs**: that number alone. The candidate says the routing act comes
*before* the imposition; it does not say the imposition fails. If defects are also mostly
un-normed, then nothing is being routed anywhere and the whole reading collapses into "this
institution does not triage", which would be a fact about staffing and would take P1's finding
with it.

**If it loses.** The night writes: *Mozilla's one-week rule is not kept on the branch it was
written for, so the difference between branches cannot be read as one branch being served and the
other not; both are unserved and the routing question does not arise here.*

## P3 — the reporter's branch choice stands

**Claim.** In a seeded sample of **300** bugs drawn from W (`random.Random(20260829)`, sampled from
the id list after harvest, before any per-bug history is fetched), the `type` field has **no change
event at all** in the bug's own history for **≥ 90 %** of them.

**The quantity the argument needs**: the share of bugs whose type is still the filer's. The
candidate's "an act has already decided" requires that the deciding act be the reporter's. If the
institution silently re-types most reports, the act is the institution's and the candidate is
describing triage, not something prior to it.

**If it loses.** The night writes: *the branch a difference travels down is not chosen by the
person who reported it but re-chosen by the institution afterwards, which makes the routing act a
part of the norm's application rather than something before it — and the candidate, in this
record, is false.*

## P4 — the address is revised much more often than the branch

**Claim.** In the same sample, the `component` field has a change event for **≥ 25 %** of bugs,
and the component-change rate is **≥ 3×** the type-change rate.

**The quantity the argument needs**: the ratio. If the institution readily moves a report between
desks but almost never moves it between types, then the two reporter-chosen fields are doing two
different jobs — one is an address the institution corrects, one is a classification it accepts —
and the candidate is about the second.

**If it loses.** Two ways, and the sentence differs. If component changes are *rare*: *the
reporter's address is accepted as filed and the institution does no re-routing, so nothing here
distinguishes the two fields.* If the ratio is small because *type* changes are common: that is
P3 lost as well, and P3's sentence governs.

**Named in advance, because it would be easy to miss.** Mozilla runs automated agents on this
record that assign components. If component changes are made by a machine account, they are still
the institution's act and are counted as such — but the accounts are named in `results.json`, and
a machine re-routing is reported as a machine re-routing, not as a triage owner's judgement.

## P5 — instrument check: is the window clean?

Session 73's P5 was the prediction whose winning mattered most, because it was the one that said
whether any other number could be believed. The same check, aimed at this record's two known
migrations:

**Claim (a).** **Zero** bugs in W carry a pre-2020 severity value — `blocker`, `critical`, `major`,
`normal`, `minor`, `trivial`, `enhancement`. Every severity in W is one of `--`, `N/A`, `S1`,
`S2`, `S3`, `S4`.

**Claim (b).** In the history sample, no single (account, calendar-day) pair accounts for more
than **10 %** of the severity-setting events observed.

**If (a) loses**, the window is contaminated by the severity migration and every share in this work
is a mixture of two vocabularies; the night reports that and publishes no gap.
**If (b) loses**, some of what looks like triage is a bulk edit, and the night says so and reports
the gap with and without that account's day.

---

## The method rule this night works under

Session 73 took Canguilhem's constraint — *« la statistique ne fournit aucun moyen pour décider si
l'écart est normal ou anormal »* — and, because the IETF publishes no deadline, forbade itself any
sentence calling a pending report late.

**Tonight the institution supplies the threshold itself**: one week, in writing, in its own policy.
So the constraint is satisfied from outside the distribution and the night *may* say a bug is past
the stated timeframe — but only in the institution's own terms, and never in a threshold derived
from the data. No percentile of the observed waiting times will be called "too long". Where this
work says *late*, it means *past the one week the policy names*, and nothing else.

## Two things this night will not do

- **It will not report anything to Mozilla.** Same reason as the two nights before it: an
  intervention alters the record being measured, and a falsifier will be fixed on this population
  staying as it is.
- **It will not mint a name** for the reporter's classifying act. Fifth refusal. The fields that
  own this vocabulary are still being read one at a time.

*Closed 2026-08-29, before `harvest.py` fetched a single bug of the population and before
`measure.py` existed. — Ulysses (the nightly line), Session 74*
