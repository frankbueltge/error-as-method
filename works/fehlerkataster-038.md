# Error Register 038 — Session 84 (2026-09-08)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## What is in this file

Five entries. Two are faults in tonight's measuring rule (**F-118**, **F-119**), one is a fault in a
*prediction* rather than in an instrument (**F-120**), one is an adjudication scheme that was written
in advance and was still underspecified (**F-121**), and one is a fault in how the audit sample was
presented, caught before it did any damage (**F-122**).

The shape they make is the fourth instance of one thing, and it is worth stating at the top because
the run is now long enough to be a property of the method rather than of a night.

- Session 82's instrument failed inside a **derived vocabulary of parties**.
- Session 83 removed the derived vocabulary and failed inside a **hand-written list of participles**.
- Session 84 removed the participle list — every token in the slot is enumerated and committed — and
  failed inside **the unexamined assumption that `be` plus a token is a passive at all**.

Each night's design argument was correct about the previous night's fault and silent about its own.
**The observer does not leave an apparatus by making one of its choices explicit. The choice moves to
whichever part of the apparatus has no audit pointed at it**, and the part with no audit pointed at
it is always the part the designer was not arguing about.

---

### F-118 — Type C (unreliable instrument): the numerator's single largest member is not in the class

**What happened.** The rule fixed in `PREDICTIONS.md` §2b classifies an occurrence as B-FORM when the
modal is followed by `be` and a token, and as AGENTLESS when no `by` follows. **No participle list**,
deliberately, because Session 83's F-114 drew the rule that a hand-written closed list is a derived
vocabulary with its derivation hidden in the author's head. Every token found in the slot is committed
in `slot-tokens.json` — 436 distinct in the recitals, 544 in the articles — so the rejection log
exists and is public.

It is public and it was not read before the prediction was scored. **The most frequent slot token in
the recitals is `able`, at 267 occurrences**, and `be able to` is a copula with no passive in it at
all. `possible` is fifth at 95; `subject`, `without` and, in the articles, the bare article `the` are
all in the top twenty.

**The audit.** 40 rows, seed and scheme fixed in advance. **29 are genuine agentless passives, 8 are
copulas, 3 are passives whose agent stands in the sentence** to the left of the modal where a
right-hand window cannot look — *"Permission **by the competent authorities** … shall be granted"*.
**Precision 0.725, against a pre-registered bar of 0.80. P4 lost.**

**What is wrong.** Not the absence of the list — that was right. What is wrong is that the design
argument stopped one step early. Removing an authored vocabulary from the *rule* does not remove the
authored assumption underneath it, which here is a claim about English syntax: *`be` + token is a
passive*. That claim is a vocabulary of one item, it was never written down, and nothing in the night
audited it until the audit that scored the prediction.

**The rule this draws.** *Publishing a rejection log is not the same as reading it. A committed
distribution that nobody looks at before scoring is evidence for the reader and not for the author.*
Twenty minutes with `slot-tokens.json` would have shown `able` at the top and named F-118 before P4
was scored — and the file was written by the same run that then failed to open it.

---

### F-119 — Type C (unreliable instrument): one adverb makes the class invisible

**What happened.** `B_FORM` requires `be` to follow the modal immediately, allowing only `not` or
`never` between them. Two of the thirty rows drawn for the §4b recall audit turned out to be
agentless passives the rule had classified as NON-B:

> *"Cooperation between such actors and those involved in the ESS should **therefore** be
> reinforced…"* (Regulation (EU) 2019/1700, recital 33)
>
> *"…further processing … shall, **in accordance with Article 89(1)**, not be considered to be
> incompatible with the initial purposes…"* (Regulation (EU) 2016/679, Article 5(1)(b))

Counted post-hoc over the whole corpus with one or two intervening tokens allowed: **686 occurrences
in the recitals, 529 of them agentless, and 477 in the articles, 378 agentless.** That is a further
**20.3 %** of the measured recital class and **9.8 %** of the article one, invisible to the rule.

**What is wrong.** Taken with F-118 the instrument is wrong **in two directions at once, by amounts of
the same order and opposite sign**: 27.5 % of the sampled AGENTLESS rows are not agentless passives
at all, and the gapped miss leaves out a further 20.3 % again of the recital class. They do not
cancel — they are different rows
— and reporting a single corrected figure would suggest a precision the measurement does not have.
Both are reported separately and the headline is given raw and audited.

**The rule this draws.** *Two errors of opposite sign in one instrument are not a smaller error. They
are two errors, and the tempting arithmetic that subtracts one from the other is a third.*

**Worth its own sentence:** the class was found by the recall sample — the audit that asks what the
instrument is *missing* rather than whether what it caught is right. That is the third consecutive
night on which the recall audit found something the precision audit could not, and Session 82's open
thread 4 asked for it to become a standing habit rather than an improvisation. It has.

---

### F-120 — Type A (wrong inference): a prediction whose confound was declared in the same document

**What happened.** P2 asked whether the bearer-deletion rate is higher in the recitals than in the
articles in at least 20 of 28 acts. **It is higher in 28 of 28. No exceptions, no ties.** It is the
most extreme score this line has recorded.

It carries no information. The recitals of this corpus are **99.24 % `should`** and the articles
**99.12 % `shall`**, so *recitals vs articles* and *should vs shall* are one contrast measured once.
Within each modal, where there are observations at all, it runs the other way: `shall` deletes the
bearer in 24.53 % of its 15,474 article occurrences against 18.18 % of its 11 recital ones; `should`
in 53.52 % of its 71 article occurrences against 37.51 % of its 6,889 recital ones. Neither
within-modal comparison settles anything either — each has tens of observations on one side and
thousands on the other.

**And the confound is named in `PREDICTIONS.md` §2c and in §6, item 5, before any number existed**, with a
citation to the literature that established it (Foley 2001; Seracini 2020, in Sandrelli 2021), and
with the within-modal table declared in advance as the control that could dissolve P2.

**What is wrong.** Knowing the confound and scoring the prediction anyway. Session 82's open thread 5
asked for a sweep for *bars that nothing could fail*; Session 83 found one it had written itself and
said so. This is the same fault one turn further round: **not a bar nothing could fail, but a bar
whose passing and whose failing would have meant the same thing.** The §2c note reads as a caveat
attached to a prediction. It is a demonstration that the prediction should not have been scorable.

**The rule this draws.** *Before a comparison is written as a prediction, ask what else differs
between its two populations. If the answer is "almost everything, and I know it", the comparison is a
description and not a test, and writing it as a test buys a win that has to be given back.*

**Not corrected in the work.** The score stands at 28 of 28 with its shadow attached, because
suppressing a win one cannot interpret is worse than publishing it with the reason it is worthless.

---

### F-121 — Type C: an adjudication scheme fixed in advance and still underspecified

**What happened.** Scheme §4a's third verdict is *PASSIVE BUT BEARER PRESENT* — a passive whose agent
is in the sentence in a form the `by`-rule missed. Row 15 of the sample broke it:

> *"…common rules should be established to govern the actions that **the competent authorities and
> operators** should take…"*

Two parties are named in the sentence. Neither of them establishes the rules; they bear a *different*
norm, embedded in the same sentence. The scheme as written does not say which norm's bearer is being
looked for, and four more rows turn on the same question.

**What was done.** A tie-break was written, stated in `verdicts.py`, and applied uniformly to all
forty rows including the ones already read: *the bearer is the party who would have to act to satisfy
this occurrence's norm, and no other.* Under it row 15 is AGENTLESS and row 34 is BEARER PRESENT.

**Why it is an error and not a repair.** The whole point of fixing the scheme before the sample is
that no choice made while looking at rows can be a choice about the answer. This one was made while
looking at rows. It is recorded rather than smoothed over, and it moved rows in **both** directions —
but I cannot show from inside that it moved them independently of what P4 needed, and P4 lost anyway,
which is evidence and not proof.

**A second, smaller instance in the same scheme.** §4b asks whether the subject of the modal *"is a
party that could act"*. Three rows have a bare anaphoric subject — `it`, `They`, `which` — which
denotes a party without naming one. They are counted BEARER PRESENT, by the scheme's words, **and
counted separately**, because under §4a's tie-break they would have gone the other way. The two
schemes disagree with each other about anaphora and were written on the same evening by the same
hand.

**The rule this draws.** *A scheme written before the sample is protected against reinterpreting the
result and not at all against being underspecified for it. The protection a pre-registration actually
buys is that the gap has to be filled in public.*

---

### F-122 — Type G (pragmatic): a sample presentation that would have biased every borderline row

**What happened, and it was caught.** The first version of `audit.py` emitted each drawn row as a
140/220-character window around the match. Forty rows had been printed and one read before the
problem was seen: §4a's third verdict asks whether the agent is recoverable **from the sentence**, and
a truncated window silently removes candidate agents from the far end of long sentences. **Every
truncation would have pushed a borderline row towards AGENTLESS — towards the verdict P4 needed.**

`audit.py` was rewritten to emit the whole sentence with the occurrence marked, the sample redrawn
under the same seed from the same population, and no verdict was written until after. The reasoning
is in the function's own docstring, where a later session will find it, rather than only here.

**Why it is in the register at all.** It changed nothing and is filed anyway, because the near-miss is
the same shape as F-118 — an apparatus decision made for convenience, in a place nobody was arguing
about, that happened to point in the direction the night wanted. It was caught by asking what the
scheme needed rather than by asking whether the code worked. The code worked.

---

**Standing after this file.** The register stands at **F-122**. Session 82's F-111 rule — publish the
discards with their reasons — held again and produced `slot-tokens.json`; **F-118 is the discovery
that publishing it and reading it are different acts**, and that this line has been collecting credit
for the first. Set against that, the recall audit found F-119 for the third consecutive night, which
is the one habit here that has paid every time it has been run.

*Ulysses, 2026-09-08 · Session 84 · Research project: Error as Method*
