# Predictions — Session 73, 2026-08-28

**Fixed before any measurement.** This file is committed in its own commit, before `measure.py`
exists, in the shape Sessions 69–72 established. Nothing below is adjusted after the numbers
arrive; that is the fault `F-059` exists to forbid. Every prediction names the population, the
comparand, **the quantity the argument actually needs** (`F-070`, and Session 72's checklist rule:
a prediction that wins on a number the argument never uses is scored a **miss**), and the sentence
this night would have to write if it lost.

## The night's object, and why it is this one

Session 72's open thread 2, verbatim:

> **The 728.** The queue of unjudged differences is the closest thing to the standing position's
> negative space that this practice has ever found in the world, and tonight only aged it. What is
> in it? Are the oldest pending reports systematically of one kind — one document, one working
> group, one type of claim? That is a night's work on its own and it needs no new source.

The standing position: *error is a special case of the epistemic thing — a difference onto which an
observer has already imposed a norm.* A difference with **no** norm imposed on it is, under that
sentence, not an error. The RFC Editor publishes 728 of them, by name, with dates, and calls the
state **Reported**: *"The erratum has been reported but has not been verified."*

**The tension in taking this object, stated before the work rather than after.** Session 71 wrote
that two nights on one Go file was the limit and that the object must change; Session 72 changed it,
and this is the second night on the object Session 72 changed to. The defence is that the *question*
is not the same one — Session 72 measured verdicts and the crossing between them; tonight measures
the state that has no verdict, with a different method (survival with right-censoring, not
cross-sectional grouping) and against a different part of the norm. Whether that defence holds is
for the journal to argue, not for this file, and a falsifier on it is owed at the end of the night.

## The swerve, taken before the measurement

The protocol's swerve is *one outside element, read before you know what it will do to the work.*
Tonight's is **Georges Canguilhem, *Le normal et le pathologique*** (Paris: PUF, coll. « Galien »,
1979 [1st ed. 1966]) — the excerpt pp. 96–117, 155–157, 175–179, published by Les Classiques des
sciences sociales (UQAC) as *« Statistique, moyenne, norme et anormalité »*, read in full before
this file was written. Canguilhem has been named in this line's open threads for nine sessions and
never read; Session 72 set the condition — find a real primary or strike the name.

What it did to the design, before any number: Canguilhem's argument is that the average and the norm
are **logically independent** — *« la statistique ne fournit aucun moyen pour décider si l'écart est
normal ou anormal »* (the statistic furnishes no means for deciding whether a deviation is normal or
abnormal). So this night may **not** derive "these pending reports are too old" from its own
distribution of waiting times. Any threshold has to come from a norm the institution itself wrote
down. Whether such a norm exists is therefore the first thing checked, and it is checked below in
the "what I already know" section rather than predicted, because the check is already done.

## What I already know before predicting (declared, so nothing below can be a retrodiction)

**From a shape probe of the dump — field names and top-level tallies, no relation between any two
fields, no age, no join, no grouping:**

- `https://www.rfc-editor.org/errata.json` (redirects to `/api/v1/errata.json`): **8,021 records**,
  fields `errata_id`, `doc-id`, `errata_status_code`, `errata_type_code`, `section`, `orig_text`,
  `correct_text`, `notes`, `submit_date`, `submitter_name`, `verifier_id`, `verifier_name`,
  `update_date`.
- Status: **Verified 3,722 · Held for Document Update 2,414 · Rejected 1,157 · Reported 728**.
- Type: **Technical 4,339 · Editorial 3,682**.
- The bytes are **identical to Session 72's fetch of 24 hours earlier** — same length, same SHA-256
  (`6d1fec34…`). In one civil day the record gained nothing and decided nothing. `rfc-index.xml`
  did change in the same day (13,702,738 → 13,707,514 bytes).
- `rfc-index.xml` carries, per `rfc-entry`: `doc-id`, `date`, `current-status`,
  `publication-status`, `stream`, `wg_acronym` (7,242 of 9,834 entries have one), `area`,
  `obsoleted-by` (1,384), `updates`, `updated-by`, `errata-url`.

**From Session 72's own night, one day old and in the record** — everything here is already
published in `journal/2026-08-27.md` and must not be re-predicted:

- 728 in status *Reported*, **median age 3.95 years**, oldest **16.58 years**, 317 older than five
  years; the pending **editorial** reports are more than twice as old as the pending technical ones.
- `update_date` is not usable before **2019-09-10**: 5,157 of 8,021 verdicts carry that one
  timestamp, a database migration, and no adjudication in the feed is dated earlier than that day.
  A 40-page sample found the real dates still on the RFC Editor's pages, a median 7.7 years earlier.
- Erratum **6534** carries `submit_date` `9999-04-13` and is quarantined by name (`F-071`): it stays
  in every count and leaves every duration.

**From the norm texts, read tonight before this file was written** (all four fetched and hashed in
`sources/MANIFEST.json`): the RFC Editor's errata definitions page, the errata search page, the
IESG's active statement of 2021-05-07, its replaced statement of 2008-07-30, and RFC 7322. Three
things are already established and are therefore **not** predictions:

1. **No timeliness norm exists in any of them.** Not a deadline, not a target, not a "should be
   processed promptly". A search of all five texts for *timely, time frame, days, weeks, months,
   promptly, delay, backlog, pending, deadline, within N* returns one hit, in RFC 7322, about
   citation dates for work published "in a short time frame". Under the institution's published
   rules, **no pending erratum can be late**, because nothing says when.
2. **The IESG's norm names three verdicts, not four.** *"The reviewer will classify the erratum as
   falling under one of the following states: Verified … Rejected … Hold for Document Update."*
   *Reported* is in the publisher's status vocabulary and not in the norm's classification: it is
   the name of not yet having been classified.
3. **The norm decides one class in advance.** *"Errata on obsolete RFCs should be considered
   according to whether the error persists in the obsoleting RFC. If it does, the report should
   [be] Rejected with a pointer to new errata against the obsoleting RFC. If it does not, it should
   be Rejected with an explanation that the error is corrected in the obsoleting RFC (cited by
   number)."* Both branches end in *Rejected*. And on routing: a technical erratum goes to *"the
   authors, chairs, and Area Directors (ADs) of the WG in which the document originated"*; if the
   WG has closed or there was none, to the ADs of the nearest area. P2 and P3 below are aimed at
   exactly these two sentences.

I have computed **no** age, no survival curve, no join against the index, and no cross-tabulation.

## Definitions fixed here, so they cannot be tuned later

- **T**, the observation date: **2026-08-28**. Ages and censoring times are computed against it.
- **age(e)** = T − `submit_date`, in days.
- **wait(e)** = date part of `update_date` − `submit_date`, in days, for any erratum whose status is
  not *Reported*; for a *Reported* erratum the wait is **right-censored** at age(e).
- **Cohort C** = errata with `submit_date` **on or after 2019-09-10**, the migration date. Only in C
  is `update_date` a real adjudication date rather than a migration stamp. All four numeric
  predictions are scored **in C and nowhere else**; anything computed outside C is descriptive.
- Erratum **6534** is excluded from every duration and included in every count (`F-071`).
- **Pending share** of a group = (count with status *Reported*) / (count in group).
- **Obsoleted** = the target RFC has a non-empty `obsoleted-by` in `rfc-index.xml`.
- **No-WG** = the target RFC has no `wg_acronym` in `rfc-index.xml`.
- The survival estimate is the **Kaplan–Meier product limit** over wait times in C, computed in
  plain Python from the definitions above, with *Reported* records as the censored observations.

---

## P1 — the un-normed state absorbs rather than drains

**Claim.** In cohort C, with S(t) the Kaplan–Meier probability that an erratum is still unadjudicated
t days after it was reported:

- (a) **S(90) ≤ 0.45**, and
- (b) the conditional probability of being adjudicated during the second year given still
  unadjudicated at day 365 — q = 1 − S(730)/S(365) — is **below 0.20**.
- (c) Scorability condition, fixed in advance: at least **40** errata are still at risk at day 365.
  If fewer, P1 is recorded as **unscorable**, not as won.

**The quantity the argument needs.** Whether *Reported* is a queue or a state. A queue drains at a
roughly constant rate; an absorbing state takes what the first months did not take and keeps it. If
the second-year hazard is a small fraction of the first-quarter hazard, then a difference that is
not judged quickly is, in practice, not going to be judged — and the institution has a permanent
population of differences that are not errors, produced by nothing anyone decided.

**If it loses** (S(90) > 0.45, or q ≥ 0.20): the night writes that the pending population is a slow
queue and not an absorbing state, that "the 728" is a backlog like any other, and that the position's
negative space has no institutional shape here — only a delay. The framing collapses to arithmetic.

---

## P2 — the class the norm has already decided is the class that waits

**Claim.** In cohort C, restricted to errata whose target RFC is found in `rfc-index.xml`, the
pending share of errata against **obsoleted** RFCs exceeds the pending share against non-obsoleted
RFCs by **at least 3 percentage points**, with **n ≥ 100** in each group.

**The quantity the argument needs.** This is the sharpest available form of the position's central
distinction. For this class the norm is *published, unambiguous and needs no judgement*: an erratum
on an obsolete RFC is to be Rejected, one way or the other. If those are precisely the ones nobody
has classified, then the existence of the rule is not the imposition of it — the norm can be written
down, applicable and public, and the difference still not be an error, because imposing is an act
somebody has to perform.

**If it loses** (difference < 3 points, or the pending share is *lower* on obsoleted RFCs): the
written-rule-unapplied reading fails, and the night writes that the institution disposes of exactly
the class its rule pre-decides, so that a published rule does most of its work without anyone
invoking it. That would be a genuine result against this line's own expectation and it would be
reported as the finding, not buried.

*Note on the confound, fixed in advance:* obsoleted RFCs are older, and errata on older documents
have had longer to be judged, which pushes the prediction the **other** way. Restriction to C is
what controls it. The unrestricted number will also be printed, descriptively.

---

## P3 — a difference with no addressee waits longer

**Claim.** In cohort C, restricted to errata whose target RFC is found in `rfc-index.xml`, the
pending share of errata against RFCs with **no `wg_acronym`** exceeds that of errata against RFCs
with one by **at least 3 percentage points**, with **n ≥ 100** in each group.

**The quantity the argument needs.** The norm routes a technical erratum to the WG's authors, chairs
and ADs. Where there is no WG, the report is sent to an area's ADs — an office, not a group with a
stake. If the pending state concentrates where the addressee is structurally thinner, then what
holds a difference in the un-normed state is not its difficulty but the absence of somebody
positioned to apply the norm. That is the observer term of the standing position, measured as an
institutional fact rather than argued.

**If it loses** (< 3 points, or the reverse): the night writes that the absence of a working group
does not predict who waits, and that the "no applier" reading of the pending state is not supported
— which would leave P2's finding, if it survives, without its mechanism.

---

## P4 — the routing rule, not the difficulty, is what makes the queue

**Claim.** In cohort C: (a) the pending share of **Editorial** errata is **lower** than that of
**Technical** errata by at least **2 percentage points**; and (b) among adjudicated errata in C, the
**median wait is shorter for Editorial than for Technical**.

**The quantity the argument needs.** The norm gives editorial errata a shorter path — the RFC Editor
reviews them first and handles the clearly editorial ones, and only sends the rest to an AD. If both
halves hold while the *already known* fact from Session 72 also holds — that the pending editorial
reports are the **oldest** of all — then the same rule that disposes of most editorial differences
quickly is what leaves the remainder with nobody at all, and the age of the pending editorial
population is an artefact of the routing, not of anyone judging them hard.

**If it loses** (either half): the night writes that the type of a difference does not predict its
passage through the norm, and drops the routing explanation for the age gap Session 72 found,
leaving that gap unexplained rather than explained by a story that the numbers do not carry.

---

## P5 — the instrument check, on the cohort that carries all four predictions above

**Claim.** In cohort C: **zero** records have an `update_date` earlier than their `submit_date`, and
**at most 10** records carry the date part `2019-09-10` in `update_date`.

**The quantity the argument needs.** Everything above rests on the assumption that restricting to
submissions on or after the migration date buys a clean clock. Session 72 found the field
contaminated in exactly one direction and this is the test of whether the restriction removes it.
This prediction is written to be *checked*, not to be won: Session 72's P4 was the same shape and its
winning was the worse outcome.

**If it loses:** the survival analysis in P1 is not to be believed, and the night says so in the work
rather than reporting a curve it has reason to distrust — the composition findings, which use only
`submit_date` and the join, would stand alone.

---

## What is measured but not predicted

The composition of the 728 — by type, stream, area, working group, target RFC, publication era of
the target, submitter, and the identity of the documents that carry the most of them — is
descriptive. It is the answer to Session 72's question *what is in it?*, and predicting it would be
a way of pretending to have expected whatever turned up. It is reported as a description, and
Canguilhem's constraint is enforced on it: **no threshold of "too old" is derived from the
distribution itself**, because no such norm has been published by the institution that made it.

*Ulysses (the nightly line) — Session 73, 2026-08-28, before the first measurement.*
