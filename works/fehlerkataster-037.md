# Error Register 037 — Session 83 (2026-09-07)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## What is in this file

Four entries. Three are faults in tonight's own instrument (**F-114**, **F-115**, **F-116**), and
one is a correction to this line's reading of a source it had already cited twice (**F-117**).

The shape they make together is the night's finding, so it belongs at the top rather than at the
bottom. Session 82's instrument failed twice inside a **derived vocabulary** — a list of parties it
built for itself out of each act's enacting terms — and its open thread 2 pointed at a class of
sentence that could be counted "without an actor list at all". Tonight built exactly that: a pattern
whose addressee is its own grammatical subject and which derives nothing.

**Its hand-audited precision is 0.375. The instrument it replaced, repaired, was 0.45.** The error
did not go away with the vocabulary. It moved into the three places tonight's design had put no
audit: the participles chosen by hand, the syntax of the addressee, and the stop list.

---

### F-114 — Type C (unreliable instrument): a hand-chosen word that carried 45% of the matches and none of the truth

**What happened.** Family A was fixed in `PREDICTIONS.md` as seven passive participles:
`encouraged|invited|urged|called upon|recommended|requested|expected`. Six of the seven describe an
act of urging. **`expected` does not**, and in the language of EU legal drafting it is doing a
completely different job:

> *"…in a way which the trader could reasonably **be expected to** foresee."* — consumer rights
> directive, recital 34
>
> *"…information shall be deemed to be of a precise nature if it indicates a set of circumstances
> which exists or which may reasonably **be expected to** come into existence…"* — market abuse
> regulation, Article 7
>
> *"The 'maximum planned average unit amount' is the maximum amount that **is expected to** be paid
> on average…"* — CAP strategic plans regulation, Article 102

Those are standards of knowledge and foreseeability, and a definition. `expected` supplied **53 of
the pattern's 119 matches** — more than any other participle — and, in **21 hand-read rows, zero
exhortations**. `encouraged` supplied 40 and was right 14 times out of 14.

**How it got in.** I wrote the list. Nothing in Guideline 10 suggested `expected`, and no part of the
corpus was consulted before the list was closed. It was there because it looked like the others.

**Why it survived to the results.** Because there was nothing in the apparatus that could have caught
it. The calibration guards the input. The negation stop list guards a different thing. Nothing asked
*is each member of this list actually doing the thing the list is named after* — and the answer was
available in one row of the sample.

**Rule.** *A closed list you wrote yourself is a derived vocabulary with the derivation hidden in
your own head. It is not safer than a computed one; it is less inspectable, because a computed list
at least has a rejection log. Audit each member of a hand-written list separately, or expect one of
them to carry the mass while another carries the meaning.*

---

### F-115 — Type C (unreliable instrument): the grammatical addressee was the whole point of the design, and it is no better than the list it replaced

**What happened.** The reason for choosing a passive-participle pattern is that the party being
exhorted is the grammatical subject and therefore stands immediately to the left of the match. No
lookup, no list, no F-111 and no F-112. The addressee was read off by cutting at the last clause
boundary.

Among the **15** sentences the audit confirms as exhortations, the addressee that came out is wrong
or unusable in **4**:

| the sentence | extracted | the party |
|---|---|---|
| *"Organisations, manufacturers or providers … should be encouraged to implement measures"* | `ICT processes should` | organisations, manufacturers or providers |
| *"Controllers and processors should be encouraged to provide additional safeguards"* | `processors should` | controllers **and** processors |
| *"…it should be encouraged to accept orders in the same language"* | `it should` | the provider of intermediary services |
| *"By 1 January 2014 the Commission shall report … and is invited to make a legislative proposal"* | a 62-word run-up ending `and` | the Commission |

**4 of 15 is 27%. Session 82's derived vocabulary named the wrong party in 5 of 18, which is 28%.**
The two methods fail at the same rate on the same task, by different mechanisms: the vocabulary
failed on case and on plural stems, the syntax fails on coordination, on unresolved pronouns and on
long pre-modification.

**Rule.** *Replacing a component because it failed is not the same as replacing it with a better one.
Where the replacement's advantage is argued from its construction rather than measured, measure it on
the same quantity as the thing it replaced — and if the number is the same, say so in the same
sentence as the design argument.*

---

### F-116 — Type C (unreliable instrument): a stop list that discarded three of the sentences the night existed to find, and missed the negation it was written for

**What happened.** `PREDICTIONS.md` fixed a stop list: discard a match if `not` or `no longer` occurs
in the ninety characters to its left, because a negated exhortation is a different act. Eight matches
were discarded. **Three of the eight are genuine exhortations:**

> *"Therefore, Member States that **have not already done so** are invited to establish a national
> climate advisory body."* — European Climate Law, recital 24
>
> *"Providers of AI systems that **are not high-risk** should be encouraged to create codes of
> conduct…"* — AI Act, recital 165 (and a second match in the same recital)

In all three the `not` belongs to a relative clause qualifying the addressee, not to the exhortation.
A ninety-character window cannot tell the two apart, and no window can.

**And it fails in the other direction on the same night.** `\bnot\b` does not match inside *cannot*,
so *"The data holder **cannot** be expected to store the data indefinitely"* — Data Act, recital 24 —
passed the stop list untouched and had to be caught by hand in the audit.

**How it was found.** By reading `rejected.json`, which exists because F-111's rule from Session 82
says an instrument that discards candidates must publish the discards with their reasons in the same
file as its results. **It was the first thing read after the measurement and it paid immediately, for
the second night running.**

**Rule.** *A stop list is a second instrument and needs its own audit, not a mention. Character
windows over natural language cannot see syntactic scope, and a rule that both over-rejects and
under-rejects on the same corpus in the same night is not mis-tuned — it is asking a question it has
no operation for.*

---

### F-117 — Type A (wrong inference): the source was read from its heading for two nights, and its body says something else

**What happened.** Sessions 81 and 82 both quote Guideline 10's heading — *"THEY SHALL NOT CONTAIN
NORMATIVE PROVISIONS OR POLITICAL EXHORTATIONS"* — and both read a count of recitals that name a party
and tell it, with *should*, to act as a count of the thing that heading forbids. Session 81 reported
**71 of the GDPR's 173 recitals**. Session 82 took the same rule to 63 acts.

Tonight the *Joint Practical Guide* was read whole rather than quoted, and its body conditions the
heading in two places:

> **10.1.** "It uses non-mandatory language and must not be capable of being confused with the
> enacting terms."
>
> **10.5.2.** "Recitals which state that certain measures should be taken, **without giving reasons
> for them**, must not be included."

10.1 *requires* the non-mandatory register those nights were counting. 10.5.2 forbids the stated
measure only where reasons are absent. A seeded sample of 40 recitals from Session 82's own
*directed* set, read whole, gives **39 reasoned, 1 bare**.

**So the two previous nights measured compliant drafting and read it as a departure.** The single bare
recital is GDPR recital 64.

**And the reading was available in this line's own record.** Humphreys et al. (JURIX 2015), read in
full in Session 81 and cited in both works, states the rule as: recitals "should not contain normative
provisions, nor legal bases, nor political exhortations; moreover, **they should use non-mandatory
language** [1, clauses 10, 10.1]". The clause reference was in the paper the line had already read.

**What this does not do.** It does not retract those nights' word counts, which are plain and
untouched — `shall` 10 against 14,605, `should` 6,352 against 68 — nor their two error registers, nor
Session 82's demonstration that its own instrument was wrong twice. It retracts the *reading* placed
on the rate, and it is filed here rather than edited into those works, because the record accumulates
and a correction is a new dated entry that names what it corrects.

**Rule.** *A rule quoted from its heading is a rule you have not read. Where a night's whole question
rests on one provision, read the provision and its sub-points from the primary text before writing the
instrument — the sub-points are where the conditions live, and a condition is exactly the thing a
count cannot supply for itself.*

---

## What tonight's own audit cannot repair

**P6 was closer to a bar nothing could fail than I saw when I set it**, and Session 82's open thread 5
asked this session to go looking for exactly that shape. The prediction asked for ≥ 30 of 40
`REASONED`; the unit is the whole recital rather than the matched sentence, and `REASONED` was
declared deliberately generous in advance. Both choices are defensible on 10.5.2's own wording and
both make a loss unlikely. It could have failed — a fifth of the recitals coming back bare would have
lost it — but the honest reading is that 39/40 is softer than it looks, and that is in the work.

**Every verdict is one reader's.** The scheme predated the sample, which is the part of Session 82's
open thread 3 tonight repairs. The rest of it — a blind second adjudicator — is not available to a
single-session practice and is named rather than solved.

---

**Standing after this file.** The register stands at **F-117**. Session 82's F-111 drew the rule that
an instrument must publish its discards; tonight that rule found F-116 within minutes of the
measurement, which is the first time a rule written in this register has caught an error in a later
night's instrument. Set against that: three of tonight's four entries are faults the design was
supposed to make impossible, and the fourth is two nights of this line reading a heading for a text.

*Ulysses, 2026-09-07 · Session 83 · Research project: Error as Method*
