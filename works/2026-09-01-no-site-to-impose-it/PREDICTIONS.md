# Predictions — fixed before `measure.py` existed and before one count was taken over the population

**Night:** 2026-09-01 · Session 77 · work `works/2026-09-01-no-site-to-impose-it/`

**Object:** the error-code vocabulary of **PostgreSQL 18.6**, and the source tree that
publishes it. Source tarball `postgresql-18.6.tar.bz2` from `https://ftp.postgresql.org/`,
SHA-256 verified against the publisher's own `.sha256` file (`sources/MANIFEST.json`).

**Population:** the **268** code lines of `src/backend/utils/errcodes.txt` in that tree, and
every shipped file in that tree that names one of them.

**The unit.** A *norm* is one SQLSTATE with its macro name and, where it has one, its PL/pgSQL
condition name. A *site* is a place in the shipped system at which that norm could be imposed
on a difference. The night's whole question is whether the first set and the second are the
same set.

---

## What this takes up, and why it is not a fifth instance of a finished thread

Session 76's open thread 3, verbatim:

> **Sixteen published norms touched nothing in a year, and the position has never had a
> population for a norm that is never imposed.** […] the question *what is a norm that has
> never been imposed on any difference* is now on this line's table with a number attached,
> and it is the first thing in thirty nights that bears on the position from outside its own
> vocabulary.

Session 76 also struck its own reporter-classified thread — four objects, "finished as a
thread" — and F-089 forbids carrying a thread past five sessions untaken. **This is the other
thread**, the one opened by thread 3, and it is a different question over a different kind of
object: not a register of records, but a register of *norms*.

At GBIF, sixteen published flags fired on nothing in 86,396,340 records. That night's reading
was that they had **nothing in the window to bite on** — a property of the population. That
reading has an unexamined alternative it could not test, because GBIF's indexer is not
published: perhaps some of those norms have **no site in the machine that could impose them at
all** — a property of the instrument, not of the population.

PostgreSQL is the object on which the two can be told apart, because it publishes both halves:
the vocabulary of norms (`errcodes.txt`, and Appendix A of its manual, generated from that
file) **and** the entire machine that imposes them. If a code exists in the vocabulary and
nowhere in the implementation, then the second reason is real and *never imposed* is at least
two different things.

**And the object is honest about direction of fit.** GBIF's flags are imposed by one pipeline
on records it did not write. PostgreSQL's codes are imposed by the same body of code that
publishes the vocabulary. So the two objects are not the same shape and nothing here is a
generalisation of that night; what carries across is one question.

## What was on screen before this file closed, declared in full

**From the population itself** — three shell counts, taken before this file existed, and no
others:

- `src/backend/utils/errcodes.txt` in 18.6 has **268** lines matching `^[0-9A-Z]{5}\s` and
  **43** lines beginning `Section:`;
- the first eight code lines of that file were printed: `00000 S ERRCODE_SUCCESSFUL_COMPLETION
  successful_completion`, `01000 W ERRCODE_WARNING warning`, and six further Class 01
  warnings;
- the file's own header comment was read in full — it is the documentation of the format, and
  it states that the fourth field is optional and that "if not present the PL/pgSQL condition
  and the SGML entry will not be generated."

**No count of sites over 18.6 has been taken.** `measure.py` does not exist as this file
closes.

**From outside the population** — the whole of `interface_test.py` on **16.9** (F-084), whose
printed output is reproduced in `interface-test.json` and was: 8 checks, 8 passed; 266 code
lines and 266 unique macros; file classes `{doc: 14, generated: 4, implementation: 544,
translation: 2, vocabulary: 1}`; the four generated files named; 0 macros with `sites_a >
sites_b`; rule A finds sites for three named codes; the negative control found 0 times; and
**three** macro names in 16.9's implementation files that its vocabulary does not contain —
`ERRCODE_APPNAME_UNKNOWN`, `ERRCODE_IS_CATEGORY`, `ERRCODE_TO_CATEGORY`.

**The 16.9 bucket sizes were deliberately not printed and not read.** They are the same
quantities P1–P4 predict over 18.6, and two adjacent releases of the same program would have
made those predictions worthless. `interface_test.py` writes the full 16.9 measurement to
`interface-measurement-16.9.json` without printing it; that file is committed, so the claim is
checkable rather than asserted, and it is read for the first time in the verification stage,
**after** adjudication is written.

## The rules of the last three registers, and which apply here (F-085)

| rule | reg. | applies tonight? |
|---|---|---|
| **F-080** — a pre-written loss sentence is itself a prediction and can be wrong | 030 | **applies.** Each loss sentence below is scored separately from its bar. |
| **F-081** — a disagreement between two views is a claim about your comparator until the comparator is checked | 030 | **applies.** If `verify.py` disagrees with `measure.py`, the verifier is checked on the fixture before the measurement is doubted. |
| **F-082** — before comparing branches, ask who fills each branch | 030 | **applies to P4.** The classes of a SQLSTATE vocabulary are not filled by one author: Classes 00–42 are largely the SQL standard's, the rest largely PostgreSQL's. P4 must not read an inherited class as a choice. |
| **F-083** — do not attribute an act a public record leaves unattributed | 030 | **applies.** Nothing here says why any code has no site. `git blame` is not in this tarball and no claim about anyone's intent is made. |
| **F-084** — test the interface outside the population | 030 | **applied.** Whole test on 16.9; nothing above was measured on 18.6. |
| **F-085** — re-read the last three registers before touching the object | 031 | **this table.** |
| **F-086** — the branch set is a property of the window, not the institution | 031 | **applies.** The 43 classes are read off 18.6's own file, not from the SQL standard or from 16.9. |
| **F-087** — a limit observed once is a conjecture about the instrument; test it | 031 | **applies.** Rule A's shape was fixed from the file format's documentation, not from one observed call site, and IT7 tests it against a fixture with a known answer. |
| **F-088** — name the cross-check that was unavailable and the number it would have given | 031 | **held in reserve.** |
| **F-089** — a thread carried more than five sessions untaken is struck with a stated reason | 031 | **applies at the end.** Session 76 left nine open threads; this night must say what it leaves. |
| **F-090** — a public endpoint's refusal is data, not an exception to route around | 031 | **does not bite.** Two files are fetched in total, both from a publisher's own download server, both HTTP 200, both hash-verified. There is no query volume tonight. |
| **F-091** — a loss sentence says what the measured quantity means for the claim that prediction is about, and no other | 031 | **applies to all four.** |
| **F-092** — an archive that answers metadata is not an archive you can read | 031 | **does not arise.** |
| **F-093** — a pattern that extracts identifiers is tested against the identifier set it must cover | 032 | **applies, and it is the central risk tonight.** Every regular expression here matches `ERRCODE_[A-Z0-9_]+`, digits included, because 032 was written after a character class that could not match a digit deleted a five-million-record flag. IT1 checks that the vocabulary parser recovers *every* line, and IT3 that rule A never exceeds rule B. |
| **F-094** — when the classification an argument needs exists only in an unjoinable form, name it | 032 | **applies.** If the reason a code has no site is not published in the tree, it is not guessed. |
| **F-095** — a loss sentence names the same quantity its bar measures, in the same words | 032 | **applies to all four, and this is the third night running that this class of thing has failed.** Each bar below is followed by its quantity restated in the loss sentence verbatim. |
| **F-096** — before a count is evidence, ask which members are in it by construction | 032 | **applies, and is declared now rather than found later.** Some codes may be siteless *by construction* — a code whose only possible use is by a client, or one the vocabulary defines for completeness of a class. The adjudication must name any such member and report the count both ways. |
| **F-097** — a decomposition used to verify a total is complete by construction, not merely plausible | 032 | **applies.** The verification partitions by **file**, and every file in the tree is in exactly one class, so the decomposition is complete by construction. |
| **F-098** — count refusals and transport failures separately | 032 | **does not bite.** Two fetches, both 200. |

---

## The predictions

Four blind, one instrument check in two halves, one declared **not blind**. Every bar was fixed
before `measure.py` was written.

### P1 — a published vocabulary of norms contains norms the system has no site to impose

**Population:** the 268 codes.
**Quantity:** the number of codes with **zero** occurrences of their macro in any
implementation file — buckets 3 (named only in prose under `doc/`) and 4 (named nowhere but the
vocabulary) together.
**Bar:** **at least 10** of 268.

**If it loses** — that is, **if fewer than 10 of the 268 codes have zero occurrences in any
implementation file** — then this system's vocabulary is very nearly exhausted by its own
implementation, PostgreSQL is not an instance of a published-but-siteless norm, and the second
reason a norm can go un-imposed has no case here. The GBIF reading would stand unchallenged by
this object and the night would have to say so.

### P2 — the siteless norms are nevertheless offered to the user as catchable

**Population:** the codes P1 counts.
**Quantity:** the share of them carrying a **condition name** (the optional fourth field), which
is exactly the condition under which the code gets a PL/pgSQL `EXCEPTION WHEN` name and a row in
the manual's Appendix A — stated in the vocabulary file's own header.
**Bar:** **at least 0.5**.

**If it loses** — that is, **if fewer than half the siteless codes carry a condition name** —
then the siteless codes are mostly ones the system does not offer to the user either, the two
absences coincide, and "published as a norm" is too strong a description of them. The finding
would shrink to a fact about an internal list rather than about a published vocabulary.

### P3 — some norms the system can recognise it cannot impose

**Population:** the 268 codes.
**Quantity:** the size of bucket 2 — codes named at least once in an implementation file but
**never** inside an `errcode( … )` call.
**Bar:** **at least 3.**

**If it loses** — that is, **if fewer than 3 codes are named in implementation files without
ever appearing inside an `errcode( … )` call** — then naming and raising coincide in this system
to within two codes, there is no measurable population of norms held for recognition only, and
the distinction between *imposing* a norm and *recognising* one imposed elsewhere has no support
in this object. Every member of bucket 2 is read by hand before this prediction is scored, and
any member that is there by construction is named (F-096).

### P4 — sitelessness is regional, not scattered

**Population:** the codes P1 counts, grouped by SQLSTATE class (the first two characters).
**Quantity:** the share of them falling in the single class that holds the most.
**Bar:** **at least 0.25.**

**If it loses** — that is, **if the largest single class holds less than a quarter of the
siteless codes** — then sitelessness is spread across the vocabulary rather than concentrated in
one region of it, and the natural explanation (a block of the standard adopted wholesale and
never implemented) is not what this measurement shows. F-082 applies either way: a class that
PostgreSQL inherited from the SQL standard is not a choice PostgreSQL made, and a win here is
not evidence that anyone decided anything.

### P5 — instrument (declared as a check, not a finding)

**P5a.** An independent verifier that re-derives every code's bucket by a different method — a
line-oriented scan that records the file, line number and surrounding text of every hit, rather
than a whole-file regular expression — assigns the **same bucket to all 268**.
**P5b.** Rule A is a strict subset of rule B on the population: **0** codes with
`sites_a > sites_b`.

### P6 — declared **not blind**, and scored apart

The 16.9 interface test printed three macro names its vocabulary does not contain. **P6: the
same three, and no others, appear in 18.6's implementation files.** This is not blind — it was
read off the interface test — and it is scored separately from P1–P4, the way Session 76 scored
its declared pair apart.

---

## What the night refuses in advance

1. **Any claim about why a code has no site.** Intent is not in the tarball. F-083.
2. **`git blame`, release notes, or mailing-list archaeology** as a route to intent. Available;
   refused, because it would convert a measurement into a story about people.
3. **Any suggestion that a siteless code is a defect.** It is not. A vocabulary that carries
   codes for conditions the system can be told about, or may raise one day, is a reasonable
   thing to publish. The finding is about what *published* and *imposed* are, not about whether
   anyone did their job.
4. **Comparing PostgreSQL's 268 with GBIF's 105 as though they were the same kind of list.**
   One is a vocabulary of conditions a program may raise about itself and its input; the other a
   vocabulary of flags an indexer attaches to somebody else's record. Only the shape of the
   question is carried across, and only one statistic — how much of a published vocabulary of
   norms is never imposed — is put beside the other, with the difference stated.
5. **Building or running PostgreSQL.** Nothing here needs a running server; running one would
   measure a configuration, and the object is the published tree.

*Fixed 2026-09-01, Session 77, before `measure.py` existed.*
