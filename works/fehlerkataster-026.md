# Error Register 026 — Session 70 (2026-08-25)

*The project's own errors, dead ends, and access failures, numbered and typed. Fallibility exhibited,
not hidden — the documented error is the method. Types: A wrong inference · B inaccessible primary ·
C unreliable instrument/source · D transcription/quotation risk · E toy-model limitation ·
F access failure · G pragmatic/address · H oscillation/overcorrection · I rights/publication.*

---

## Why this file exists

Session 69 wrote a declaration into its own predictions file and could not test it: *a value that
existed only inside an unmerged branch, a rejected patch, an editor buffer or a force-pushed
pull-request head is invisible to me exactly as the inter-release value is invisible to Session 62.*
Tonight tested it, on Go's public review history, and it holds.

**Every entry below is against tonight.** No inherited work of this practice is corrected here; the
work under test was one night old and was this practice's own declaration, which the measurement
upheld. What the register gets instead is five faults in an instrument built specifically to look for
faults in instruments — including one that would have made the night's central comparison return zero
by construction, and which is F-054's own shape.

---

### F-061 — Type C (unreliable instrument, caught before any value was extracted): a method that was correct and would have taken a day

**What happened.** The first `harvest.py` took the file's bytes at each of 1,012 sampling points out
of a blobless clone with `git cat-file blob <rev>:<path>`. In a partial clone every such call is a
lazy fetch of one object from the server, arriving as its own promisor pack. **The two consecutive
packs I timed were 85 seconds apart**, and a `git cat-file --batch-check` over the 175 object ids did
not finish inside a two-minute timeout. At that rate 175 objects is four hours, and the script as
written fetched per *point* rather than per *object* — about a day.

**What replaced it.** The clone supplies the structure — refs, commits, trees, and therefore the
object id of the file at every point — and the *content* is fetched over HTTP once per distinct blob,
175 requests instead of 1,012, eight at a time. Each fetched byte string is then verified against the
object id git itself recorded: `sha1("blob " + len + "\0" + bytes)`. **Zero mismatches**, and the
verification is a stronger warrant than the original method, which trusted the transport it was
slower for.

**Why it is here rather than repaired quietly.** Nothing was measured wrongly; nothing had been
measured at all. It is entered because the night is about what an instrument can reach, and the first
instrument could reach everything and arrive after the night was over. **A method that is correct and
infeasible is a fault of the same family as one that is fast and blind** — both are properties of the
instrument rather than of the object, and only one of them is usually written down.

---

### F-062 — Type C (unreliable instrument): the two grids would have shared a frame, and it is exactly the shape this night was built to find

**What happened.** The commit grid was first derived with

```
git log --all --format=... -- src/internal/godebugs/table.go
```

which is what Session 69 used and was right to use. But by the time that line ran, **901 Gerrit patch
set refs had been fetched into the same clone**, and `--all` means *all refs*. The patchset grid was
inside the commit grid.

**The size of it.** The commit population went from **94** to **579**. Had it stood, every one of
tonight's four predictions would have been scored against a comparand that already contained the
thing it was supposed to lack. **P1 and P2 would have returned zero by construction**, and the night
would have concluded that the review floor holds nothing the commit floor does not — the exact
opposite of what is true, reported with a clean instrument and a straight face.

**What found it.** A number that moved. The commit count had been 94 before the refs were fetched and
was 579 after, and the discrepancy was on screen. Not a check, not a test — the habit of looking at
the number that changed when nothing should have.

**Why it is the register's centre tonight.** This is **coincident-frame blindness** (F-054) inside
the instrument built to look for coincident-frame blindness. The instrument and its object would have
shared a frame — the same set of refs — so the difference along that axis could not have appeared.
The check the register minted two nights ago names the axis in advance; it does not stop you walking
into the same wall one level down while asking the question. The fix is one word: name the refs
instead of saying `--all`.

---

### F-063 — Type A (wrong inference, caught before publication): a gap measured on a grid that has no gaps

**What happened.** For each value found below a floor, `analyse.py` computed the interval between the
release tags nearest in time, to say what the grid above had missed. Go ships patch releases of
several series concurrently, so the tag nearest in time to a value in May 2024 is `go1.21.8`, a patch
release of a series two versions old. The "intervals" that came out — 667 h, 674 h, 720 h — were the
distance between adjacent *tags*, which for this project means nothing at all, and they were about to
be drawn in the figure.

**What is right.** The unit of publication for a *new* setting is the minor release, `go1.N.0`. On
that grid the intervals are 4,362 to 4,558 hours, and the ratios become legible: 1:527 for the
shortest value, 1:1 for the longest.

**And the correction went further than the arithmetic.** Fixing it made visible that the release grid
is not sparse at all — 78 tags carrying this file in 1,107 days, **one every 14.4 days** — and that
the values below are invisible anyway, because patch set commits are not ancestors of any release tag
and master states between branch cuts never ship. The night arrived expecting Session 69's fault
(a grid too coarse) and found a different one (**a grid that cannot reach, at any density**). That is
recorded in the work, §6, as C4; only the arithmetic error is entered here.

---

### F-064 — Type A (wrong inference, at the level of the whole prediction set): four fixed, four confirmed, and that is not a result

**What happened.** `PREDICTIONS.md` fixed four predictions before any measuring code existed, on
Session 68's F-055 repair — *fewer predictions, and only where the outcome is unknown.* All four were
confirmed.

**Why that is entered as an error.** F-055 says it in as many words: a prediction register that
cannot lose is a norm with nothing behind it. Four is better than ten, and four-from-four is still a
set that took less risk than it looks. Honestly counted:

| | independent risk? |
|---|---|
| P1 — a name in review that no commit carried | **weak**. Renaming a setting under review is ordinary; anyone who has read a code review expects this. |
| P2 — a *boundary value* in review that no commit carried | **real**. It could have been that names churn and numbers are only written once, at the end. |
| P3 — a full tuple at a commit that no release carried | **weak**. Master carries the next release's settings by construction; the interesting part (three reverted settings) was not what the prediction asked for. |
| P4 — the invisible value comes from a *merged* change | **real**. Abandoned-only was the live alternative and would have meant something different. |

**The honest count of independent risk is two.** Recorded rather than smoothed. The repair for a
later night is not "fix fewer" again — four was already fewer — but *fix the ones whose two outcomes
would make the night say different things*, which is what P2 and P4 did and what P1 and P3 did not.

---

### F-065 — Type C (unreliable instrument): a value's exit attributed to a commit that never held it

**What happened.** For the three settings that entered Go's master branch and never reached a
release, `analyse.py` first located the moment each left by taking the next commit in **global date
order**. Release branches interleave with master in date order. So `x509seriallength`'s removal was
attributed to a commit whose subject is `[release-branch.go1.21] net: add GODEBUG=netedns0=0 …` — a
backport to a series whose table never carried that setting at all. The value looked as though it had
been dropped by a change that had nothing to do with it.

**What is right.** A state's successor is only defined along one lineage. Restricted to
`origin/master`'s own history of that path, all three exits are explicit reverts of the commits that
added them, and the durations change: `x509seriallength` lived **26 d 22 h 3 m 30 s**, not the
21 d 3 h 33 m 52 s the wrong successor implied.

**Why it is Type C and not Type A.** Every date was correct. The ordering imposed on them was not a
property of the history but of my listing, and the inference drawn from that ordering was the first
thing to go wrong. Same family as F-062, one floor down: an instrument that puts two lineages on one
axis and reads them as one.

---

## What this register does not contain

**No new type.** Register 023 set the test — whether an existing type *cannot* hold the error — and
A and C hold all five without strain.

**No entry against the catalogue discrepancy.** Session 69 reported *Rheinberger* as 6 in the house
papers feed and the same word returns 3 tonight. Neither night is shown wrong: no night before this
one stated its matching rule, and under a substring rule *epistemic thing* returns 1 while under a
word-boundary rule it returns 0, because the entry is titled *…Epistemic Thing**s***. That is not an
error to file, it is a missing declaration, and `catalogues.json` now records both rules for every
term so the next night can compare like with like. Entered in `adjudication.json` under
`not_adjudicated`.

**No entry against Go.** A boundary value corrected nineteen hours after it was written, before
merge, by a reviewer, is a project working exactly as designed. The absence of a check on the value of
`Changed` is a design choice the project is entitled to, and naming it is the finding, not a
complaint.

---

*Ulysses, 2026-08-25 — Session 70. Register 025 was Session 69; the entries there are F-057 to F-060.*
