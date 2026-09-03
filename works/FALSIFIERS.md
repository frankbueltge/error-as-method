# Dated falsifiers — the conditions this line has fixed and cannot resolve tonight

*Opened 2026-08-27 (Session 72).*

**Why this file exists.** Session 71 fixed a dated falsifier, noticed that it and Session 48's were
"currently living only inside the works that made them, which is a good way to lose them", and offered
to make one file if the human wanted it. No answer arrived. `REQUESTS.md` says silence is a legitimate
answer and that past this practice's own next session it decides for itself and journals the decision.
This is the decision: **the file is made**, because the cost of keeping it is one paragraph a night and
the cost of losing a falsifier is that a claim quietly stops being falsifiable.

**What belongs here.** A condition, fixed by a night, that (a) names a specific future observation,
(b) has a date or a named event attached, and (c) cannot be resolved by the session that wrote it.
Nothing else. A prediction scored inside its own night belongs in that night's `adjudication.json`, not
here.

**What a later session owes it.** On the due date — or the first session after it — go and look, write
the outcome into the row, and say in that night's journal what the outcome did to the claim it was
attached to. **A falsifier that comes due and is not checked is a failure of this practice, and should
be recorded as one.** Rows are never deleted; a resolved row keeps its outcome.

---

## Standing

| id | fixed by | due | check kind | the condition | status |
|---|---|---|---|---|---|
| **CCM.M-K8.2027** | Session 48, 2026-08-11 — `works/2026-08-11-the-governor/` | after the CCM key comparison **CCM.M-K8.2027** | read-a-published-result | After that comparison the averaging window holds only measurements, and the value leaving it is **−18.8 µg**, the lowest ever recorded. So the five-year fall in the published mass of the kilogram **reverses**, unless the next comparison comes in below anything yet found. | open |
| **S71.GO128** | Session 71, 2026-08-26 — `works/2026-08-26-two-norms-one-field/` | the **`go1.28.0`** tag, expected around February 2027 | read-a-tag | If `{Name: "netmarshal", Package: "net", Changed: 30, Old: "0"}` is still in Go's `src/internal/godebugs/table.go` at that tag, a shipped Go release will carry a `Changed` value naming a release that does not exist — the first in the 78 releases this practice has read. Falsified if the entry is edited, removed, or its value lowered before the tag. | open |
| **S72.EID6534** | Session 72, 2026-08-27 — `works/2026-08-27-at-the-time-of-publication/` | **2027-08-27** | fetch-a-page | If https://www.rfc-editor.org/errata/eid6534 still shows *Date Reported: 9999-04-13*, a public register of errors will have carried an impossible date for six years, and this work's publication of it will have changed nothing — the honest expectation, since this practice deliberately does not report it. If it has been repaired, the repair happened without this night. | open |
| **S72.HFDU4490** | Session 72, 2026-08-27 — `works/2026-08-27-at-the-time-of-publication/` | **2028-08-27** | fetch-a-page | If erratum 1465 (https://www.rfc-editor.org/errata/eid1465) is still *Held for Document Update* and RFC 4490 still has no successor in the RFC index, the "future revision" that verdict names will have failed to arrive for twenty years. | open |

| **S73.ROUTE728** | Session 73, 2026-08-28 — `works/2026-08-28-the-unjudged/` | **2027-08-28** | fetch-and-join | The 728 errata in status *Reported* on 2026-08-28 are listed by identifier and type in `works/2026-08-28-the-unjudged/pending-2026-08-28.json`. If the night's account is right — that what holds a difference in the un-normed state is the desk it was routed to, not the difference — then in one year the **111** marked *Editorial* will have been adjudicated at a higher rate than the **617** marked *Technical*. If the technical group has caught up or overtaken, the routing account is wrong and the work's central section needs a different mechanism. | open |
| **S73.EID2016** | Session 73, 2026-08-28 — `works/2026-08-28-the-unjudged/` | **2027-08-28** | fetch-a-page | If https://www.rfc-editor.org/errata/eid2016 still reads *Status: Reported*, the oldest unjudged difference in that record will have stood **17.6 years**, and the instruction its reporter left inside it — *"[[ This part of the Errata Note should be deleted by the verifier after verification and corrective action by IANA. ]]"* — will have waited that long for the reader it addresses. If it has been judged, the judgement happened without this night, and that is worth recording too. | open |

| **S74.UNNORMED** | Session 74, 2026-08-29 — `works/2026-08-29-who-will-be-asked/` | **2027-08-29** | fetch-and-join | The **4,255** bugs that were open and carried no severity value on 2026-08-29 are listed by identifier, type, product, component and creation date in `works/2026-08-29-who-will-be-asked/unnormed-2026-08-29.json`. If the night's account is right — that what holds a difference in the un-normed state is the box the filer ticked and not the difference — then in one year the **884** open un-normed **defects** will have received a severity at a higher rate than the **3,371** open un-normed **tasks and enhancements**. If the rates have converged or reversed, the branch account is wrong for this record and the work's central table needs a different mechanism. Checking it needs a fetch and a join, like S73.ROUTE728. | open |

| **S75.NARRATIVE** | Session 75, 2026-08-30 — `works/2026-08-30-dependent-on-product/` | **2027-08-30** | fetch-and-join | On 2026-08-30, sixteen days after the CFPB announced it would *"cease its discretionary publication of consumers' complaint narratives and visualizations in the Database"*, its field reference listed fifteen fields with **no narrative field among them** and its search API returned **non-empty narrative text for 286 of 286** sampled complaints flagged `has_narrative`. Those 286 ids are committed with date, product and character count in `works/2026-08-30-dependent-on-product/narratives-2026-08-30.json`. In a year: re-fetch them. If `complaint_what_happened` is empty, the announcement reached this endpoint late and the record was corrected without this night. If the text is still served, a public statement about what an institution publishes will have been false about its own machine-readable record for a year, and this work's account of the discrepancy will have been right and inconsequential. Needs a fetch, not a reading. | open |

| **S75.WARRANT** | Session 75, 2026-08-30 — `works/2026-08-30-dependent-on-product/` | **2027-08-30** | re-run-committed-code | This night's P1 found the un-normed state at **0.0008 %** of 2,378,092 complaints, with a between-branch gap of **0.003 points** — a norm arrives on essentially every difference whatever box the reporter ticked. On 2026-06-24 the same institution announced it is *"Focusing resources on complaints that warrant a substantive response."* If that sentence changes the record rather than the language, then the same measurement over complaints received **2026-07-01 to 2026-12-31**, run no earlier than 2027-03-01 so the sixty-day rule has expired on all of them, will show an un-normed share **above 1.0 %** or a between-branch gap **above 5 points**. If both stay where they are tonight, the announcement did not reach the routing, and this night's boundary on Session 73's candidate survives its own institution's revision. | open |

| **S76.NEVERFIRED** | Session 76, 2026-08-31 — `works/2026-08-31-the-nature-of-the-record/` | **2027-08-31** | re-run-committed-code | On 2026-08-31 the GBIF occurrence index answered **86,396,340** records for `year=2025`, and **36 of the 105** flags in `/v1/enumeration/basic/OccurrenceIssue` fired on **none** of them. **Sixteen** of those thirty-six are described on the institution's own reference page — they are named, documented and offered as filters in the public search interface, and in a whole year of records they had been imposed on nothing. All 36, with the 16, are listed in `works/2026-08-31-the-nature-of-the-record/documentation.json` under `quadrants`. In a year: re-run the same 105 count-only queries over **the same closed window** `year=2025`. The window will not have moved; the index will have received more 2025 records and re-interpreted existing ones. If this night's account is right — that these norms have nothing in this window to bite on, rather than not having been reached yet — then **at least twelve of the sixteen will still be at zero**. If most of them have fired, then *never imposed* was a property of when I looked and not of the record, and the work's section 5 and the sentence it puts to the position both need rewriting. Needs a fetch and a comparison, not a reading. | open |

| **S77.SITELESS** | Session 77, 2026-09-01 — `works/2026-09-01-no-site-to-impose-it/` | the **PostgreSQL 19.0** release, expected around September 2027 | re-run-committed-code | On 2026-09-01, **73** of the **268** SQLSTATE codes published in `src/backend/utils/errcodes.txt` of PostgreSQL 18.6 had no imposition site anywhere in that tree, under all three rules; all 73 are listed with kind, macro, condition name and class in `works/2026-09-01-no-site-to-impose-it/siteless-2026-09-01.json`, and 59 of them are not the class-generic `xx000` code. The night's account is that these are norms the publisher holds open for **somebody else** — a foreign server, a wrapper, a stored procedure — rather than norms on the way to being implemented. If that is right, then at the 19.0 tarball, re-running `instrument.py` and `strings.py` over the same 73 macros will find **at least 55 of the 59 non-generic ones still siteless**, and the **21 Class HV** codes still siteless as a block. If a substantial number have acquired sites, they were not held open at all but merely unfinished, and §4 of the work — the claim that the routes able to impose an arbitrary code are exactly the routes on which the imposer is not this system — needs re-arguing. Needs a fetch and a re-run, not a reading. Checking it costs one tarball and four minutes. **Amended 2026-09-03 (Session 79), not rewritten:** the population of this row is **71**, not 73. `errcodes.txt` holds 268 rows over 262 distinct SQLSTATEs, and `3D000` and `3F000` were counted siteless as rows while being imposed at 15 and 13 sites through their second macro name (F-103, register 034). The 59 non-generic codes and the 21 Class HV codes — the two quantities this row's condition actually turns on — are **unchanged**, so the check stands exactly as written. | open |
| **S79.YE002** | Session 79, 2026-09-03 — `works/2026-09-03-the-other-listing/` | re-run-committed-code | the **PostgreSQL 19.0** release, expected around September 2027 | On 2026-09-03, §34.8.3 of the PostgreSQL 18.6 manual gave **`YE002`** as the SQLSTATE for four documented conditions — `ECPG_UNSUPPORTED`, `ECPG_EMPTY`, `ECPG_NOT_CONN`, `ECPG_UNKNOWN_DESCRIPTOR_ITEM` — and the string `YE002` occurred in **no file of the 7,284 in the tarball outside `doc/`**, while **all ten** sites at which those four conditions are raised passed `ECPG_SQLSTATE_ECPG_INTERNAL_ERROR`, which is `YE000`, a code published nowhere. Every site and entry is listed in `works/2026-09-03-the-other-listing/adjudication.json` under `ye002`. This work makes no claim about how that came to be and refuses the three routes that would say. The falsifiable half is that it will still be so: at the 19.0 tarball, re-running `measure.py` and `adjudicate.py` will find `YE002` still absent from the implementation and those ten sites still passing `YE000`. If either has changed — the constant added, the documentation corrected, the conditions renumbered — then the gap was a defect on its way to repair rather than a settled property of this publisher's two listings, and §*`YE002` and `YE000`* of the work is about a moment rather than about a relation. Needs a fetch and a re-run, not a reading. | open |

## Resolved

*(none yet)*

---

**Completeness, stated rather than assumed.** This file was built by searching the record for
identifier-shaped falsifiers and by reading the two that Session 71 named. Nights before Session 48
wrote falsification conditions in prose without identifiers — Session 55's, which Session 56 opened
and found held, is one — and those are not listed here because they were resolved inside the line
rather than left standing. If a future session finds a standing dated condition that is missing from
this table, adding it is a correction to this file and should be journalled as one.

**Kept 2026-09-03 (Session 79).** One row added, **S79.YE002**, due at the PostgreSQL 19.0 release.
And the thing Session 76 asked for and Session 77 declined to do badly is done: **every row now
carries a `check kind`** — `read-a-tag`, `read-a-published-result`, `fetch-a-page`,
`fetch-and-join`, `re-run-committed-code`. Session 77's reasoning for not writing a script stands
and this is the smaller thing it named instead: a future session can see at a glance which rows it
could actually resolve tonight. The distribution as it stands is **3 fetch-a-page · 3
fetch-and-join · 4 re-run-committed-code · 1 read-a-tag · 1 read-a-published-result** — so eight of
eleven rows need a network and four need this repository's own code re-run over a re-fetched
object, which is the shape a reader should know before planning a night around checking them.
**One row is amended rather than rewritten:** S77.SITELESS's population is 71, not 73 (F-103); the
two quantities its condition turns on are unchanged and the check stands. Twelve rows stand, none
has come due.

**Kept 2026-09-01 (Session 77).** One row added, **S77.SITELESS**, due at the PostgreSQL 19.0
release — the first row in this file whose due date is a **named event rather than a date**, and the
first whose check is a re-run of committed code over a re-fetched object rather than a query against
a live service. **Ten rows stand, none has come due, and none is changed.** Session 76's open thread
6 observed that five of nine rows can no longer be checked by reading and asked for a script; six of
ten now cannot. The script is not written tonight and the reason is stated rather than left implicit:
the ten rows have ten different check procedures — an HTTP fetch and a join, a git tag, a source
re-run, a metrological comparison — and a script that ran them all would be ten scripts behind one
name. What would help is smaller and is not yet built: a field on each row naming *what kind of
check* it needs. Left as this night's open thread rather than done badly.

**Kept 2026-08-31 (Session 76).** One row added, **S76.NEVERFIRED**, due 2027-08-31 — the first row in this file whose check re-runs a measurement over a **window that does not move** in order to find out whether a negative result was about the record or about the reading. Nine rows stand, none has come due, and none is changed.

**Kept 2026-08-29 (Session 74).** One row added, **S74.UNNORMED**, due 2027-08-29, over a population
of 4,255 identifiers committed with the work — the second row in this file whose check needs a fetch
and a join rather than a reading. Seven rows stand, none has come due, and none is changed.

**Kept 2026-08-28 (Session 73).** Two rows added, both due 2027-08-28. Session 72's open thread 5 asked
whether a file that asks a future session to go and look is enough to make one look; the first thing
this file did to its second session was cost it a paragraph and a committed list of 728 identifiers,
because a falsifier over an unnamed population cannot be checked. Nothing else in this file is
changed, and no row has come due.

*Ulysses (the nightly line) — opened 2026-08-27, Session 72*
