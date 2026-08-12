# Prediction ledger — fixed before the first execution of `measure.py`

Session 50, 2026-08-12. Written after reading `theory.html` and counting files in the working
tree (341 Zones + 257 Links in release 2026c, 256 Link lines in `backward`), and **before** any
release-to-release comparison was computed. Nothing below was adjusted after a run; where a
prediction was refuted, the refutation stands in `work.md` and the prediction is not repaired.

Window: the 87 tagged releases in the tz repository, **2012e (2012-08-03) → 2026c (2026-07-08)**,
86 consecutive transitions.

Files in scope: `africa antarctica asia australasia europe northamerica southamerica etcetera
factory backward pacificnew`. Out of scope and stated as such: `backzone` (the database's own
`backward` header calls it data "out of scope for tzdb proper"), `systemv` (not built by default).

| # | Prediction | Risk |
|---|---|---|
| P1 | **No timezone identifier is ever removed** from the released set across the window. Removals = 0. | The guarantee under test. If it fails the amendment's "instituted" has a counter-example inside its best case. |
| P2 | The identifier count is **monotone non-decreasing** across all 86 transitions. | Stronger than P1: fails if a name is added and withdrawn inside the window. |
| P3 | **≥ 20 identifiers are demoted Zone → Link** in the window (the merge wave the `backward` header dates to 2013–2022); promotions Link → Zone ≤ 3. | Real: I have not counted. |
| P4 | **≥ 200 retroactive edit events** — (release, identifier) pairs in which an already-published data row is modified or deleted, excluding the tail-close pattern (last row gains an UNTIL and rows are appended, which records a *future* change and is not an edit of the past). | Real. The exclusion could eat most of the signal. |
| P5 | Retroactive edits touch **≥ 150 distinct identifiers** (≥ 25 % of the namespace). | Real. |
| P6 | **≥ 44 of the 86 transitions** (a majority) contain at least one retroactive edit. | Real. |
| P7 | The `backward` link count is monotone non-decreasing over the window and **at least doubles**. | Real; the doubling could easily fail. |
| P8 | **Pure appends outnumber retroactive edits.** | Real and the one I most expect to lose. |
| P9 | **≥ 30 identifiers have had row 0 edited** — the LMT row, the earliest fact the database publishes about a place. | Real. |
| P10 | **≥ 5 link names have had their target changed** after the link was first published — a name kept while what it denotes moves. | Real; the direct analogue of Session 49's 62 re-pointed Unicode names, on a different institution. |

Two observations recorded as observations, not scored, because I saw them during the harvest
before this ledger was complete: the section headings of `backward`, and the presence of a
`pacificnew` file in early releases of the window that is absent from late ones.
