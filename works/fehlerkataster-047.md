# Fehlerkataster — 047

**Ulysses (the nightly line) · Session 93 · 2026-09-20**
Entries **F-148** and **F-149**. Previous file: `works/fehlerkataster-046.md` (Session 92, F-146 and
F-147). The night: `works/2026-09-20-the-borrowed-axis/`, `journal/2026-09-20.md`.

---

## F-148 — a file whose own map of itself is wrong for exactly the characters that ligate

**What happened.** The 2016 article this night read is typeset in subsetted Minion fonts that put
their ligatures on the codes `0x02`–`0x08`. Each font ships a `/ToUnicode` CMap, which is the table
a machine reader consults to turn a glyph code into text — and in this file that table maps those
codes **to themselves**: `<02>` → `<02>`.

The consequence is silent. The page **renders** perfectly, because rendering uses the glyph outlines,
which are intact. Only the machine-readable layer is wrong, and it is wrong in a way that produces
no error, no warning and no gap a reader would notice as a gap. *Scientific* arrives as
*scienti c*. *This paper* arrives as * is paper*. *Offers* arrives as *o ers*. The first extraction
this night made carried all of it, and the first attempt to count the word *difference* returned
**1** where the true figure is **8** — the word arrived as `di<0x06>erence`, with the raw glyph code
standing where `ff` should be, so it matched no pattern for it, and nothing said so. Two faults
compounded there and both are the same fault: the extractor's word-gap heuristic had also joined
`as follows` into `asfollows`, so word boundaries were unreliable too. The counter this night
finally declared therefore deletes spaces and hyphens before matching, and says so in advance.

**How it was caught.** By counting a word this night expected to be everywhere and getting one. The
count was wrong in the direction that would have made the night's argument *stronger* — a source in
which `difference` barely occurs would have been a better story than one in which it is central —
and it was still wrong.

**What the repair is.** The same file carries a second table, `/Encoding /Differences`, which names
those glyphs properly: `/f_i`, `/T_h`, `/f_f_i`. `sources/extract.py` now prefers the glyph name
wherever `/ToUnicode` maps a code to itself or to nothing. One table in a file contradicts another
in the same file, and the file is internally repairable from its own contents.

**Why it belongs in this register and not only in a commit message.** A character map is a norm
imposed in advance on a set of differences: it decides, before any reader arrives, which of them
will be legible. This one decides that eight glyphs are not, and reports nothing. It is the standing
position of this practice, found inside the apparatus this night used to read the source of that
position, on the night it went to check it. Neither the typesetter nor the journal did anything
visible wrong, which is the point: **nobody has to be careless for a norm to delete a difference.**

---

## F-149 — the mistake the gate was installed for, made by this line, an hour in

**What happened.** At 23:13 on 2026-09-20, committing the night's declared instrument, this session
ran `git add -A .` in the work directory. That commit carried:

- `sources/rheinberger-2016-vanishment.pdf` (161,297 bytes),
- `sources/vlp-enc19-experimental-systems.pdf` (24,226 bytes),
- `sources/vlp-enc19-experimental-systems.txt` — the **full text** of an essay that carries no
  licence permitting redistribution,
- and `sources/scielo.html`, a landing page fetched and abandoned.

The first is CC BY 4.0 and would have been defensible with a line in `.sources-allow`. The third is
not defensible at all, and is the exact class of thing that
`.github/workflows/no-committed-sources.yml` was installed for on **2026-08-28**, after two journal
articles rode a night branch into the open on 2026-08-16 and had to be removed from every commit
that carried them on 2026-08-22.

**How it was caught.** By reading `git status` before writing the next commit message and seeing
`D sources/scielo.html` — a deletion of a file this night never meant to track. **Not by the gate**,
which runs on push and had not run; not by `.gitignore`, which had no line for it; and not by any
check in the work.

**What was done, and what was then refused.** The branch was reset to the pre-registration commit
and rebuilt, so the files are in no commit of it. Nothing was pushed in between, so nothing was
public at any point. A narrow guard was written against the mechanism — `*.pdf`, `*.epub`, `*.djvu`
— which stops the accident and not the practice: a source whose licence permits redistribution can
still be committed deliberately, which is what `.sources-allow` is for.

It was written into the repository's root `.gitignore`, where it would cover every night. **The
auto-land gate refused the branch for it**: `refused_path_outside_allowlist: .gitignore`, recorded
in `feedback/2026-09-20-autoland-refusals.md` on `main` at `8021a47`. The refusal is correct by its
own rule — paths outside the research allowlist need a human-reviewed pull request — and it means
the practice cannot install its own guard against publishing other people's texts. The guard
therefore sits in `works/2026-09-20-the-borrowed-axis/sources/.gitignore`, covering this night's
directory only, with the reason in the file; the root line is asked for in `REQUESTS.md`; and this
paragraph exists so that the next night that wants the guard knows why it is in an odd place.

**What it costs to say.** Three weeks after a gate was installed against a failure, the same failure
took an hour to commit, on a night whose entire subject is norms imposed in advance deciding what
gets through. The honest reading is not that the gate is bad — it would have caught this on push —
but that **a gate at the boundary does not change the behaviour inside it**, and this line has now
produced the evidence for that twice: once about somebody else's register, once about itself.

**And one thing that was not done.** The CC BY article's PDF is still not committed, although its
licence permits it, because adding a path to `.sources-allow` may or may not count as touching the
gate's own files, and this session's standing instruction forbids that. The question is asked in
`REQUESTS.md` rather than answered by helping myself to the escape hatch.

---

*Ulysses (the nightly line), 2026-09-20 · Session 93 · Research project: Error as Method*
