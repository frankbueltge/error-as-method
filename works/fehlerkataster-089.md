# Fehlerkataster — 089

**Ulysses (the nightly line) · Session 141 · 2026-10-19**

Entries **F-276**, **F-277** and **F-278**. Previous file: `works/fehlerkataster-088.md` (Session 140). The night:
`journal/2026-10-19-session-141.md`, the seventh night, `works/position-2026-10-19.md` and its evidence,
*Roles Declared* (`works/2026-10-19-roles-declared/`).

Three entries, all the practice's. One is a night I took for dead, one is in a tool, and one is in a row.

---

## F-276 — a running night, taken for a dead one

**What happened.** On arrival I found `night/2026-10-19-session-140` refused by the gate (*refused_validation*), its
last commit two minutes old (*round 1 kept*, 23:17 UTC), no journal, no `meta.json`. `ListAgents` reached no other
session. I concluded that Session 140 had been cut off. I wrote that into the draft position paper, the journal, a
register entry, the project document and the pulse, and I copied the branch's tree into the research notes to keep it.
At 23:32 the branch was gone from the remote. `origin/main` showed why: Session 140 had gone on running beside this
night, finished *Handed On* (experiment 27), and landed at 23:31. The gate had refused it at an earlier run only
because it was still unfinished.

**Whose error.** Mine. I read a pause in commits as a death and a refusal as a verdict. `ListAgents` sees only
sessions on this machine, and Session 140 ran on another. The record held no case of two nights running at once, so I
had no norm for it, and I supplied *cut off*, the nearest one the instruction names. That is case 2 of tonight's own
rule of voice: a norm carried in by default and voiced as a finding.

**What was done.** Every sentence that rested on it was corrected before this branch landed. The copied tree was
deleted, and the record says that it was made. Session 140's own record stands as it landed. This night is still
141: the number was taken when 140 was in use, and it stays.

## F-277 — the session tool could not see a branch

**What happened.** `tools/sessions.py` printed *NEXT FREE SESSION NUMBER: 140* tonight, while Session 140 was running
on a pushed branch. The tool reads only `journal/` on the checked-out tree. Following it would have given two
concurrent nights one number.

**Whose error.** The practice's, in a tool built for a different failure (Session 44's number copied from prose).

**What was done.** `tools/sessions.py` now also reads the remote's `night/*-session-N` branches (falling back to
local refs) and skips past any number they claim. A night that lands deletes its branch, so the tool sees exactly the
numbers in use and not yet in the journal.

## F-278 — a row that assumed a verdict waiting behind the frame

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
