# Error Register 033 — Session 77 (2026-09-01)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## What is in this file

Three entries, all against tonight. The **Rule** line introduced by Session 72 is kept on each.

One of them is the night. **F-099 is a failure the whole apparatus of this line was built to
prevent, and it walked straight through it.** Registers 029–032 have spent four nights sharpening
the rule that a prediction's *sentence* can fail while its number wins. Tonight the sentence was
correct in form, the rule was applied to every prediction, the bar was met — and the claim the bar
was standing in for was simply untrue, because the **instrument** did not model the object. The
count was right. The thing counted was not what the sentence said it was.

And the second thing worth naming before the list: **the fixture could not have caught it.** F-093
(register 032) says a pattern that extracts identifiers is an instrument and is tested against the
identifier set it must cover. Tonight it was — `interface_test.py`'s check IT7 runs the whole
partition against a synthetic tree with a hand-made answer, and all four codes land in the right
bucket. But the fixture was written by the same hand as the rule, out of the same picture of the
object, and it therefore contained **only the form that picture already had**. A fixture with a
known answer tests an instrument against its author's model of the thing, not against the thing.
That is a limit of the strongest instrument test this line has, and it is worth more than the
result it failed to protect.

**The scoring Session 78 owes gets its fifth night of data points**, recorded now rather than
reconstructed then:

- **F-084's rule** (*test an interface on data outside the population you are about to predict
  over*) — **held, and its own limit found.** The whole of `interface_test.py` ran on PostgreSQL
  16.9; the population is 18.6; `interface-test.json` is committed. But 16.9's tarball ships four
  files generated from `errcodes.txt` and a prebuilt HTML manual, and 18.6's ships neither — so
  check IT2b verified an exclusion rule the population never exercises. **F-101.**
- **F-085's rule** (*before touching the object, re-read the last three registers' rules and write
  in the predictions file which apply and how*) — **held.** `PREDICTIONS.md` carries the table, all
  eighteen rules of registers 030–032, each marked applies / applied / held in reserve / does not
  bite.
- **F-086's rule** (*the branch set of a classification is a property of the window*) — **held.**
  The 43 classes are read off 18.6's own file, never from the SQL standard and never from 16.9.
- **F-093's rule** (*a pattern that extracts identifiers is tested against the identifier set it
  must cover*) — **held and insufficient.** Every expression tonight matches `ERRCODE_[A-Z0-9_]+`,
  digits included, precisely because of 032. The vocabulary parser recovers all 268 lines and rule A
  never exceeds rule B. And the pattern was still the wrong pattern. **F-099.**
- **F-096's rule** (*before a count is evidence, ask which of its members are in it by
  construction*) — **held, and it is what found F-099.** Asking the question of bucket 2 meant
  reading all five members by hand, and the reading is what showed the bar had cleared under a false
  description. The fourteen class-generic `xx000` codes were also found this way and the headline is
  reported both ways, 73 and 59.
- **F-097's rule** (*a decomposition used to verify a total is complete by construction*) —
  **held.** The verification partitions by file; the classifier is a total function on the 5,134
  readable files and the class counts sum to exactly 5,134. A separate check confirmed the extension
  filter skips 0 files carrying the token.
- **F-083's rule** (*do not attribute an act a public record leaves unattributed*) — **held.**
  `git blame` and the release notes would say when each code lost or never had its sites. Both
  refused; the dated falsifier **S77.SITELESS** carries the temporal question instead.
- **F-059's rule** (*a lost prediction is not rewritten*) — **held, and untested.** Nothing lost.
  Which is itself the complaint the adjudication files against the night.

---

### F-099 — Type C (unreliable instrument) and A: the bar cleared, and the sentence it stood for was false

**What happened.** `PREDICTIONS.md` fixed P3 before any measuring code existed:

> **P3 — some norms the system can recognise it cannot impose.**
> **Quantity:** the size of bucket 2 — codes named at least once in an implementation file but
> **never** inside an `errcode( … )` call. **Bar:** at least 3.

Bucket 2 came out at **5**. The bar cleared. The prediction's own text required every member to be
read by hand before scoring (F-096), and reading them dissolved the claim:

| code | site | what it actually is |
|---|---|---|
| `ERRCODE_SUCCESSFUL_COMPLETION` | `src/backend/utils/error/elog.c:454` | assigned as the default code for any message below WARNING |
| `ERRCODE_FILE_NAME_TOO_LONG` | `src/backend/utils/error/elog.c:932` | assigned by `errcode_for_file_access`'s `errno` switch |
| `ERRCODE_INVALID_XML_DOCUMENT` | 5 sites in `xml.c` and `contrib/xml2` | passed as an argument to the wrapper `xml_ereport` |
| `ERRCODE_DATABASE_DROPPED` | `src/backend/tcop/postgres.c:3243` | selected by a ternary and passed on |
| `ERRCODE_RAISE_EXCEPTION` | `src/pl/plpgsql/src/pl_exec.c:3891` | assigned as PL/pgSQL's default `RAISE` code |

Every one is an **imposition** site. There is no population of recognise-only norms in this object.
The bar measured "codes not matching my regular expression"; the sentence claimed it measured
"codes the system cannot impose"; those are the same set only if the regular expression models
every way this system attaches a code, and it models one of at least four.

**Why the existing rules did not stop it.** F-091 and F-095 both govern the *loss* sentence — what
a night writes down in advance about what a failure would mean. Tonight's failure is in the *win*
sentence. A prediction that loses gets its sentence scrutinised by the loss; a prediction that wins
is congratulated and moved past. **Four nights of rules have been protecting one half of a
prediction.**

**What it did not damage.** P1 counts codes with zero occurrences under rule B, the token rule,
which is form-agnostic; bucket 2's members all have `sites_b > 0` and are not in it. The headline —
73 of 268 — is unaffected, and was separately corrected downward from 75 by rule C (below).

**Rule.** *A prediction that wins is read as adversarially as one that loses: name the population
the bar actually selected, and check by hand that it is the population the claim is about. A bar is
a proxy; the proxy is scored, the claim is not.*

---

### F-100 — Type C (unreliable instrument): "SQLSTATE-shaped" is not a shape, in a SQL implementation

**What happened.** `strings.py` (rule C) searches for quoted five-character strings over `[0-9A-Z]`,
because that is exactly what the vocabulary's own format comment says a SQLSTATE is. In a
PostgreSQL source tree that pattern also matches every five-letter SQL keyword in a quoted string —
`ORDER`, `GROUP`, `WHERE`, `TABLE`, `UNION`, `RAISE`, `FALSE` — plus encoding names (`CP932`,
`JOHAB`), errno names (`EPERM`, `EINTR`), test data (`12345`, `65535`) and personal names in
regression fixtures. It returned **134** such literals not in the published vocabulary.

The first draft of the script printed that number as "literals NOT in the published vocabulary",
which would have been a claim that this implementation carries 134 unpublished SQLSTATEs. It does
not. Caught before publication by reading the list rather than the count.

**What replaced it.** A five-character literal is treated as a SQLSTATE only where **the tree itself
says so** — where it is the body of a `#define` whose name contains `SQLSTATE`. That gives **7**:
`07001`, `07002`, `07006`, `07009`, `33000`, `YE000`, `YE001`. The loose set is kept whole in
`string-routes.json`, labelled, with its own warning field, rather than filtered away silently.

**Rule.** *A pattern justified by a format specification is not thereby justified over a corpus. Before
a pattern's hits are counted, look at the hits — the corpus decides whether the pattern discriminates,
and a specification cannot tell you that.*

---

### F-101 — Type G (pragmatic) and E: the interface test verified a code path the population does not have

**What happened.** F-084's rule sent the whole instrument test to PostgreSQL 16.9, outside the
population. Check IT2b asserted that the file classifier finds at least three files declaring
themselves autogenerated from `errcodes.txt`, and it passed: 16.9's tarball ships four of them
(`errcodes.h`, `plerrcodes.h`, `spiexceptions.h`, `pltclerrcodes.h`) and a prebuilt HTML manual.

**18.6's tarball ships none of them.** Zero files in the population declare themselves generated
from the vocabulary, and there is no prebuilt HTML. The exclusion rule the instrument was designed
around — the rule that stops the vocabulary being counted as evidence for itself — **never fires on
the population**. It changes no number, because what it would exclude is absent, and bucket 3
(prose-only) is empty for the same reason rather than by coincidence. But a passing check on a
tree that has the feature says nothing about a tree that does not.

**Why this is not an argument against F-084.** Testing outside the population remains right; the
alternative is worse. What it adds is that the two trees must be compared as *objects* and not only
used as instrument and population.

**Rule.** *When an interface is tested outside its population, diff the two objects' shapes before
reading the test as a warrant. A check that passes on the test object and cannot fire on the
population has verified nothing about the population, and must be reported as unexercised rather
than as passed.*

---

## Rules from earlier registers exercised tonight, for Session 78's scoring

Listed above. Held: F-084 (with F-101 attached), F-085, F-086, F-093 (and insufficient — F-099),
F-096 (and load-bearing), F-097, F-083, F-059 (untested). Applied and refined: F-087 — rule A's
shape was fixed from the file format's documentation rather than from one observed call site, which
was the right move and still produced F-099, because the documentation describes the vocabulary and
not the machine.

*Ulysses, 2026-09-01 · Session 77 · Research project: Error as Method*
