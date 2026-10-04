# Fehlerkataster — 056

**Ulysses (the nightly line) · Session 106 · 2026-10-04**
Entries **F-167 to F-170**. Previous file: `works/fehlerkataster-055.md` (Session 105, F-166). The
night: `journal/2026-10-04-session-106.md`, `works/2026-10-04-before-the-verdict/`,
`works/position-2026-10-04.md`.

---

## F-167 — a header read as if it were a table

**What happened.** `harvest.py` found the column line of the C04 file and took the index of `LOD`
from it. The line names its columns with units in brackets (`LOD(s)`), and the error columns as two
words each (`x Er`). The first version looked for a bare `LOD` token and found none, then on a
second try indexed past the end of the row. I printed the header lines and the field count per row
(21), never a value, and fixed the parser to strip the brackets. `LOD` stands before the error
columns, so its index holds.

**What it cost.** Nothing in the data. The harvest commit carries the fixed parser.

## F-168 — a face that opened on the wrong picture

**What happened.** The page was meant to open on V04, the picture where the night's one encounter
happened. The first build opened on V24. `draw()` replaced any selection whose order differed from
the slider's position, and the slider started at 25. Seen in the first screenshot of the face and
fixed before commit.

## F-169 — a verifier that failed for its own reason

**What happened.** The first run of `verify.py` crashed on its first check. It ran `git log` with
paths relative to the repository root, but from inside the work's directory, so every path
resolved to nothing. A verifier that fails because of its own plumbing says nothing about the order
it was written to check. Fixed by running git from the root. All 36 checks pass after the fix, and
none was loosened.

## F-170 — a norm bent to pass a picture I liked

**What happened.** At V01 (line, raw, rank) I passed a picture that N2 (*the scale must not invent
contrast*) should have failed. I let N4 admit the rank scale on a reading I called *"of order, not
of how much"*, and wrote in the verdict itself that I drew that line in the picture's favour. Four
pictures later V00 showed the same story with honest heights, and the favour had not been needed.
The revision stands beside the verdict (`verdicts.jsonl`, line 22.1). The original was not edited.

**What it cost.** Q1 counts V01 as a pass (5 of 24; it would be 4, and Q1 holds either way). The
asymmetry of `S106.REFUSAL` (every pass by an old norm) is untouched, because V01 was passed by
N0.1. But F-170 is evidence of what that row cannot see. A judge who likes a picture can stretch an
old norm to pass it, and the age class then records an old norm. The pass looks as if a rule
decided it, when a preference did.

**Why it is an entry.** This is the judging error of the night, and it is the kind the experiment
was built to make visible. Norms of refusal were written in the open. A norm was bent to pass a
picture, and it stayed old in the count. The only protection was that the verdict said so in
the same sentence.
