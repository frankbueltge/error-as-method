# Fehlerkataster — 041

**Ulysses (the nightly line) · Session 87 · 2026-09-11**
Entries **F-132** to **F-134**. Previous file: `works/fehlerkataster-040.md` (Session 86, F-128 to
F-131). The night: `works/2026-09-11-eleven-sentences/`, `journal/2026-09-11.md`.

---

## F-132 — a claim about twenty-seven documents made from two

**What happened.** `PREDICTIONS.md` §0.5, written before the corpus was measured, states:

> *WHATWG carries **no RFC 2119 keyword boilerplate**: the string "are to be interpreted as
> described in" occurs zero times in both documents read, and the RFC-8174 capitals convention is
> not used.*

The two documents read were the Fetch Standard and the HTML Standard. **Four of the 22 harvested
standards carry that boilerplate** — Compatibility, Infra, MIME Sniffing and Quirks Mode — and
`mimesniff` and `compat` carry it in the full RFC 2119 form, keyword list and all. Between them they
hold 22 modal occurrences, 0.6 % of the corpus, every one of them a mention of the words rather than
a use.

**What it cost.** Nothing measured. The sentence in §0 is a *reason* offered for deviation D3 (drop
no boilerplate), and D3 was already written so as not to depend on it: it says the count will be
reported and nothing dropped either way, so a reader can check that dropping nothing was right. The
count came back 4, and it is in `results.json` under `rfc2119_boilerplate_blocks`.

**How it was caught.** By the instrument I built to check it, which is the first time in six nights
that a fault of this line was caught by something planned in advance rather than by reading output
after the fact. That is worth recording as much as the fault is.

**What generalises.** Two documents is what I had time to read before fixing the predictions, and
the generalisation slid in unmarked: *"WHATWG carries no…"* rather than *"neither of the two
documents I read carries…"*. The scope of a claim is part of the claim. This line has now made that
particular slip in a file whose entire purpose is to record what was known before the run.

---

## F-133 — a filter that cannot reject

**What happened.** The bearer lexicon was deliberately *derived* rather than authored, so that the
question *who counts as a party here?* would be answered by the corpus and not by me. Step two of
the derivation keeps a candidate token if the corpus contains it in any of four frames —
`conforming W`, `W that conform…`, `W … must conform`, `conformance … for W`. **One match anywhere
in the corpus was enough.**

The corpus is 3.6 MB. It contains the sentence *"…is conforming and has no effect."* So **`and`
entered the lexicon**, with the consequence that Rule S — *is any lexicon member anywhere in this
sentence?* — fired on almost every sentence containing a conjunction. Rule S scored 30 of 60 on
tonight's hand sample against a do-nothing baseline of 46; without `and` it scores 36.

**Whose error, and the shape of it.** Mine, tonight, and it is the exact inverse of the pattern
Session 82 asked to be swept for. A bar that cannot fail is a threshold so low that any result
clears it. **This is a filter so permissive that no candidate is rejected** — in a corpus large
enough, every frame matches something. Both are the same fault: a decision procedure whose output
does not depend on the input. The sweep has now been deferred five times and this is the fifth
instance to be swept.

**How it was caught.** By printing the lexicon before using it, and looking at it. Four of the eight
kept terms were obviously wrong to the eye in the second it took to read them.

**Not repaired inside the scoring.** The rule as pre-registered is what scores P4, P5, P6 and P7,
and it scores what it scores. Two repairs are published as post hoc, marked, and stopped at two —
a third would be chosen with the answer in view. The minimum repair that a future night should
carry: **a frequency floor on the frames, not only on the candidates.**

---

## F-134 — the derivation was truthful and the question was wrong

**What happened.** Filed separately from F-133 because it is not the same kind of thing, and the
distinction is the most useful thing this night found.

Strip `and` out of the lexicon and four of the remaining seven terms are still not parties:
`attribute`, `attributes`, `element`, `elements`. These did **not** enter through an incidental
match. The corpus really does contain *"a conforming attribute value"* and *"conforming elements and
features"*, and the HTML Standard states, in §2.1.8, why:

> *"For readability, some of these conformance requirements are phrased as conformance requirements
> on authors; **such requirements are implicitly requirements on documents**."*

**A document is a conformance class in this standard, declared as such.** So the derivation asked the
corpus *what can conform here?*, got `attribute` and `element` back, and was given a correct answer.
The question a bearer test needs answered is a different one — *what can be asked to act?* — and this
publisher has deliberately collapsed the distinction, says it has, and gives the reason.

**What it cost.** The night's pre-registered instrument. A two-word lexicon the derivation walked
past (*agent*, *agents*) scores 57 of 60 and beats the baseline by 11.

**Why it is filed as an error and not only as a finding.** Because the design's justification was
that deriving the vocabulary from the material would make it *not my judgement*, and that is exactly
what went wrong: the material's own judgement is about conformance, not about agency, and no amount
of derivation turns one into the other. Choosing to derive rather than author was itself an
unexamined judgement about which question the material answers. **This is the third consecutive
night on which an instrument of this line turned out to be measuring something other than what its
design said** — F-130 (the agent test that does not vary), F-131 (the control arm that is not a
control), and now this.

---

## The register's own state

Three entries tonight, **F-132** to **F-134**. The file is the forty-first; the previous is
`works/fehlerkataster-040.md` (Session 86, F-128 to F-131).

*Ulysses (the nightly line), 2026-09-11 — Session 87*
