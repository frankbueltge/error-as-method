# Predictions and coding rules — committed before any maker runs (Session 180, 2026-11-18)

## The question

When a machine practice makes a form that states facts (a museum wall label, from a photograph alone), where do
its errors live: in what it sees or in what it brings? And when a record people made is set beside its work, does
it correct only what the record names? The second half is standing finding 3 (*what is told passes only by
admitted moves*) tested in making, not in judging. The field's nearest study (Siro & Hollink, arXiv:2610.31193,
EMNLP 2026 Findings) measures museum descriptions in one pass, claim by claim; it does not show the maker the
record and let it revise.

## Material and arrangement

Twelve objects from The Metropolitan Museum of Art's Open Access collection (CC0), one each from twelve
departments, drawn by `prepare.py` under a fixed seed and rule. Six fresh makers, four objects each, each object
labelled by two makers:

| maker | objects |
|---|---|
| m1 | A B C D |
| m2 | E F G H |
| m3 | J K L M |
| m4 | A E J B |
| m5 | F K C G |
| m6 | L D H M |

Round 1: the photograph only (`briefs/round1.md`). Round 2: the same maker, continued by message, is sent the
museum's record and revises (`briefs/round2.md`).

`record_fields`: title, objectName, culture, period, dynasty, reign, artistDisplayName, artistDisplayBio,
objectDate, medium, dimensions, geographyType, city, state, county, country, region, subregion, locale,
classification, creditLine. Empty fields are left out.

**Confound carried, stated before the run.** Every maker carries this repository's instruction file, headed with
the line's working title (`S179.NAME`, `REQUESTS.md`, 2026-11-17). Its request went unanswered past Session 180, so
by that request's own terms the confound is recorded on every maker claim and the line goes on. P8 measures how far
the name leaks into tonight's labels.

## Coding (by the conductor, Session 180, by these rules)

Each round-1 claim gets one record verdict:
- **R+** the record states it or entails it (a date range that contains or overlaps it within the record's own
  hedging; the same culture or a wider/narrower name of the same place; the same material).
- **R−** the record states something incompatible (date ranges that do not overlap; a different culture or place
  of making; a different material; a different object type; a different maker).
- **R0** the record is silent.

R0 claims of kind `depiction`, `technique` or `size` and source SEEN are checked against the photograph:
**V+** visible, **V−** contradicted by the photograph, **V?** cannot be told from the photograph.

Round-2 fate of each round-1 R− claim: **corrected** (removed or changed so it no longer contradicts) or **kept**.
Round-2 fate of each round-1 R0 KNOWN claim: **kept** (the same content, reworded or not) or **dropped**.

## Predictions

- **P1 — error lives in knowing.** At least 70 % of R− claims carry source KNOWN.
- **P2 — the size of the error.** Among round-1 claims the record can judge (R+ and R−), the share R− lies
  between 15 % and 40 %.
- **P3 — told, it corrects.** At least 90 % of round-1 R− claims are corrected in round 2.
- **P4 — what is not told survives.** At least 60 % of round-1 R0 KNOWN claims are kept in round 2.
- **P5 — the record is built on, not only obeyed.** Round 2 holds at least 80 % as many R0 KNOWN claims as round 1
  (counted in round 2 against the same record).
- **P6 — two makers, one observer.** Where both makers of one object make an R− claim of the same kind
  (where, when, who, material, what), they give the same wrong answer in at least half of those pairs.
- **P7 — the maker misnames its sources.** At least 10 % of SEEN claims are of kind when, where or who with no
  inscription in the photograph that shows it (checked by the conductor against the image).
- **P8 — the name leaks little.** At most 2 of 24 round-1 labels match
  `error|mistak|misattribut|misread|wrong|forger|fake` (case-insensitive).

What would count against the project's hypothesis rather than for it: if P4 fails low (the makers drop what the
record does not name), a record corrects more than it names, and standing finding 3 does not carry from judging to
making.
