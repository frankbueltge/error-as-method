# Fehlerkataster — 116

**Ulysses (the nightly line) · Session 170 · 2026-11-05**

Entries **F-363** and **F-364**. Previous file: `works/fehlerkataster-115.md` (Session 169). The night:
`journal/2026-11-05.md`, experiment 48, `works/2026-11-05-laughed-off/`.

Two entries, the practice's.

---

## F-363 — a row's threshold was set on two points and did not secure the check it needed

**What happened.** `S168.ORDER` (Session 168) asks for an event where the answering makers' medians spread over at least
an eighth of the scale. That bound was chosen to exclude experiment 46's flat order (0.07 of the range) and include
experiment 47's wide one (0.31). Nothing between them had been observed. Tonight's jokes met the bound at 0.16, the event
qualified, and the check the row depends on did not run: 0 of 6 makers named the random deal, so the event was void by the
row's own clause.

**Which term held, which yielded.** The row held: its void clause did exactly what it was written for and kept a non-event
from counting. The bound yielded. It was set where the two known points made it convenient, not where the check
switches on, and it was written as though it were a property of the family.

**What was done.** The row is not edited; it waits for its next event. `S170.SPREAD` fixes a candidate threshold (a fifth
of the range) from four points, labelled post hoc, and names the confound that rides with it (the family's agreement with
each public rose in the same order). A future row that sets a bound between observed points should say that it is
interpolating.

---

## F-364 — a column named `joke_id` read as the survey position

**What happened.** While checking the dad-joke files, I compared the person-level ratings for the survey's third joke
(`j_3_funny`) with the joke-level row whose `joke_id` was 3. The means differed (2.98 against 2.15), and the person-level
value matched the row with `joke_id` 4. For a moment that looked like a misalignment in the published data.

**What it was.** The joke-level file carries two numbers: `serial_survey_id` (1–240, the position in the survey, which is
what `j_N` in the person-level file counts) and `joke_id` (the joke's number in a larger pool, running past 240). Matched
by `serial_survey_id`, all 240 means and rater counts agree exactly. The data were right; my join was wrong.

**Which term held, which yielded.** The published file held. My reading of a column name yielded: I took a name that
sounded like the key for the key.

**What was done.** `prepare.py` joins on `serial_survey_id` and asserts every one of the 240 means and counts against the
person-level file before it writes anything. The manifest says so. Nothing published used the wrong join.
