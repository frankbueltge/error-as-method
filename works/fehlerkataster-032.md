# Error Register 032 — Session 76 (2026-08-31)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## What is in this file

Six entries, all against tonight. The **Rule** line introduced by Session 72 is kept on each.

Two of them are worth naming before the list, because they are about this register rather than
about GBIF.

**The pre-written loss sentence failed for the third night running, in a third way.** F-080
(Session 74) caught a loss sentence that drew a conclusion another prediction was responsible for.
F-091 (Session 75) caught the rule written to prevent that being applied to one prediction in four.
Tonight the rule was applied to **all five** — and one loss sentence still failed, because it
described the wrong *quantity*: it spoke about concentration where its own bar measured magnitude.
**A rule can be fully held and still not prevent the failure it was written for, if the failure
changes shape.** That is F-095, and it is the most useful thing this register acquired tonight.

**F-081 fired for the first time.** Its rule — *a disagreement between two views of the same record
is a claim about your comparator until the comparator has been checked* — has been available for
two sessions and had never been needed. Tonight the verification disagreed with the harvest on
every branch, the comparator was checked on the interface year rather than assumed, and the
disagreement turned out to be **a hole in the record and not a fault in the comparator**. The rule
worked exactly as written. F-097.

**The scoring Session 78 owes gets its fourth night of data points**, recorded now rather than
reconstructed then:

- **F-084's rule** (*test an interface on data outside the population you are about to predict
  over*) — **held.** Every query of `interface_test.py` is `year=2024`; the population is
  `year=2025`; `interface-test.json` is committed so the separation can be checked rather than
  taken on trust.
- **F-085's rule** (*before touching the object, re-read the last three registers' rules and write
  in the predictions file which apply and how*) — **held.** `PREDICTIONS.md` carries the table, all
  seventeen rules of registers 029–031, each marked applies / applies-and-held / not engaged. It
  cost about twenty minutes and it caught two things before they were errors.
- **F-086's rule** (*the branch set of a classification is a property of the window*) — **held.**
  The nine branches are read off `year=2025` by facet; the interface year's branch set is never
  carried across, and the residue's share of its branch turned out to differ between the two
  windows by a factor of six, which is exactly what the rule exists to stop being reported as a
  trend.
- **F-087's rule** (*a limit observed once under one filter is a conjecture about the instrument*)
  — **applied to the facet and broken on the second instrument of the same night.** `facetLimit` was
  tested at three values against 105 count-only queries; the regular expression that read flag names
  off the reference page was not tested against the flag names at all, and could not match the one
  name in the vocabulary that contains a digit. **F-093.**
- **F-090's rule** (*a public endpoint's refusal is data about the night*) — **held and refined.**
  Zero throttles across all five passes; the route dropped the connection 73 times. The client
  counts the two separately, because a reset is a fact about the path and a 429 is a fact about the
  endpoint, and reporting one as the other would have made GBIF look like it was defending itself
  when it never once said stop. **F-098.**
- **F-091's rule** (*a loss sentence says what the measured quantity means for the claim that
  prediction tests, and nothing else*) — **held, and insufficient.** F-095.
- **F-088's rule** (*name the cross-check that was unavailable and the number it would have given*)
  — **applied.** F-094.
- **F-059's rule** (*a lost prediction is not rewritten*) — **held.** P2b lost by one and P3 lost by
  a factor of forty; both bars, both loss sentences and both quantities stand verbatim in
  `PREDICTIONS.md`, and P3's wrong loss sentence is quoted in the work rather than replaced.

---

### F-093 — Type C (unreliable instrument) and D: a character class that could not match a digit, and the flag it deleted from the record

**What happened.** Section 5 of tonight's work crosses the 105 flags the API will apply against the
flags the institution's own reference page describes. One of the two rules for "described on the
page" counts a flag as described if the page links an example search for it, `?issue=NAME`. It was
written as `re.findall(r"issue=([A-Z_]+)", page)`.

`[A-Z_]` does not match a digit. The page carries
`…/occurrence/search?issue=GEODETIC_DATUM_ASSUMED_WGS84`; the pattern read it as
`GEODETIC_DATUM_ASSUMED_WGS`, which is not in the enumeration, so the flag came back **undescribed**
— and that flag fires on **5,428,125** records in this window, 6.28 % of it, and is one of only five
that occur in every one of the nine branches. The published table carries its row, its label
*"Geodetic datum assumed WGS84"*, its description *"If the datum is null, data interpretation
assumes the record coordinates are in WGS84"*, and its example link. Nothing was missing except in
the instrument.

**How it was caught.** By distrusting the result, not by re-reading the code. *A flag applied to
five million records with no published description* would have been the night's headline, and a
headline that arrives for free is a reason to check the instrument that produced it. Searching the
page's plain text for the flag's name found it in one step.

**What was done.** The count is now produced by **two independent rules** — the name, or the name
spelled out in words, appearing anywhere in the page's text; and the corrected example-link rule
with `[A-Z0-9_]+` — and they **agree exactly**: 80 described, 25 not. Both rules, both results and
the broken pattern are recorded in `documentation.json`, so the correction is checkable rather than
merely asserted. A second instance of the same class of failure was found in the same pass and is
also corrected in place: the keyword rule in `operations.py` spells *assumed*, GBIF wrote *assumes*,
and the same five-million-record flag fell out of the self-reporting set for that reason. Both the
rule as first stated and the amended one are reported, with the 0.57-point difference between them.

**Why it is not a small thing.** The rule that failed here is F-087's, filed the night before last
and quoted approvingly in tonight's own `PREDICTIONS.md` table two hours before it was broken — *a
limit observed once under one filter is a conjecture about the instrument.* It was applied where
the register's example pointed, to `facetLimit`, an obvious instrument parameter with a number in
it, and not to the second instrument in the same night, which was a regular expression over
somebody else's HTML. And the pattern mangles exactly one name in the whole
vocabulary — `WGS84` is the only flag name containing a digit — which is why it produced a single,
large, plausible-looking wrong result instead of an obvious mess. This is F-085's pattern one
register later: a rule applied where its own example points.

**Rule.** A pattern that extracts identifiers is an instrument and is tested against the identifier
set it must cover, not against the two examples that suggested it. Before a count of *what a
document does not contain* enters an argument, produce it by two rules that do not share a
mechanism, and check the loudest member of the count by hand.

---

### F-094 — Type B (inaccessible primary) and G: the classification this night wanted is published, but not in a form that can be joined

**What happened.** GBIF's data blog distinguishes three kinds of remark — *Excluded* ("the original
data couldn't be interpreted, so is excluded in the interpreted fields"), *Altered* ("the original
data is modified in the interpretation process"), *Inferred* ("Using other record information the
data indexed is inferred, if the original is empty"). Only the first is a verdict about what a
publisher supplied. That distinction is the exact instrument tonight's section 6 needs, and it is
displayed **per record on the website**, not per flag in any machine-readable place this night
could find. Neither the enumeration endpoint nor the technical reference page carries it.

**The cross-check that was unavailable, and the number it would have given.** With the per-flag
mapping, section 6 would state: *of the 86,396,340 records in this window, N carry at least one
flag that GBIF itself classifies as Altered or Inferred and no flag it classifies as Excluded* —
i.e. records whose whole normed status is the interpreter's account of its own work. That number is
not in this work and no estimate of it is offered.

**What was done instead, and how it is labelled.** A keyword rule stated before it was applied, run
over the institution's own description text: *a flag is self-reporting if its description says the
interpretation derived, inferred, assumed, rounded, reprojected, collapsed or modified a value.*
The rule, the selected flags and their full quoted descriptions are in `operations.json`, and every
use of the resulting number in the work is marked **this night's reading of GBIF's wording, not
GBIF's classification of its own flags.**

**What was refused.** Assigning all 105 flags to the three classes by hand. It would have taken
twenty minutes and would have produced a table visually indistinguishable from a sourced one. The
protocol's first prohibition covers exactly that.

**Rule.** When the classification an argument needs exists but is published only in a form that
cannot be joined to the data, say which join is missing and what number it would have produced,
then either measure a stated proxy under a stated rule or drop the claim. Do not reconstruct the
institution's classification and present it in the institution's voice.

---

### F-095 — Type A (wrong inference): the loss sentence held its own rule and still described the wrong quantity

**What happened.** P3 measured the share of each branch's records carrying
`OCCURRENCE_STATUS_INFERRED_FROM_BASIS_OF_RECORD` — the flag GBIF raises when it reads a record's
present/absent status out of the box the publisher ticked — and fixed the bar as *a gap of at least
10 percentage points between eligible branches*. The loss sentence, written before the harvest, was:

> *"the inference GBIF draws from the box alone is not concentrated in particular branches at that
> scale, and P3's claim — that the box's power here is uneven across branches — is not supported."*

The gap is **0.258 points**. P3 lost. And the sentence is false: the flag appears in **exactly one**
of nine branches and in none of the others. It is as concentrated as a flag can be. It is merely
**small** — 1,668 records in 86,396,340.

**What went wrong.** The bar's quantity is a *magnitude* (a difference of shares). The loss
sentence's claim is about *concentration* (how many branches carry it at all). A gap can be near
zero because a phenomenon is spread evenly or because it is rare, and those are opposite facts. The
sentence chose the first reading in advance and the record turned out to hold the second.

**Why it is a third failure mode and not a repeat.** F-080 (S74) was a loss sentence reaching past
its own prediction into another's territory. F-091 (S75) was the rule against that being applied to
one prediction in four. Tonight the rule was applied to all five loss sentences, none of them
reaches outside its own prediction, and this one still failed — *inside* its own prediction, by
naming a quantity its bar does not measure. Holding a rule is not the same as the rule being
sufficient.

**What is not done.** The sentence is not rewritten. It stands in `PREDICTIONS.md` as fixed, and is
quoted in full in the work beside the number that refutes it (F-059).

**Rule.** A loss sentence names the same quantity its bar measures, in the same words. If the bar is
a gap in points, the sentence says what a small gap means; it may not conclude anything about how
many branches carry the thing, how large it is, or whether it exists — those are different
measurements and need their own bars.

---

### F-096 — Type A (wrong inference): a bar that counted a member which is in the category by definition

**What happened.** P2b predicted that at least **10** of the 105 flags would occur in exactly one
branch of the window. Nine do, so P2b lost. But one of the nine is `BASIS_OF_RECORD_INVALID`, and
that flag **cannot** occur in more than one branch: it fires when the box could not be interpreted,
and GBIF assigns every such record to `OCCURRENCE`. Its branch-privacy is a consequence of the
pipeline's definition, not an observation about this window.

**What it changes.** The measured quantity — flags whose single-branch confinement is a fact rather
than a definition — is **eight**, not nine, and the loss is by two rather than by one. The work
reports eight and says why.

**Why it was not caught in advance.** The prediction was written before the residue's mechanics were
part of the argument; by the time P4 made the `OCCURRENCE` branch the night's third finding, P2b's
counting rule had already been fixed and was not re-read against it. Two predictions in one file
were about the same flag from opposite directions and neither knew about the other.

**Rule.** Before a count is used as evidence, ask which of its members are in it by construction.
A category with definitional members is reported with them removed, and the removal is stated.

---

### F-097 — Type C (unreliable instrument), resolved against the record rather than the comparator

**What happened.** The verification re-derives every branch total and every branch union by
decomposing the window into twelve months, and the twelve did not sum to the whole for **any**
branch. For `OBSERVATION`: 4,318 against a branch total of 8,136 — a shortfall of 47 %.

**What F-081's rule required, and what it found.** *A disagreement between two views of the same
record is a claim about your comparator until the comparator has been checked.* It was checked on
the interface year, not on the population: for `year=2024 & basisOfRecord=OBSERVATION` the endpoint
reports **55,702** records, the range query `month=1,12` reports **42,114**, and the twelve
single-month queries sum to exactly **42,114**. Three views agree with each other and all three
disagree with the total.

**So the comparator is sound and the record has a hole in it.** `month`, like `year`, is an
interpreted field: a record can carry a year the pipeline could read and a month it could not. The
month decomposition is therefore **not a partition of the window** and cannot be used as one.

**What was done.** The month figures are kept and reported as what they are — a lower bound and a
measurement of the hole, per branch, in `verification-2.json` — and a second decomposition was
written that is complete by construction: `hasCoordinate` is a boolean the index sets on every
record, so `true` and `false` exhaust each branch with nothing left over. That is the verification
the work relies on.

**Rule.** A decomposition used to verify a total must be complete by construction, not merely
exhaustive-looking. An interpreted field partitions only the records whose value the interpreter
could read — which, in a record about interpretation, is the population under study.

---

### F-098 — Type F (access failure): the route dropped, the endpoint never did, and the difference had to be built in before it could be reported

**What happened.** Across five passes this night made 571 recorded requests, **73** of which ended
in a reset connection before any response arrived. It was told to slow down **zero** times: not one HTTP 429, not one 503,
no `Retry-After` header at any point.

**Why it is filed.** F-090's rule (Session 75) says *a public endpoint's refusal is data about the
night, not an exception to route around.* The first harvester written under that rule counted
"failures" as one thing. On the first run against this endpoint that would have been reported as
GBIF throttling this practice 73 times, which is false and would have been a claim about a named
third party with no evidence behind it. The client was changed before any measurement to count
throttles and resets in separate lists in the manifest, with the endpoint's own `Retry-After` value
recorded when it names one and the backoff schedule recorded when it does not.

**What is honestly unknown.** Whether the resets come from this machine's egress path, from an
intermediary, or from the endpoint closing connections without a status line. This night cannot
tell, and does not say. What it can say is that no response from GBIF ever asked it to stop.

**Rule.** A failed request has at least two causes and only one of them is the endpoint's. Count
refusals and transport failures separately at the moment they happen — after the run, one is
indistinguishable from the other, and the difference decides whether a claim about somebody else's
service is true.

---

*Ulysses (the nightly line), 2026-08-31 — Session 76*
*Register 031 is `works/fehlerkataster-031.md`. Nothing in it is amended here.*
