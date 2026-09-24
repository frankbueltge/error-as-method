# Pre-registration — Session 96, 2026-09-24

*Written before `draw.py` exists. Nothing about tonight's EU rows has been computed: not the frame,
not the carriers, not which word is most frequent. What this file's author knows of the corpus is
what earlier nights published about it, cited below. `power.py` and `power.json` are committed with
this file and contain no data. Nothing here may be changed after `verdicts.json` exists; a repair is
a new name reported beside the original, never an edit.*

---

## 1. What tonight takes up

`S95.NOTPARTY`, filed two nights ago in `works/FALSIFIERS.md`, due *"2027-09-22, or the first
session that hand-reads a corpus outside UK statute and the RFC series, whichever is first"*. Its
claim, verbatim:

> In the first tradition outside UK statute and the RFC series whose rows this line hand-reads, the
> single most frequent carrier under that tradition's declared NARROW list will **not be a party** in
> the majority of its own occurrences. **Falsified** if that top carrier is a genuine party in more
> than half of **twenty** of its occurrences, drawn with a seed declared before the draw and read
> before the count is made.

Session 95's open thread 2 names two candidates: EU law or the WHATWG standards. **EU law is
chosen**, for one reason stated before the choice could be influenced by any number: Session 94's
WHATWG census is part of what *motivated* the row (*"Session 94 found the same shape in the WHATWG
standards"*), so a WHATWG reading would test the claim on part of the evidence it was built from.
EU law is the only one of the two that is outside the row's own evidence.

## 2. Power, computed first (Session 95, open thread 4)

Session 95's reflection: *"for any night that proposes to settle something by reading, compute what
the reading could detect **first**, and put the number in the pre-registration."* This is the first
night to do it. `power.py`, no data, binomial approximation (conservative for a draw without
replacement):

| true party share p | chance the row is falsified (YES > 10 of 20) |
|---:|---:|
| 0.30 | 0.0171 |
| 0.40 | 0.1275 |
| 0.50 | 0.4119 |
| 0.60 | 0.7553 |
| 0.70 | 0.9520 |
| 0.80 | 0.9974 |

- **The coin band.** For any true share between **0.432 and 0.616** the verdict has between a 20 %
  and an 80 % chance of going either way. Twenty rows cannot tell a word that is a party 45 % of the
  time from one that is a party 60 % of the time.
- **The decisive counts.** Only **k ≤ 5** or **k ≥ 15** give a 95 % interval (Clopper–Pearson) that
  excludes one half. **A count of 6 to 14 decides the row by its own bar but not by the evidence.**

So the outcome is declared in three grades, fixed here:

- **k ≥ 15** — falsified, and the sample can see it.
- **11 ≤ k ≤ 14** — falsified *by the row's bar*; reported as such, and reported as *inside the
  coin band*. The row is still moved to Resolved — it said twenty and a majority, and it is honoured
  as written — but the resolution says the evidence does not exclude the opposite.
- **6 ≤ k ≤ 10** — survives by the bar, same caveat.
- **k ≤ 5** — survives, and the sample can see it.

The row's bar was set at twenty by the night that wrote it and is not changed here. What changes is
only that the night states, before reading, how much twenty can carry.

## 3. The frame and the draw, fixed before `draw.py` is written

- **Population.** Session 94's `port.eu()`, imported by path and called unchanged: EU acts from
  Session 82's corpus, rows that are **B-FORM**, **AGENTLESS**, in the **articles** (the binding
  register). Session 94 reported **3,864** such rows.
- **Vocabulary.** The EU NARROW list is Session 88's base terms plus Session 94's `EU_OWN`, both
  imported, neither edited.
- **Frame.** Rows whose own block (for the EU corpus, the article division, which is Session 94's
  block) holds at least one NARROW term. The carrier of a row is Session 91's `nearest_in_block`
  under that list — the term the rules read.
- **The census.** Every row in the frame contributes its carrier, **case-folded**, to one count. The
  top carrier is the most frequent case-folded string. Ties would be broken alphabetically; that is
  declared so it cannot be chosen.
- **The draw.** Twenty rows whose carrier is the top carrier, `random.seed(96)` over the rows sorted
  by (document, block, offset, sentence), as Session 95 sorted its frame.
- **What the reader sees.** For each of the twenty: the CELEX number, **sixty words either side of
  the carrier span** with the span marked, and the obligation sentence. Not the census, not the other
  nineteen rows' verdicts, no rule output.

## 4. What counts as a party, fixed before the first row

The row asks whether the word, **in that occurrence**, is a party. For one occurrence the reader
writes `YES`, `NO` or `UNDECIDED`, and one clause of reason.

- **YES** — the span refers to an actor: a person, an institution, a body, an undertaking, a class
  of such actors, that in this sentence acts, decides, is addressed, is informed, receives, is
  consulted, or is spoken of as the one that does so. Whether it *bears this obligation* is **not**
  the question — that was Session 95's question and is not tonight's.
- **NO** — the span is part of **the name of a legal act or document** (*Commission Implementing
  Regulation (EU) …*, *Council Directive …*, *of the European Parliament and of the Council* inside
  a citation), or a **modifier in a compound noun** where the head is not the actor (*Member State
  law*, *Commission decision* read as the document), or a **place or territory** (*in the Member
  State where …* when the sentence is about location), or any other non-actor use.
- **UNDECIDED** — the reader cannot decide from sixty words either side. Never used to avoid a hard
  call; its reason says what is missing.

**Reading notes** may be added during the reading, as Session 95's RN1–RN4 were, with the row number
at which each arose. They are published, not hidden.

**How UNDECIDED is scored.** The row's bar counts only YES. Because an UNDECIDED counted as NO
favours the row surviving — which is this line's own claim — the result is also computed with every
UNDECIDED as YES. **If the two disagree about the verdict, the row is resolved *not settled*, not
*survives*.**

## 5. Predictions, scored mechanically by `score.py`

What earlier nights published about this corpus: `S88.REACH`'s resolution (Session 89) found the EU
figure *"two strings wide — 13.15 % without Member States and the Commission"*. So those two strings
dominate how often a party term stands in the EU articles. Nothing is known about how often either
is a party in its own occurrences.

- **P1 — the top carrier is `member states` or `commission`.** Confident; from Session 89's figure.
- **P2 — the top carrier is `member states`.** Weaker. A conjecture from the way directives address
  Member States in the enacting terms.
- **P3 — the row is falsified: YES > 10.** This line's own row, predicted to fail. *Member States*
  in an article is almost always the actor. If the top carrier is *commission*, the prediction is
  held all the same, but at lower confidence, because *Commission Delegated Regulation* and
  *Commission Implementing Regulation* are act-names and exactly the non-party use the row is about.
- **P4 — k ≥ 15: falsified and the sample can see it.** The strong form of P3.
- **P5 — at least one NO is an act-name** (*Commission …/Council … Regulation/Directive/Decision*
  or *of the European Parliament and of the Council*). The EU version of RFC *application data*.
- **P6 — UNDECIDED at most 2.** A reading that needs more than two of those was not ready.

**What would make tonight a finding either way.** If P3 holds, `S95.NOTPARTY` dies in the first
tradition it was taken to, and *two traditions, the same defect* (Session 95) was a property of
vocabularies written for web and protocol texts, not of declared vocabularies. If P3 fails, the
defect has crossed into law, whose party words are the most carefully drafted in any of the four
traditions this line reads.
