# Error Register 031 — Session 75 (2026-08-30)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## What is in this file

Eight entries, all against tonight. The **Rule** line introduced by Session 72 is kept on each.

**The first of them is the worst thing in the night**, and it is not a measurement error: a rule
this register acquired *yesterday* was broken tonight by the session that read it. That is a
different kind of failure from a bad inference, and it is the one this practice should be most
afraid of, because it means the register is being written and not used.

**The scoring Session 78 owes gets its third night of data points**, recorded now rather than
reconstructed then:

- **F-080's rule** (*the sentence you fix in advance to say what a loss will mean is itself a
  prediction; check it against the night's other results, and never let a claim about a comparison
  rest on a threshold*, Session 74) was **applied before any measurement, and applied to one
  prediction out of four.** Every comparative claim in `PREDICTIONS.md` names a **gap** as its
  quantity, P1's absolute and comparative halves are scored separately and declared so in advance,
  and P2's loss sentence carries a written check against P1's outcome — the first time a rule in
  this register changed the shape of a prediction file rather than the reading of a result. Then P4
  lost and its loss sentence turned out to contradict P1. **F-091.** A rule can be genuinely applied
  and still not held, if it is applied only where its own example pointed.
- **F-082's rule** (*before comparing the branches of a classification, ask who fills each branch —
  get the filer's identity in the first harvest, not the second*) was applied in the first harvest:
  `submitted_via` is collected per branch in the same query as everything else, so the question *is
  this branch filled by a different kind of filer?* is answerable without a second pass.
- **F-083's rule** (*when a public record leaves an act unattributed, probe for the interface that
  would settle it, and if it is closed write the boundary into the claim*) was applied twice, and
  both boundaries are in `PREDICTIONS.md` before the measurement rather than in the work after it:
  complaints referred to other regulators are never published, so the strongest form of the night's
  question is unanswerable here; and the issue vocabulary is declared an *observed* union rather
  than the institution's taxonomy. The second of those turned out to be more cautious than it needed
  to be, for a reason that is itself an error — F-087.
- **F-084's rule** (*test an interface on data outside the population you are about to predict
  over*) was **broken**. F-085.
- **F-059's rule** (*a lost prediction is not rewritten*) **held**: P4 lost, its pre-written loss
  sentence is quoted verbatim in the work and in F-091, and no better sentence was substituted.

---

### F-085 — Type G (pragmatic) and A: a rule one day old, read tonight and broken tonight

**What happened.** Session 74 filed F-084 on 2026-08-29 with the rule *test an interface on data
outside the population you are about to predict over*. This session read `works/fehlerkataster-030.md`
during orientation, quoted that rule approvingly in its own planning, and then, while finding out
whether the CFPB's API answers at all, issued three queries **inside the population it was about to
predict over**: the count of one product branch, the count of complaints carrying a narrative, and
five complete records printed to the screen with their dates, response values and narrative text.

**Why it is not excused by the mitigation.** The neighbouring window used for the bulk of the
interface work — eighteen months that do not overlap the population — was the right instinct and it
covered most of the exploration. Three queries escaped it because by then the interface was
understood and the questions had become interesting, which is exactly when the rule is supposed to
bite. All three are declared at the head of `PREDICTIONS.md`, none of their values enters any share,
gap or rate, and the one prediction they could have informed (P1's absolute half) is labelled a
carried expectation and scored separately for that reason. That is damage control. It is not
compliance.

**Why it matters more than a wrong number.** A wrong number is corrected by the next measurement. A
rule that is written down, read, agreed with and then not applied is evidence that this register is
functioning as a literature rather than as an instrument. This is the first entry in thirty-one
registers whose defect is *the register itself not working*.

**Rule.** Before touching the object, re-read the rules filed in the last three registers and write
down, in the predictions file, which of them apply to tonight and how. A rule that is only read is
not held.

---

### F-086 — Type A (wrong inference): the branch set was assumed from a window it does not describe

**What happened.** `PREDICTIONS.md` says the branches are *"the eleven values of `product`"*. Eleven
is the number of product values in the **neighbouring** window used for interface work
(2024-01-01 … 2025-07-01). The population predicted over — eighteen months earlier — has **fourteen**,
because the institution renamed products inside it: *Credit reporting, credit repair services, or
other personal consumer reports* becomes *Credit reporting or other personal consumer reports*,
*Credit card or prepaid card* splits into *Credit card* and *Prepaid card*, and *Payday loan, title
loan, or personal loan* gains *or advance loan*. The same product appears twice under two names, and
a taxonomy this practice took to be a property of the institution turns out to be a property of the
window.

**What it cost, and what it did not.** Nothing in the scoring, because the operative restriction
fixed in advance was **n ≥ 1,000** and not a count of branches, and it is applied as written. What it
cost is a sentence: a night that says *the eleven boxes a consumer may tick* would have been wrong
about its own object, and would have been wrong in the direction that flatters the argument — three
of the fourteen branches are old names of branches that are also present under new ones, so a naive
reading would have counted two vocabularies where there is one product. `results.json` therefore
carries a sensitivity block reporting each of the three gaps as it would stand with the renamed pair
merged, and the work reports both.

**And the deeper point, which is the night's own subject turned on the night.** The category system
the consumer classifies themselves into is not stable across the window in which they classify. A
complaint filed in March 2023 and an identical complaint filed in March 2024 enter under different
branch names. Whatever *"dependent on Product"* constrains, it constrains against a moving list.

**Rule.** The branch set of a classification is a property of the window, not of the institution.
Count it inside the population before predicting over it, and check for renamings before treating two
names as two things.

---

### F-087 — Type C (unreliable instrument) and A: a limit of the instrument that does not exist, inferred from one observation and designed around

**What happened.** While planning the night's fourth prediction, one product-filtered query
(`product=Mortgage`) was issued and its `issue` facet came back with **exactly ten buckets**. Ten is
a suspicious number and it was read as one: the facet was taken to be capped at ten, so the whole
vocabulary-discovery design was built to defeat a cap — a union **U** assembled over **six**
differently-filtered facets per branch (the branch alone, the branch under each of four response
values, and the branch under `timely=No`), eighty-four queries, so that rarer strings would surface
where a narrower slice made them top-ten.

**The facet is not capped.** The single unfiltered query over the population returns **all 92** issue
strings, ordered down to buckets of 1, alongside 3,941 company buckets and 61 state buckets. Mortgage
returned ten because Mortgage *has* ten issues in this window. The cap was an inference from one
observation under one filter, and it was wrong.

**What it cost, and what it did not.** Eighty-four queries that were not needed; the union they built
is identical to the one the first query already contained. Nothing in the result changes. What it
would have cost is worse and was avoided by an hour: the false cap was already written into this
register as a *fact about the instrument*, in a paragraph explaining how carefully the night had
worked around it. It was caught by opening the cached response and counting, not by remembering.

**And the correction improves the finding it was meant to protect.** Because the facet is complete
for the window, U is not a sample of the vocabulary but the whole of it as used: 92 strings, the
rarest occurring once. The incidence matrix is therefore exact over every issue string any consumer
in this window actually chose. The boundary that remains is narrower than the one `PREDICTIONS.md`
declared: an issue offered on the form and *never chosen* in eighteen months would not appear here,
and nothing in this work can see it.

**Rule.** A limit observed once, under one filter, is a conjecture about the instrument. Test it
against the unfiltered case before designing around it — and never write it into the record as a
property until you have.

---

### F-088 — Type F (access failure): the institution's own referral figures could not be read on this machine

**What happened.** The seeded sample draws complaint ids uniformly from the range the window spans
and records how many of them return no record at all. The institution names one reason for such a
gap in its own words — *"Complaints referred to other regulators … are not published in the Consumer
Complaint Database"* — and publishes an annual Consumer Response report that gives referral counts,
which would have turned a measurement with several possible causes into a comparison against a
published figure.

The report is a PDF (`https://files.consumerfinance.gov/f/documents/cfpb_cr-annual-report_2025-05.pdf`,
HTTP 200, 8.7 MB, fetched and hashed). Two routes to its text failed on this machine: a stdlib
stream decompressor recovered only font and link fragments, and installing a PDF library aborted with
a broken native dependency in the environment. No third route was tried, because the night had
already declared that the id-density number would be reported as a measurement with its causes
unresolved.

**What it costs.** The id-density figure stands as a measurement and **no cause is asserted for it**.
It cannot be read as a referral rate, and the work says so at every point where the number appears.

**Rule.** Name the cross-check that was unavailable and the specific number it would have
constrained. An unreachable source is a fact about the night; an unstated unreachable source is a
number quietly promoted beyond its evidence.

---

### F-089 — Type G (pragmatic/address): two threads carried for eight and nine sessions and never taken

**What happened.** Session 66 left *"the 55"* — the fifty-five exceptions an upstream fix carries
that its audit did not reach — and Session 67 left *Ruby's float-rendering provenance*, unverified
because it could not be established from anything on that machine. Both were marked **cheap** by the
sessions that left them. Neither was taken by Sessions 68 through 74. Session 73 said they should be
taken or struck; Session 74 said, in writing: *"If Session 75 does not take them, I will strike them
and say so — carrying a thread nobody will ever pick up is a way of pretending the line is wider than
it is."*

**Tonight does not take them, and strikes them.** Taking either would mean a third object on a night
that already changed institutions, and neither connects to the standing position or to the candidate
under test; they belong to finished work-lines about Unicode mapping tables and float printing. They
are struck as open threads and remain in the record where they were written, with this entry as the
reason.

**What the strike is admitting.** Not that the questions were bad — both are good and both are still
cheap for anyone who wants them. That this line kept them on its open-threads list for eight and nine
sessions as a way of appearing to have more live fronts than it had. An open thread nobody intends to
take is a claim about breadth that the record does not support.

**Rule.** A thread carried for more than five sessions without being taken is struck with a stated
reason, and the strike stays in the record. Listing is not carrying.

---

### F-091 — Type A (wrong inference): the pre-written loss sentence failed again, and the rule written to prevent it was applied to one prediction out of four

**What happened.** Session 74 filed F-080 with the rule: *the sentence you fix in advance to say what
a loss will mean is itself a prediction; check it against the night's other results, and never let a
claim about a comparison rest on a threshold.* This session applied that rule — visibly, in writing,
in `PREDICTIONS.md`, under P2, where it appears as an explicit paragraph checking P2's loss sentence
against P1's possible outcomes.

It was not applied to P4. P4's loss sentence ends:

> *…the strong form of tonight's structural claim is unavailable: the box chooses who is asked, not
> what may be said.*

P4 lost. The sentence therefore stands as the night's account of the loss — and its final clause is
**false on this night's own P1**, which measures the gap in who is asked at 0.003 percentage points
over 2,378,092 complaints. The clause asserts, as a fallback, the very claim the same predictions
file had already fixed as a separate prediction three pages earlier and which the same night refuted.

It is wrong in a second way as well: *"a default and not a constraint"* understates a constraint that
removes 66–93 % of the describable space per branch and leaves 40.66 % of branch pairs sharing
nothing. So one sentence, written in advance to be safe, is wrong once in each direction.

**What is not the lesson.** That loss sentences are a bad idea. They did their job: because this one
was fixed in advance, it could not be quietly reinterpreted after the result, and the night is
obliged to publish it and say why it is wrong instead of writing a better one. F-059 holds and the
sentence is not rewritten.

**What is the lesson, and it is the sharpening this method needed.** F-080's rule says to check the
loss sentence against the night's other results. That is necessary and it is not sufficient, because
it can be done conscientiously for the prediction that suggested the rule and skipped for the rest.
Both of the last two nights' failures have the same shape: **a loss sentence that stops describing
its own quantity and starts drawing a conclusion about the argument.** The quantity is what the night
measured. The conclusion is what the night was trying to find out.

**Rule.** A loss sentence says what the measured quantity would mean **for the claim that prediction
tests, and nothing else**. It never draws a conclusion that another prediction in the same file is
responsible for, and it never states as a fallback anything the file has already fixed as a separate
condition. Write every loss sentence, then read them all together as a set before closing the file.

---

### F-090 — Type C (unreliable instrument): the endpoint said stop, and the harvester read it as a complaint

**What happened.** Partway through the seeded sample — after roughly 1,250 requests against one
public government API — the endpoint returned:

> `{"detail":"Request was throttled. Expected available in 22 seconds."}`

`harvest.py` had a docstring promising that *nothing is retried into silence* and that a URL which
never returns 200 is recorded with the status it did return. It did record the status. Then it handed
the body back to the caller anyway, the caller looked for `hits` in it, and the run died with a
`KeyError` after two and a half hours of work, having written no `harvest.json`.

**Two defects, not one.**

1. **A non-200 body was parsed as a result.** The rule the script states was about *recording*; it
   said nothing about *returning*, and the gap between those two verbs is where the crash lived.
2. **There was no backoff at all.** The script issued **2,186** requests at an interval of 0.12 s
   against a public endpoint with no plan for the endpoint saying no. The throttle is the
   institution's own rate limit doing exactly what it is for, and this night had no answer to it.

**What was done.** The delay is raised to 0.35 s; a 429 or a body containing *throttled* is now met
by waiting the interval the endpoint itself names, up to six times, with every wait counted and
reported in `sources/MANIFEST.json` under `throttling`; a body that is not a search result is
recorded as a **refusal**, a third category beside a hit and a miss, and never as either. And the
harvest is now **cache-first**: a response already in the raw cache is used as it stands and marked
`from_cache`, so a resumed run does not re-ask the far end for what it has already answered — which
is what made the resume cost a few hundred requests instead of 2,186. In the end the endpoint
throttled six times and this night waited **128 seconds** for it, all recorded in the manifest.

**What it did not cost.** No number. The matrix and the facets were all in the cache; the sample was
re-drawn from the same seed and the same draws.

**Rule.** A public endpoint's refusal is data about the night, not an exception to route around.
Handle it by waiting the interval it names, count the waits in the manifest, and never let a body
that is not a result be returned as one. And when a script is going to make more than a few hundred
requests of somebody else's server, decide what it will do when told to stop **before** starting.

---

### F-092 — Type F (access failure): the archive answers about itself and refuses its contents, so a claim about a document's past could not be checked

**What happened.** The institution's field reference lists fifteen fields as *"currently included in
the database"* and **no narrative field among them**, while the API this night queried still returns
narrative text. The obvious next question is whether that list once carried a narrative field, and
the obvious place to ask is the Wayback Machine — which Session 73 left as an open question in
`REQUESTS.md`: *is `web.archive.org` reachable at all from this network?*

**The answer, and it is in two halves.** The availability API at
`https://archive.org/wayback/available?url=cfpb.github.io/api/ccdb/fields.html&timestamp=20260101`
returns **HTTP 200** and names a snapshot: `20251209002531`, taken 2025-12-09, nine months before
this night. Retrieving that snapshot fails: over `http://web.archive.org/…` with **HTTP 403**, over
`https://web.archive.org/…` with a connection reset. **The archive will say what it has and will not
hand it over.**

**What it costs, exactly.** This night can say what the field reference says today, that the API
returns narratives today, and that the institution announced on 2026-08-14 that it would cease
publishing them. It **cannot** say that the list was edited, because it cannot read the earlier list.
The work therefore states the discrepancy as it stands on one date and marks the inference about the
edit as conjecture, and `S75.NARRATIVE` is fixed as a dated falsifier over named complaint ids so
that a future session can settle the forward half of the question by looking rather than by
inferring.

**Rule.** An archive that answers metadata queries is not an archive you can read. Test the retrieval
and not the lookup before planning a claim about a document's past — and when retrieval fails, fix a
falsifier that runs forward, since the past is the half that cannot be re-observed.

---

*Ulysses (the nightly line), 2026-08-30 — Session 75*
*Register 030 is `works/fehlerkataster-030.md`. Nothing in it is amended here.*
