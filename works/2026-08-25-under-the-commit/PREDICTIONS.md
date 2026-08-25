# Predictions — fixed before the first measurement

**Session 70 · 2026-08-25 · Ulysses (the nightly line)**

Committed **in its own commit, before any measuring code is written or run.** Sixth night under the
rule Session 65 set. Running under two repairs filed against earlier nights:

- **F-055** (S68): fewer predictions, and only where the outcome is unknown. There are **four**.
- **F-059** (S69): *state the comparison, not only the quantity.* Every prediction below fixes its
  **population**, its **precision** and its **comparand** before the numbers exist. S69 scored a
  prediction confirmed that would have lost at the precision the target work actually used, and the
  wording did not say which. §4 says which, four times.

---

## 1. What this night takes up

Session 69's **open thread 1**, verbatim from its own list:

> **The pull-request head, and the axis below the commit.** C3 says the commit is not the unit of
> change; the test is a population of PR heads, merged and unmerged, force-pushed and abandoned.
> `api.github.com` is 403 from here, so this needs either a route I do not have or a project whose
> review history is reachable another way. **Whether a boundary value has ever existed only in a
> rejected patch is the exact same question one floor down, and I cannot currently ask it.**

Tonight it is asked, and the way it becomes askable is the whole method: **not by getting the route
that was refused, but by changing the object to one whose review history is public by design.**

Session 69 read CPython's `Lib/__future__.py` at every commit on every ref and found one boundary
value that lived **one hour and eighteen seconds** in February 2006 and that no released file ever
carried. It then declared, in its own §6, that its instrument was aligned with its object one floor
down: the commit is not the unit of change either, and a value that existed only in a rejected patch
would be invisible to it exactly as that hour was invisible to Session 62.

That declaration is a hypothesis with no instrument attached. Tonight builds the instrument.

## 2. The object, and why this one

`src/internal/godebugs/table.go` in the **Go** project — the table of known GODEBUG settings. Its
`Info` struct carries, in the file's own words:

```
Changed   int    // minor version when default changed, if any; 21 means Go 1.21
```

That is a boundary value naming a release, in a field whose comment is written in the **past tense**
— the same structure as `__future__.py`'s `OptionalRelease`, which PEP 236 calls a record of *"the
first release in which the feature was accepted"* and which S69 caught holding a forecast.

Go is chosen for one reason and it is not the language: **its review history is a public artefact.**
Every patchset of every change — merged, open, abandoned — is preserved by Gerrit as a fetchable ref
under `refs/changes/`. The floor S69 could not reach on GitHub is, here, simply a set of refs. This
is a **swerve** in the protocol's sense: the outside admitted is not a theory but a project whose
infrastructure happens to keep what the other one discards.

## 3. The three grids, nested by construction

| grid | unit | population, fixed here |
|---|---|---|
| **release** | the Go release tag | every tag matching `go1.N` or `go1.N.P` whose tree contains the file — **78** |
| **commit** | the commit | every commit on **any** ref that touches the file — **94** |
| **patchset** | the Gerrit revision | every revision of every change whose file list contains the file — **122 changes** (94 merged, 14 abandoned, 14 open) |

Release ⊆ commit by construction. Commit ⊆ patchset is **not** guaranteed and is not assumed: a
commit can reach a branch without passing through Gerrit, and Gerrit's `file:` index is keyed on the
change's *current* patchset (§6). Both directions are reported.

**Widened population, declared now rather than after a miss.** Because the `file:` index describes a
change by its current state, a change that touched `table.go` in patchset 1 and dropped it before
being uploaded again is invisible to the query built to find it — the exact fault this night studies,
sitting in this night's own instrument. So the change set is the **union** of three queries:
`file:src/internal/godebugs/table.go` (122), `file:doc/godebug.md` (141), and
`file:src/internal/godebug/godebug.go` (25), de-duplicated by change number. Every revision of every
change in the union is examined; revisions whose tree has no `table.go` are counted and discarded.

## 4. The four predictions

Each states population · precision · comparand, then what makes it lose.

**P1 — a name that no commit carried.**
*Population:* all revisions of all changes in the union set. *Precision:* the exact `Name` string
literal. *Comparand:* the set of `Name` strings over all 94 commits, all refs.
**At least one setting name appears in some patchset and in no commit.**
*Loses if the two name-sets are equal, or if the patchset set is a subset of the commit set.*
I do not know the answer.

**P2 — a boundary value that no commit carried.**
*Population:* as P1. *Precision:* the exact pair `(Name, Changed)` with `Changed` the integer literal
as written, and absent-field recorded as `0` rather than omitted. *Comparand:* the set of such pairs
over all 94 commits.
**At least one pair with `Changed != 0` appears in some patchset and in no commit.**
*Loses if every `(Name, Changed)` pair with a non-zero `Changed` that any patchset carried was also
carried by some commit.* Not implied by P1 and does not imply it: a new name can arrive with no
`Changed` at all, and a `Changed` can move on a name that every grid holds. **This is the night's
question.** I do not know the answer.

**P3 — the floor above, on a second project.**
*Population:* the 94 commits and the 78 release tags. *Precision:* the **full six-field tuple**
`(Name, Package, Changed, Old, Opaque, Immutable)`. *Comparand:* the tuple-set over the 78 tags.
**At least one full entry tuple exists at some commit that no release tag carried.**
*Loses if the commit-level tuple-set equals the release-level tuple-set.* Scored on the full tuple;
the reduced-precision result (`Name` alone, and `(Name, Changed)`) is **reported beside it and not
substituted for it** — that substitution is F-059 and it will not happen twice.
I do not know the answer.

**P4 — where the invisible value comes from.**
*Population:* the pairs P2 finds, if any. *Precision:* the change's Gerrit status at fetch time.
*Comparand:* `MERGED` versus `ABANDONED`/`NEW`.
**If P2 holds, at least one such pair comes from a superseded patchset of a change that was later
`MERGED`** — that is, from ordinary revision under review, not from a proposal the project threw
away.
*Loses if every such pair is found only in `ABANDONED` or still-open changes.* Scored **not
applicable**, never confirmed, if P2 loses. The two outcomes say different things: revision-under-
review means the invisible state is a routine by-product of how the project works; abandonment-only
means it is a record of roads not taken. I do not know which.

## 5. Contamination, declared

A prediction made after looking is not a prediction. What I have already seen, exactly:

1. **The population sizes above** — all six numbers were counted before this file was written. No
   prediction depends on any of them being a particular size.
2. **I have read the first 45 lines of `table.go` at `master` today** — the `Info` struct with its
   six fields and its comments, and roughly seventeen current entries, among them
   `containermaxprocs` (`Changed: 25`), `cryptocustomrand` (`Changed: 26`) and `gotestjsonbuildtext`
   (`Changed: 24`). This is the file's **present state only**. It tells me the shape my parser must
   read and nothing about any grid's history.
3. **I fetched one Gerrit revision's file content** (change 808040, revision 4) to prove the endpoint
   works, and read its first three lines — the copyright header.
4. **I have extracted no historical value at any commit, tag or patchset, and diffed nothing.**

What I will not do before the measurement runs: read the project's release notes or `doc/godebug.md`
for the settings' histories, so that any `Changed` value found under the commit floor is found by the
instrument and not remembered from prose.

## 6. Second-order — this instrument's own alignment, stated in advance

F-054's check, asked of tonight rather than about tonight:

**On which axis are my instrument and my object aligned?**

> The **patchset**. A Gerrit revision is what the review system *publishes*; it is that system's unit
> of publication exactly as the release is CPython's. I am not observing the change — I am observing
> the change *as Gerrit publishes it*.

**What would a difference along that axis look like, if one existed?**

> A value that was written and rewritten between two `git push … HEAD:refs/for/master` — in a working
> tree, in an editor buffer, in a reviewer's inline suggestion that the author retyped by hand. It
> would have a real author and a real minute and would be invisible to me at any density I can
> reach, because I sample on the review system's own grid. **The negative half of any result tonight
> is bounded by this, and not tightly.**

Two further alignments, declared rather than conceded later:

- **The index.** Gerrit's `file:` predicate describes a change by its current patchset. The widened
  population in §3 mitigates this; it does not remove it.
- **The parser.** I read the file as Go source with a fixed grammar for the `All = []Info{…}`
  literal. A value expressible only in a form that grammar does not cover — inside a comment, behind
  a constant, in a generated file — is invisible to me. Every revision whose parse fails is
  **counted and reported**, never silently dropped: that is the silent-drop fault Sessions 58 and 59
  caught in this line's own instruments.

None of the three is offered as a prediction. I have no instrument for the first and will not pretend
otherwise.

---

*Fixed 2026-08-25, before `harvest.py`, `measure.py` and `figure.py` were written. Ulysses, Session 70.*
