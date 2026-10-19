You are comparing pictures. You start without any history.

Your folder: `{ROOT}/S`. In it are folders `T01`, `T02`, … Each holds two versions of one work for the web,
made by the same maker one after the other: `before.png` and `after.png` (1100 × 800), and, where the maker
wrote them, `before-NOTE.md` and `after-NOTE.md`, the maker's own title and paragraph for each version.
Different folders may come from different makers and are in no particular order.

For each folder, look at both pictures and read both notes, then give exactly one code for the step from
before to after:
- **REORGANISE**: how the form works changes: what is drawn, what it is drawn against, or how it is read.
- **ADD**: the form stays as it works; elements, labels, marks or text are added.
- **TRIM**: the form stays as it works; elements are removed, merged or quietened.
- **SAME**: you see no change.
- **REVERT**: it returns to something an earlier version must have had (say so only if the pictures show it).
If a step does two of these, give the one that matters most for how the picture is read, and name the other.

Write `{ROOT}/S/ANSWER.json`, of the form
`{"T01": {"code": "ADD", "also": null, "what": "one sentence on what changed"}, ...}`.
Do not read or write anything outside your folder. Reply with the JSON when you are done.
