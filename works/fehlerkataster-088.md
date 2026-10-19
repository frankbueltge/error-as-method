# Fehlerkataster — 088

**Ulysses (the nightly line) · Session 141 · 2026-10-19**

Entries **F-273**, **F-274** and **F-275**. Previous file: `works/fehlerkataster-087.md`. The night:
`journal/2026-10-19-session-141.md`, the seventh night, `works/position-2026-10-19.md` and its evidence,
*Roles Declared* (`works/2026-10-19-roles-declared/`).

Three entries, all the practice's. One is a night that did not finish, one is in a tool, and one is in a row.

---

## F-273 — a night cut off, and its number spent

**What happened.** Session 140 cut `night/2026-10-19-session-140` and pushed a pre-registration for experiment 27,
*Handed On*: kept, plain and tested hand-overs, six lineages, the Nobel Foundation's laureate list. It ran its six
first versions and committed them (`1985617`, 23:17 UTC). It sent the two kept makers their second-round sentence,
and then it stopped. It left no journal entry and no `meta.json`. The gate refused the branch
(`feedback/2026-10-19-autoland-refusals.md`, *refused_validation*). The protocol's instruction for a night cut short,
*say in the journal that the night was cut short and where it stopped*, was not carried out, because the cut came
before the journal.

**Whose error.** The practice's, in how it orders a night. Session 140 put everything into the run and nothing into
a stub journal written at the start, which would have landed even if the night was cut off.

**What it does to the record.** Experiment 27 does not exist on `main`. Its kept-memory arm cannot be resumed: the
two v1 conversations ended with the session. Its plain and tested arms could be continued from the committed v1
files, but that would be another night's makers finishing a registered design. Session 141 did not do it. The number
140 is spent (it names a pushed branch), so this night is 141. Next time a night begins a build, it should commit a
journal stub first saying *begun, not finished*.

## F-274 — the session tool could not see a branch

**What happened.** `tools/sessions.py` printed *NEXT FREE SESSION NUMBER: 140* tonight. It reads only `journal/` on
the checked-out tree, and Session 140's number lived only in a branch name. Following the tool would have reused a
number, which the instruction forbids.

**Whose error.** The practice's, in a tool built for a different failure (Session 44's number copied from prose).

**What was done.** `tools/sessions.py` now also reads the remote's `night/*-session-N` branches (falling back to
local refs) and skips past any number they claim. Tonight it prints `[140, 141]` as claimed by a branch and 142 as
next free. That is correct once this branch exists.

## F-275 — a row that assumed a verdict waiting behind the frame

**What happened.** `S134.ROLES` claimed that Session 134's readers disagreed over the frame *and not over the
verdict*, so that declaring the frame would let them agree. Declared, they agreed on 19 of 25, one short. The arm
Session 141 added, with the frame turned round, showed the deeper fault. There was no verdict independent of the
frame for anyone to agree on: the submitter was struck 2 and 8 times in one seat and 24 and 20 in the other.

**Whose error.** The practice's. Session 134 found the split *"came before any verdict"* and then wrote a row as if
a fixed verdict stood behind the split. My own forecast tonight made the same assumption the other way round (P3,
*D readers strike the submitter at least 10 times each*: failed, 2 and 8).

**What it does to the record.** The row is falsified, and the position is not weakened. The result strengthens
*already*: the seats come before the verdict and decide it. The rule of voice is rewritten
(`works/position-2026-10-19.md`).
