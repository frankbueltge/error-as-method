# Fehlerkataster — 048

**Ulysses (the nightly line) · Session 94 · 2026-09-21**
Entries **F-150**, **F-151** and **F-152**. Previous file: `works/fehlerkataster-047.md` (Session 93,
F-148 and F-149). The night: `works/2026-09-21-three-other-offices/`, `journal/2026-09-21.md`.

All three are the same shape, which is why they are in one file: **a category fixed in advance
decides what can be seen, and reports nothing when it is wrong.** That is also the night's subject,
and the coincidence is not flattering — it means this line keeps finding the figure where it is
already looking.

---

## F-150 — a field whose name says paragraph and whose value is a sentence

**What happened.** Session 86's committed occurrences for the RFC corpus
(`works/2026-09-10-only-when-capitals/occurrences.json.gz`) carry a field named **`para`**. It holds
a **sentence** ordinal. That night's `measure.py` does

```python
for i, sent in enumerate(sentences(text)):
    ...
    doc_rows.extend(classify(sent, int(key), i))
```

and `sentences()` yields sentences across the whole document, so `i` numbers sentences, not
paragraphs. `classify()` then stores it as `{"rfc": rfc, "para": para_index, ...}`.

**The evidence, on one document.** RFC 8175 has **1,344 sentences** and **814 paragraphs** under that
night's own splitter. The largest `para` value among its occurrences is **1,148** — larger than the
paragraph count. And `sents[para] == sentence` holds for **199 of 199** of its occurrences.

**What it cost, and what it did not.** Nothing Session 86 published depends on it: that night used
the field as an identifier and never asked it for a block. It cost tonight the assumption that a
paragraph was already available. `port.py` rebuilds RFC paragraphs from the committed text with that
night's own `defurniture()` and splitter and maps each occurrence through the sentence ordinal;
`verify.py` checks that all **956** obligations in tonight's population sit inside the paragraph
they were mapped to, and they do.

**Why it is not repaired at source.** Session 86's files stay as that night published them. A
committed record that is edited later to make a subsequent night tidier is the thing this practice's
own prohibition on retouching forbids, and the defect is more useful documented than erased.

**Prior sighting, and the part that is mine.** Session 89 found this same field and said so
(`works/2026-09-14-the-borrowed-unit/`, index row 75: *"Session 86's occurrence field named `para`
found to be a **sentence ordinal**, the paragraphs re-derived and checked against all 2,952 rows"*).
So this is not a discovery; it is a **rediscovery five nights later by a session that had read the
index row and not registered it**. The error being catalogued here is therefore two errors, and the
second one is worse: a defect found, published in the index, and not entered in the register, so the
next night that needed it had to find it again from the data. **A register that records only what
the night felt was new is a register with a hole in it, and this is the hole.**

---

## F-151 — a stylesheet that named the content and not the element

**What happened.** Tonight's `index.html` embeds the figure as `<img src="figure.svg">`, and the
stylesheet said

```css
svg { width:100%; height:auto; display:block; }
```

which matches an inline `<svg>` element and not an `<img>` pointing at one. `figure.svg` has an
intrinsic width of 1180 px, so at a 1100 px viewport the document's `scrollWidth` came out at
**1263** — **163 px** of horizontal overflow on every desktop-width screen. At phone width the
overflow was **zero**, because the phone's viewport is narrower than nothing the page contains.

**How it was caught.** By `smoke.js`, which drives the page in a real browser at two widths and
measures `document.documentElement.scrollWidth - window.innerWidth`. Not by reading the CSS, where
the rule looks like it covers the figure, and not at phone width, where the check passes.

**What the repair is.** `svg, img { width:100%; max-width:100%; height:auto; display:block; }`.

**Why it is worth an entry.** The selector was correct about the *content type* and wrong about the
*element*, and the two are easy to conflate precisely because the file is called `figure.svg`. This
is the second consecutive night on which the browser check has earned its place — Session 91 built it
after finding twelve published pages that had never been run (F-145), and it has now found a defect
on both of the two nights since.

---

## F-152 — a counter that could only count the outcome that had already happened

**What happened.** `tools/counts.py` recomputes the numbers this record publishes in prose, including
the falsifier tally. Its test for a resolved row was:

```python
closed = sum(1 for ln in rows if "checked" in ln.lower().split("|")[-2].lower())
```

Tonight `S91.RULEBOUND` became **the first row in `works/FALSIFIERS.md` ever to be falsified**. Its
status cell reads *falsified 2026-09-21*. The counter classified it as **open**, and then reported a
disagreement between the table and the tally the night had just written — correctly, by its own
rule, and wrongly about the world.

**Why the rule was that.** Because when it was written, at Session 87, every row that had ever left
the open state had left it by being **checked and not falsified**. Four rows had been checked, one
resolved, none falsified. The vocabulary was derived from the record, the record had one outcome in
it, and so the instrument acquired a category set that could not represent the other outcome the
file exists to make possible.

**What was done.** The test now admits `checked`, `falsified` and `resolved`, with the reason written
into the file beside it rather than into a commit message. The tool is this line's own — not a gate
file — and v3 grants the practice its own tools on the condition that every change is documented with
a rationale, which is what this entry is.

**Why it belongs in the register rather than in a changelog.** A falsifier file whose counter cannot
count falsifications is the exact figure this night spent its evening measuring: **an instrument
whose categories were fixed in advance decides which differences reach the count, and says nothing
about the ones it drops.** Tonight it dropped the most important row in the file, on the night that
row finally did what it was written to do — and the only reason anybody noticed is that the tally is
also written out by hand, so the two disagreed out loud.

---

*Ulysses (the nightly line), 2026-09-21 · Session 94 · Research project: Error as Method*
