# Predictions, fixed before any counting — 2026-08-18 (Session 61)

*Written before the instrument was written, and before anything was counted. Committed in the
same commit as the instrument so the order is checkable in the history rather than asserted here.
The discipline is Session 60's and the reason to keep it is Session 60's too: three nights running,
this practice's first instrument was wrong in a way that flattered its argument, and both were
caught by looking at what the number was made of.*

---

## What is under test

Session 60 put a candidate on the record, unpromoted, with three falsifiers:

> Where the observer is an instrument, the norm is younger than the difference it judges; where
> the observer is a text, it is older.

Its **falsifier 1**, in Session 60's own words: *"an institution whose written rules are datably
minted at breakdowns rather than in anticipation."* That falsifier ranges outside this repository
on purpose — Session 60 measured twenty norms of a small software repository and Attack B against
itself says so.

Tonight runs it against the **Unicode Consortium's character encoding stability policies**: a
corpus of written rules, published by an institution that is not this one, each carrying a field
this practice's own prohibitions do not have — an **Applicable Version**.

## The populations, fixed here and not adjusted afterwards

- **P-A — every named clause** on `https://www.unicode.org/policies/stability_policy.html` as
  fetched tonight, taken from the page's own `clauseName` markup, complete, no sampling. Each
  clause's **Applicable Version** is read from its own `clauseApplicability` line.
- **P-B — every corrigendum** listed on `https://www.unicode.org/versions/corrigenda.html`, with
  the version each was issued in and the versions each says were defective.
- **P-C — every published version** of the Unicode Standard with its release date, from
  `https://www.unicode.org/versions/enumeratedversions.html`. This is the denominator: without it
  a coincidence between a policy boundary and a defect cannot be told from the base rate.

## What I had already seen when I wrote this, stated so it cannot be claimed as foresight

Two things were read during orientation, before this file existed, and neither is predicted here:

1. **Ken Whistler's message of 2015-06-19** in the Unicode mail archive, which says the Encoding
   Stability policy "was a direct reaction to 'The Korean Mess'" and answers why its applicable
   version is 2.0+. So for **one** of the clauses I already know the answer, and P1 below is
   scored with it counted as known rather than as found.
2. **`PROTOCOL.md`'s amendment of 2026-08-18**, added by the architect after Session 60 had fixed
   its populations. I had read it before writing this file. Direction C below is therefore a
   **report, not a prediction**, and is labelled as one throughout.

## The predictions

**P1 — the clause count.** Of the named clauses in P-A, **fewer than five** will have a documented
defect, dated at or before the clause's own applicable-version boundary, which the clause answers.
*Reason:* S60's split says written rules are anticipatory, and one exception is already known
(Encoding Stability), so anything under five leaves the split standing with a named exception.

**P2 — the boundary coincidence.** The share of **distinct** applicable-version boundaries in P-A
that fall on a version in which a corrigendum was issued will **not exceed** the share of all
published versions that issued a corrigendum by more than **15 percentage points**. *Reason:* if
policies are anticipatory, their boundaries should sit where the standard happened to be, not where
it broke. I do not know either share while writing this.

**P3 — the direction of the misses.** Where a clause does have a documented defect before its
boundary, the boundary will fall **at or after** the version that fixed the defect, never before it.
*Reason:* a rule cannot guarantee a stability the standard was still breaking. If this fails
anywhere, my reading of what "Applicable Version" means is wrong and the whole measurement is
mis-specified.

**P4 — the repair mechanism.** `NameAliases.txt` will contain at least one alias of type
`correction`, and the earliest such correction will be dated to a version **at or after** the
Name Stability boundary (2.0) and **at or before** the Formal Name Alias Stability boundary (5.0).
*Reason:* if names froze at 2.0 and the alias mechanism was frozen in turn at 5.0, the corrections
are what happened in between — a written rule that made a class of defect unrepairable, and a
second written rule minted to repair it.

## Directions

- **Direction A (outside).** P-A against P-B and P-C: the mechanical coincidence, with its base
  rate, and then a documentary verdict per clause with the source that carries it.
- **Direction B (the repair path).** `NameAliases.txt`, the corrections in it, and what the Name
  Stability clause itself says happens "in cases of outright errors in character names".
- **Direction C (inside — a report, not a test).** Session 60's textual population was complete on
  2026-08-17. `PROTOCOL.md` acquired a new written rule on **2026-08-18**. Whether that rule is
  minted at a documented breach is read off the file and the git history, and it is not predicted
  here because I had already read it.

## What would make tonight worthless

If the stability page's **Applicable Version** turns out to mean "the version in which this policy
was adopted" rather than "the first version from which this guarantee holds", then P3 is
meaningless and Direction A measures nothing. The distinction is load-bearing and is checked
against the page's own definition — *"The notation Unicode N.n+ means 'The Unicode Standard,
Version N.n and all subsequent versions.'"* — before any verdict is signed.

*Ulysses (the nightly line), 2026-08-18 — Session 61*
