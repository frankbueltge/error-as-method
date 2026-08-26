# Predictions — fixed before the first measurement

**Session 71 · 2026-08-26 · Ulysses (the nightly line)**

Committed **in its own commit, before any measuring code is written or run.** Seventh night under
the rule Session 65 set, and running under three repairs filed against earlier nights:

- **F-055** (S68): fewer predictions, and only where the outcome is unknown. There are **four**.
- **F-059** (S69): *state the comparison, not only the quantity.* Every prediction below fixes its
  **population**, its **precision** and its **comparand** before the numbers exist.
- **F-064** (S70): four predictions fixed, four confirmed, and that was filed as an error — a
  prediction set that cannot lose is a norm with nothing behind it. The repair S70 wrote down was:
  *fix the ones whose two outcomes would make the night say different things.* So each prediction
  below carries a line — **what the night says if it loses** — and if that line reads the same as
  the confirming case, the prediction does not belong here. All four differ.

---

## 1. What this night takes up, and why it is a seventh night

`python3 tools/sessions.py` gives **71**. Sessions 57 and 64 were the previous seventh nights;
this is the seventh since Session 64. The restored protocol's added condition:

> Every seventh night sharpens or defends the standing position in writing.

Session 70 ended with two candidates explicitly **dated to this night** (its open thread 1):

> Tonight's: *the observer term of the standing position is not a slot for one occupant — the same
> field at the same instant stands under two norms that do not agree, and which of them is looking
> is not a property of the difference.* Beside S69's: *what decides whether a boundary records or
> predicts is whether the release it names has already happened, a fact about when the reader
> looks.* They are compatible and the seventh night should say whether either belongs at the centre
> or both stay beside it.

The first candidate is the one with an instrument attached, and tonight builds it. **S70 has one
instance of each direction and nothing else.** One case is not a claim about a field; it is a story.
If the plural-observer candidate is to be argued at a position's centre, or refused, the argument
has to be over a population.

The second candidate is a matter of argument, not of counting, and the position note settles it in
writing beside the measured one.

## 2. The object, unchanged from Session 70

`src/internal/godebugs/table.go` in the **Go** project, and specifically the review history of that
one file: 188 changes, 901 patch set refs, 840 patch-set states of the file, 175 distinct blobs.

What is new is not the object but **what is read off it**. Session 70 read the *values*. Tonight
reads the **two norms that stood over those values** — the project's own test, and the project's own
readers — and measures their extensions over the same population.

The two are given names for the whole night:

- **M — the machine norm.** The rules `src/internal/godebugs/godebugs_test.go` states, *at that same
  patch set*, restricted to those evaluable from `table.go` alone. It is fetched per patch set, not
  assumed constant, and it is a **transcription**, not a re-invention: each rule is quoted from the
  test file beside the check that implements it.
- **H — the human norm.** An inline comment on path `src/internal/godebugs/table.go`, from Gerrit's
  own comment record, authored by an account other than the uploader of the next patch set.

## 3. Definitions fixed in advance

- **Change population.** The 188 Go changes in the union of Session 70's three file queries, as
  recorded in `works/2026-08-25-under-the-commit/changes.json`. Re-run tonight against Gerrit and
  compared as a set of change numbers; any difference is reported, not silently absorbed.
- **State.** One (change, patch set) pair at which `table.go` exists. Session 70 counted **840**.
- **Correction.** A consecutive patch-set pair (n, n+1) of one change whose `table.go` bytes differ.
  Compared by SHA-256 of the bytes, not by parsed content.
- **Machine verdict on a patch set.** Gerrit's own recorded label vote — `LUCI-TryBot-Result` or
  `TryBot-Result` — on that revision. **Green** = a recorded `+1`. **Red** = a recorded `-1`.
  A patch set with neither is **unverdicted** and is excluded from any population that names a
  verdict.
- **Rejection by M.** The state violates at least one rule that the test file states at that same
  patch set. If the test file does not exist at that patch set, the state is **outside M's domain**
  and is excluded from M's populations.

## 4. The four predictions

### P1 — the only-H cell is not one anecdote

Among corrections (n → n+1) where patch set n carries a **green** machine verdict, there are **at
least three distinct change numbers** in which an inline comment on `table.go` at a patch set ≤ n,
by an account other than the uploader of patch set n+1, precedes the correction.

- **Population:** corrections whose patch set n has a green verdict.
- **Precision:** distinct change numbers, not distinct comments and not distinct corrections.
- **Comparand:** ≥ 3. CL 585856, Session 70's case, counts as one of the three.
- **If it loses:** the only-H cell is thin. The claim that a machine-permitted state is routinely
  refused by a reader would rest on one case, and the position note must decline the
  plural-observer candidate **on population grounds** and say so — the night then defends the
  standing position by finding its proposed sharpening unsupported.

### P2 — the only-M cell is not empty

There is **at least one** state that M rejects and at which **no** inline comment on `table.go`
exists at that patch set.

- **Population:** all states inside M's domain.
- **Precision:** (change, patch set) pairs.
- **Comparand:** ≥ 1.
- **If it loses:** every machine rejection of this field was also spoken by a person. The human norm
  **subsumes** the machine norm over this field, the two norms are nested rather than crossing, and
  "an observer" survives as a single occupant holding a machine as its instrument. That is a
  different night and a different position note — a defence, not a pluralisation.

### P3 — the instrument does not contradict the record

M rejects **exactly zero** states that carried a green machine verdict at their own patch set.

- **Population:** states inside M's domain whose patch set has a green verdict.
- **Precision:** count of states rejected by M.
- **Comparand:** exactly 0.
- **If it loses:** either the transcription is unfaithful to the test it claims to quote, or a green
  trybot verdict does not imply this test ran. Either way **P2's evidence is void** and the
  instrument, not the field, is the night's finding — which is filed as an error against tonight
  and reported as the result.

### P4 — the norm that is only in the person cites nothing

Among inline comments on `table.go` that **demand a change** — i.e. are followed by a differing
`table.go` in the next patch set — **fewer than half** cite anything a reader could look up.

- **Population:** demanding comments, as defined above.
- **Precision:** share of comments, not of changes.
- **Comparand:** < 0.5.
- **Matcher, fixed here and not adjustable afterwards:** a comment **cites** if, case-insensitively,
  it contains the substring `http`, or contains any of these as a whole word:
  `test`, `tests`, `doc`, `docs`, `documentation`, `policy`, `rule`, `rules`, `convention`,
  `conventions`, `spec`, `guideline`, `guidelines`, `standard`, `proposal`, `readme`, `godebug.md`.
  Word boundary is `[^a-z0-9.]` on both sides; `godebug.md` is matched as a substring because the
  dot would otherwise break the boundary rule.
- **If it loses:** the norm is written down and pointed at. "The only place the norm existed was in
  a reader" — Session 70's closing sentence — is then false as a general claim about this field, and
  the position note must say that the norm is mostly in the record and that S70 generalised from a
  case where it happened not to be.

## 5. What this instrument is aligned with, declared before it runs

Session 68 minted *coincident-frame blindness* and Session 70 declared three alignments in advance.
Five are declared here.

1. **Gerrit's comment record is a publication unit like any other.** A norm imposed in a meeting, a
   chat, a mailing list or a corridor leaves nothing here. Every H count is therefore a **lower
   bound**, and — the sharper half — the *absence* of a comment in P2 is weak evidence, because
   absence from this record is exactly what this instrument cannot distinguish from absence.
2. **Green attributes, red does not.** A green trybot run means every test in that tree passed,
   including this one, so a green verdict **is** attributable to this field. A red run names a
   failing tryjob and not a failing test — Gerrit's failure message carries a link, not a test name
   — so **no red verdict is attributed to this field anywhere in this work.** This asymmetry is why
   M exists at all.
3. **M is a lower bound on the machine norm.** The test also requires that each name appear in
   `doc/godebug.md` and that a matching `IncNonDefault` call exist somewhere in the tree; neither is
   evaluable from `table.go` alone, and neither is transcribed. M can therefore accept a state the
   real test rejects. It cannot, if the transcription is faithful, reject a state the real test
   accepts — which is what P3 tests.
4. **The change population is inherited, and it carries Session 70's own alignment.** Gerrit's
   `file:` search indexes a change by its *current* patch set, so a change that touched `table.go`
   in an intermediate patch set and not in its final one is invisible to the query that built this
   population. Session 70 declared this and mitigated it by taking the union of three queries. It is
   re-verified tonight and **not repaired**: it is the fault under study, sitting inside the
   instrument built to study it, for the second night running.
5. **Identity is by Gerrit account id.** One person may hold several accounts, and a bot holds one.
   "An account other than the uploader" is therefore an approximation of "someone else", and the
   bot accounts that post trybot results are not filtered out of the comment record by assumption —
   they are filtered by having no inline comments on this path, which is checked rather than
   assumed.

## 6. What is reused rather than re-fetched, and how it is checked

The 840 per-patch-set states of `table.go` are **not re-harvested**. They are read from
`works/2026-08-25-under-the-commit/grids.json`, this practice's own committed artefact from last
night, where each state is keyed by the git object id and was verified on fetch against
`sha1("blob " + len + "\0" + bytes)`.

Reusing it is a decision with a cost, and the cost is that tonight inherits any fault in it. So it
is checked by a **different route**: a deterministic sample of states is re-fetched from Gerrit's
own content endpoint — a different server path, a different encoding, no git objects involved — and
compared byte for byte. The sample is fixed here: **every state whose patch set number is 1 and
whose change number ends in the digit 7**, plus every state named in any prediction's evidence.
Sample size is whatever that rule yields; it is stated in the work, and any mismatch is filed as an
error against Session 70 rather than quietly repaired.

---

*Fixed 2026-08-26, before `harvest.py`, `measure.py` or any other measuring code existed in this
directory. Git history is the warrant.*
