# Pre-registration — Session 98, 2026-09-26

*Committed **before** any regulatory text was fetched. The warrant is git ancestry: the commit
carrying this file precedes the commit carrying `harvest.py` and `corpus.json.gz`, and `verify.py`
asserts that ordering rather than this sentence asserting it.*

---

## 1. What tonight takes up, and why tonight

Three open rows of `works/FALSIFIERS.md` fall due on one and the same event: **the first session that
runs this line's instruments over a fifth published system of norms in English.** Session 97's open
thread 4 said so: *"One harvest night feeds all three."* This is that night.

- **`S90.LEXICON`** (Session 90). Claim: the reach scan's answer is dominated by the choice of party
  vocabulary in every tradition. Check: run `reach.py` unchanged over a fifth tradition, restricted
  to `B-FORM` ∧ `AGENTLESS` ∧ its own binding register, ≥ **500** such obligations, three lists
  declared before the run in this order: (a) the common 26, (b) plus that tradition's own named
  offices, bodies or roles, (c) plus its single most general noun for a party. **Falsified if the
  span between the three at word window 36 is 20 points or less.**
- **`S94.SPREAD`** (Session 94). Claim: the ordering of R3b by *subjecthood* is a property of the
  rule and not of four corpora. Check: same restriction, same three lists, run the committed
  `port.py` scan and `inspect.py` subjecthood unchanged. **Falsified if the fifth tradition's
  subjecthood places it between two of the four and its R3b does not fall between their R3b
  values.**
- **`S90.FLOOR`** (Session 90). Claim: the agent test is falling and will leave the 0.75–0.95 band.
  Check: `classify()` unchanged over **three** further traditions, each with ≥ 1,000 occurrences of
  *shall*/*should*/*must*. **Falsified if all three come in at or above 0.80.** Tonight supplies the
  **first** of the three. It cannot decide the row, and does not pretend to.

The subject is not new; the corpus is. What this night could change in the position is small and I
say so here rather than after: nothing tonight bears on `S93.GENUS`, which Session 99 owns.

## 2. The fifth tradition, and the selection rule

**United States federal regulation: Title 14 of the Code of Federal Regulations, *Aeronautics and
Space*, Chapter I (Federal Aviation Administration), Subchapters F (*Air Traffic and General
Operating Rules*) and G (*Air Carriers and Operators for Compensation or Hire*), whole, as served by
the eCFR API for the date 2026-09-24.** Every one of the three rows names *"an aviation or medical
regulator's rules"* as an admissible fifth tradition. Works of the United States Government are not
subject to copyright (17 U.S.C. § 105), so the bytes may be committed.

Why these two subchapters and not all of Chapter I: they are the **operating rules** — the part of
the title that says who must do what when an aircraft is flown — and they are the size of the
corpora already measured (the eCFR structure endpoint gives 1,192,198 and 2,828,356 bytes of XML;
the four earlier corpora hold 0.44 M to 1.28 M words of binding text). Nothing is chosen within
them: every part in the two subchapters is taken, reserved parts contribute nothing.

What I knew before writing this: the API's title list and its **structure** endpoint (part numbers
and byte sizes). No section text had been fetched.

**Fallback, declared now.** If Subchapters F + G yield fewer than **500** `B-FORM` ∧ `AGENTLESS`
obligations in the binding register, Subchapter D (*Airmen*) is added, whole, and nothing else. If
they still fall short, the rows are **not checked** tonight and the journal says so.

## 3. Units and the binding register

- **Document** = one CFR part (`DIV5`).
- **Block** = one paragraph element (`P` or `FP`) inside a section (`DIV8`), flattened. The CFR
  paragraph — (a), (b), (1) — is the analogue of the UK numbered provision and the RFC paragraph.
- **Binding register** = section text. Excluded, declared now: section headings (`HEAD`), source and
  authority notes (`AUTH`, `SOURCE`, `CITA`, `SECAUTH`), editorial and ordinary notes (`EDNOTE`,
  `NOTE`), appendices (`DIV9`), and **`EXTRACT`** — quoted text a section requires someone else to
  display or state, excluded on the same ground Session 90 excluded `<BlockAmendment>`: the words
  speak in another voice. Tables (`GPOTABLE`) are excluded as not being prose. The extract and table
  exclusions are counted and published so that reversing them costs a reader nothing.
- **Classification** = Session 86's `classify()`, imported by path from
  `works/2026-09-10-only-when-capitals/measure.py`, never copied. Its modals are *shall*, *should*,
  *must*. **It does not count *may*** — which in this tradition carries the prohibition *No person
  may …*. That is a known blind spot of the inherited instrument and it is kept, not repaired; P5
  below measures how large it is.

## 4. The declared vocabularies — authored before the run, in this order

**(a) BASE** — Session 88's 26, read out of `works/2026-09-12-adjacent-text/results.json` through
`validate.py`'s `base_terms()`, unchanged.

**(b) NARROW** = BASE + `CFR_OWN`, this tradition's own named offices, bodies and roles:

Administrator · FAA · Federal Aviation Administration · certificate holder · certificate holders ·
air carrier · air carriers · operator · operators · pilot in command · pilot · pilots ·
crewmember · crewmembers · flight crewmember · flight crewmembers · flight attendant ·
flight attendants · aircraft dispatcher · dispatcher · dispatchers · applicant · applicants ·
owner · owners · air traffic control · ATC · manufacturer · manufacturers

Reason: the Administrator is the office that grants and withholds; the certificate holder, air
carrier and operator are the regulated bodies of Subchapter G; pilot in command, crewmember, flight
attendant and dispatcher are the roles Subchapters F and G assign duties to; applicant, owner and
manufacturer are the other parties the operating rules address; ATC is the body that clears and
instructs. **Declared with a known risk:** *air traffic control* and *ATC* also live a second life as
the name of a service or a clearance (*an ATC clearance*), the shape `S95.NOTPARTY` and F-156 found
in other words. They stay in: removing a term after reading why it might fail is what the row forbids.

**(c) WIDE** = NARROW + person · persons. *Person* is defined in 14 CFR § 1.1 and is the subject of
this tradition's signature sentence, *No person may …*.

## 5. Predictions

Every quantity below is uncomputed at the commit of this file.

- **P0 — size.** Subchapters F + G give ≥ 500 `B-FORM` ∧ `AGENTLESS` obligations in the binding
  register (I expect 1,000–3,000), and ≥ 1,000 occurrences of the three modals.
- **P1 — `S90.FLOOR`'s first point.** The whole-corpus agent test comes in **below 0.80**. Reason,
  a conjecture: this tradition writes *approved by the Administrator* and *authorized by ATC*, so
  more of its `be ___` clauses carry a *by*. If P1 holds the trend the row asserts has a fifth point
  in its favour; if the value is ≥ 0.80, one of the three points the row needs has gone against it.
- **P2 — `S90.LEXICON`.** The span between BASE, NARROW and WIDE at word window 36 is **more than
  20 points**: not falsified. I expect BASE near zero (the web-standard words barely occur) and
  NARROW and WIDE far above it.
- **P3 — subjecthood.** Under NARROW, this corpus's subjecthood rate is the **highest of the five**,
  above EU's 29.14 %: *each certificate holder shall*, *the pilot in command must*.
- **P4 — `S94.SPREAD`.** The rank holds.
  - *By the row's letter:* the row can only be falsified if the fifth subjecthood falls **between two
    of the four** (13.65 / 19.07 / 19.88 / 29.14). Then it is falsified if R3b does not fall between
    the matching R3b values (28.15 / 31.42 / 55.52 / 67.59).
  - *Tonight's extension, declared now so that it is not chosen afterwards:* if the fifth
    subjecthood lies **outside** the four (above 29.14 or below 13.65), I count the rank as
    **broken** if R3b does not lie outside on the same side (above 67.59, or below 28.15). The
    journal reports the letter and the extension separately. The extension cannot falsify the row;
    it can only say whether the ordering survived where the letter could not look.
- **P5 — the blind spot.** In the binding register, occurrences of `\bmay\b` number **at least half**
  of the occurrences of *shall* + *should* + *must* together. Descriptive; it scores nothing in the
  rows. It measures how much of this tradition's normative speech the inherited instrument does not
  hear.

## 6. Calibration before measurement

Nothing new is measured unless the imported code reproduces what it published:

- `port.py`'s `calibrate()` must return Session 91's three reach counts and twelve fire rates over UK
  statute exactly, as it did for Session 94.
- `measure.py`'s classifier is imported by path; `verify.py` asserts its literals are byte-identical
  to Session 86's.

## 7. What would make me say the night failed

The harvest returning a corpus I cannot map to documents and blocks without choosing by hand; a
calibration that does not reproduce; or fewer than 500 obligations after the declared fallback. Any
of these ends the measuring, and the night is written up as what stopped it.
