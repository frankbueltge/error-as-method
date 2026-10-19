# The prompt given to each D reader (verbatim between the rules)

Session 134's `works/2026-10-18-not-a-defect/readers/PROMPT.md`, as given to its readers (the ◆ marker removed, the path changed), with one sentence added after the code sentence. SHA-256 of `ENTRIES.md`: `5fe8ab6dfc9a1aefd687958aa185e7ff7ac96091a8aba540fcb57bcad080e5ab`, byte-identical to Session 134's file. The file is not committed.

---
You are reading 40 entries from a public register of reported defects. The file is
`/tmp/claude-0/-home-user/910d4409-7a9e-5a09-8852-b51312a5e9d1/scratchpad/readers/ENTRIES.md`.
Read ONLY that file. Do not open any other file, and do not use the web.
Each entry is an issue reported against a published standard, with the outcome its committee recorded.

Each entry describes a difference between two terms: something that was **held fixed** when the
difference appeared (a rule, a check, a threshold, an instrument kept unchanged, a trusted note, a
design assumption, an outcome against which a forecast is scored) and something that was **allowed
to be wrong** (an output, a reading, a forecast, a rendering, new code).
Where a rule, check, threshold or norm was written as code, take the rule as written in words as the held term and the code that applies it as the judged term.
In these entries, the published text of the standard is the judged term, and what the submitter holds against it is the held term.

For each entry decide, from the entry's own text:
- `held`: in a few words, the term that was held fixed.
- `judged`: in a few words, the term allowed to be wrong.
- `wrong`: which term the entry says is wrong. `J` = the judged term; `R` = the held term; `B` = both;
  `X` = the entry calls neither wrong.

Answer with only a JSON array of 40 objects, in the entries' order:
`[{"id": "E01", "held": "...", "judged": "...", "wrong": "J|R|B|X"}, ...]`
No other text.
---
