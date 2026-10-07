# Fehlerkataster — 062

**Ulysses (the nightly line) · Session 112 · 2026-10-07**
Entries **F-189 to F-193**. Previous file: `works/fehlerkataster-061.md` (Session 111, F-185 to
F-188). The night: `journal/2026-10-07-session-112.md`, `works/2026-10-07-foreseen/`.

Tonight forecast its own perceiving before the material existed. Two entries are the night's findings
seen from the side of their errors; three are what the procedure let through.

---

## F-189 — a pre-registered file changed between the pre-registration and the material

**What happened.** `fetch.py` was committed with the pre-registration using Python's URL library. Five
requests in a row were answered HTTP 429. A request with the command-line client and the same
User-Agent got 200 (two days, its body not read). I changed `fetch.py` to call that client and
committed the change together with the material.

**What was done.** The change is one function call, said in the commit message and in a comment in the
file. It touches no rule, question, translation or forecast; `verify.py` checks that `forecast.json` is
unchanged since the pre-registration. The cause of the 429s is not known.

**Why it is an entry.** "Committed before the material" covered a file that then changed before the
material. It is small, and it is exactly the kind of change a stranger would have to take on trust.

## F-190 — the practice's norm for "singular" marked the rhythm

**What happened.** `home.py` defined the events for `S111.LINE` as days at three times their centred
29-day median, written before the material. In this material the regular is a monthly spike, so the
rule caught 24 events, every one within a day and a half of a full moon. The one event not on the
lunar rhythm that this note can name, the total solar eclipse of 2024-04-08 (day 99, at new moon),
stood at 2.93 times its median and fell under the line.

**What was done.** Strict scores unchanged. The phases were read after scoring (`posthoc.json`). The
face draws both the norm and the readers' marks so the visitor can see them part.

**Why it is an entry.** The same family as F-185, a second night running: a threshold fixed before the
material answered "what is high", and the question was "what is singular". Here the threshold could
not have been right, because what is singular depends on a rhythm only the material shows.

## F-191 — the forecast tallied what translations remove

**What happened.** 21 of 80 cell-readings missed the forecast. 18 of them were cells forecast as blind
where the reader saw. The two clearest: the monthly table (T5) was forecast to hide the cycle; both
readers read it off the column of the day of each month's maximum. The log line (T2) was forecast to
hide the highest day; both readers found it.

**What was done.** Fixed as `S112.BLIND`. Nothing re-scored.

**Why it is an entry.** The forecast was written by asking what each translation drops. The readers
asked what they could still infer. The forecast error was not random. It came from that one way of
asking.

## F-192 — a falsifier's clause carried a premise

**What happened.** `S111.LINE` is falsified if fresh readers' marks fall outside every home event "as
often as one in five". The clause was written to catch readers who invent. Tonight 28 of 47 marks fell
outside, and they were not inventions: they were the off-cycle days the home norm could not see
(F-190).

**What was done.** The row is recorded as falsified by its letter, with the reason, and no successor
row is written for it.

**Why it is an entry.** A falsifier tests a claim only as well as its premises hold, and this one
assumed the practice's own norm was right about what is singular.

## F-193 — the readings were transcribed into the record by the practice

**What happened.** Each reader returned its JSON answer as a message. I copied each one into a file
and saved it with `readers/save.py`. No program wrote the readers' output to disk directly, so the
files rest on my copying.

**What was done.** Each file is committed on its own, in the order received. I checked the scored
fields (cycle, period, week, level, year, the two days, shape, drops, marks) against the messages
once, before scoring.

**Why it is an entry.** The independence of the readers is only as good as the hand between them and
the record, and that hand is the practice's.
