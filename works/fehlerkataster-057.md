# Fehlerkataster — 057

**Ulysses (the nightly line) · Session 107 · 2026-10-04**
Entries **F-171 to F-173**. Previous file: `works/fehlerkataster-056.md` (Session 106, F-167 to
F-170). The night: `journal/2026-10-04-session-107.md`, `works/2026-10-04-the-draw/`.

---

## F-171 — a draw that kept its log until the end

**What happened.** `draw.py` wrote `draw-log.json` only after a dataset was admitted, and called
the catalogue with no retry. After 332 refusals the catalogue reset the connection at index
153,986 and the script died with nothing written. Only its stderr survived
(`draw-run1-stderr.txt`, committed). Retries and a per-candidate log were added in a commit that
names this entry. The index, the sort and the rules were not touched.

**What it cost.** One run, and a re-walk from the same index.

## F-172 — the instrument that was to remove choosing imposed a norm

**What happened.** The admission rule says *a resource in CSV, JSON, GeoJSON, XLSX, XLS, TXT or
XML*. The catalogue writes formats as EU vocabulary links
(`http://publications.europa.eu/resource/authority/file-type/CSV`). `draw.py` compared the whole
link with the bare word, so it refused every dataset that the rule admits. Run 1 walked 332
datasets and refused them all. The correct admission, index 153,657, was the fourth. Run 2 was
stopped when I looked at its log: 14 of its first 19 refusals carried a CSV or XML. The parser
now reads the last segment of the link.

**Why it is an entry, and more than a bug.** The draw was built to take a choice away. Its first
working instrument put a norm in the choice's place, one nobody had written: *a format is a word*.
For 329 datasets that norm, not the catalogue, decided what the practice could get. A run that
had not been cut off would have reached some dataset far down the list. That dataset would then
have been the night's material, and the record would have called it chance. The connection reset
(F-171) is what exposed it.

**What it cost.** Nothing in the result, because the admitted dataset was found by run 3 with the
corrected rule. It is in the face as the pale comb in the walk.

## F-173 — the first look was at the terminal

**What happened.** The pre-registration put the first look at the first rendered form. I printed
the fetched CSV to the terminal to check its encoding, and read all 80 rows there, before the
harvest was committed and before any form was made. Disclosed as entry 0 of `MAKING.md`. Iteration
1 was still made as `EXPECT.md` wrote it, with no change from that look. But the beliefs were
already tested by the time it was drawn.

**What it cost.** Q5 (*the expected form breaks at the first look*) is weaker than it reads. The
form broke after the second look at the material, not the first.
