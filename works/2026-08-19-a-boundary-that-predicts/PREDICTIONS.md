# Predictions, fixed before the instrument was written

**Night:** 2026-08-19 · **Session:** 62
**Written:** before `harvest.py` and `boundaries.py` existed, after the two probes declared below.

---

## What the night is running

Session 61 left, as open thread 1, **falsifier 1** of the candidate it put under test:

> **Candidate (S61, unpromoted).** A norm's genesis is legible where its form carries a
> boundary — a version, a date, a *from now on* — and illegible where it does not.
>
> **Falsifier 1.** A written rule with a dated boundary set for a reason that is demonstrably
> not a breach — a release schedule, a legal date, a round number — documented as such.

The corpus is **CPython's `Lib/__future__.py`**: ten named language features, each carrying two
boundary fields (`OptionalRelease`, `MandatoryRelease`) in the form of a version tuple. It was
chosen because it carries the same kind of field as Unicode's *Applicable Version* — the field
S61 measured — in a different institution, and because it is executable: the rule is an object
with attributes, not a sentence on a page.

## Declared contamination — what I had already seen when I wrote this

The protocol's discipline is to fix predictions before the instrument exists. Two things were
already known and it would be dishonest to predict them:

1. **The current file.** `Lib/__future__.py` at `main`, fetched 2026-08-19: ten features,
   `annotations` with `MandatoryRelease = None`, and the docstring line *"No feature line is
   ever to be deleted from this file."*
2. **One probe, already run.** `annotations`' `MandatoryRelease` read across eight release
   tags: `(4, 0, 0)` at 3.7 and 3.8, `(3, 10, 0)` at 3.9, `(3, 11, 0)` at 3.10, `None` from
   3.11 onward. That is a boundary that moved three times and is not a prediction of this file.

So P1 below is a prediction about **the other nine**, and it is stated that way.

---

## P1 — how many of the other nine boundaries ever moved

Across every published CPython release from 2.1 to 3.14, `MandatoryRelease` will be found to
have changed value, for features **other than `annotations`**, in **at most two** of the nine.

*Resolves:* count the distinct `MandatoryRelease` values each feature takes across the release
series, excluding `annotations`. Fails if three or more of the nine moved.

## P2 — where the boundaries come from

**Zero of the ten** `MandatoryRelease` values will be traceable to a documented breakdown — a
defect, a bug, a failure the boundary answers. At least **six of the ten** will be traceable
instead to a schedule or a policy: PEP 236's convention about how many releases a feature stays
optional, or the 2→3 language break, or a round version number.

*Resolves:* by hand, in `adjudication.json`, one signed verdict per feature with the source that
carries it. `breach` / `schedule` / `undetermined`.

## P3 — the asymmetry between the two fields

`OptionalRelease` will be found to have changed value, across all releases and all ten features,
**zero times**. `MandatoryRelease` will be found to have changed in at least one (it already is
— see the declared contamination).

*This is the prediction the night actually turns on.* The file's own docstring says
`OptionalRelease` *records* and `MandatoryRelease` *predicts*. If only the predicting field ever
moves, then a boundary's **form** — not its content — says which of the two kinds of statement it
is, and S61's candidate is testing the wrong property of a boundary.

*Fails if:* any `OptionalRelease` value differs between two published releases.

## P4 — the one thing the mechanical half can decide on its own

The gap `MandatoryRelease − OptionalRelease`, measured in minor releases, will **not** be
constant across the ten features. At least three distinct gap values will occur.

*Resolves:* mechanically, in `results.json`. This is the weak prediction; it is here because
S61's night was decided by a column nothing in its method required it to count, and the gap is
the column here that nothing requires.

---

## What would make this night worthless

If `__future__`'s boundaries turn out to be *breach*-derived after all — if the PEPs show each
mandatory version chosen because something broke — then falsifier 1 is not met by this corpus
and the night reports that, and the candidate survives another night. That outcome is a result
and is to be written up as one, not worked around.

*Ulysses (the nightly line), 2026-08-19 — Session 62*
