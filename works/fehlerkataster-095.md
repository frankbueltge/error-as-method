# Fehlerkataster — 095

**Ulysses (the nightly line) · Session 147 · 2026-10-22**

Entries **F-302** to **F-305**. Previous file: `works/fehlerkataster-094.md` (Session 146). The night:
`journal/2026-10-22.md`, experiment 33, *Every Column True* (`works/2026-10-22-every-column-true/`).

Four entries, all the practice's.

---

## F-302 — the design left the siblings in the packet, and counted only words, memory and table

**What happened.** The pre-registration named three routes to a refusal: the page's words (P was there to rule
them out), the judge's knowledge of the material, and the table (WT). It put each work's true page and its four
dealt copies in the same packet, as experiments 31 and 32 had done. W used the packet. Two of its nine refusals
in K rest on nothing but a comparison (*"compared with the correct versions, the poor-rated arcs have moved"*;
*"the layout is the same as W03, but the ratings are attached to the wrong bridges"*). Of G's 20 reasons, 7 cite
another page, and of the practice's own, 14.

**Whose error.** The practice's, in design. It is F-300's error again in a new place. Last night the design left
out the page's own words as a source of the norm, tonight the page's siblings. Session 146 had a hint: W read the
figure 2,729 off the true pages in its packet, and W1 was added for that reason. The night's question still has an
answer, because P rules out the words. But memory and siblings are not separated, and `S147.SIBLINGS` says so.

## F-303 — the practice passed four lying pages as works, a third time

**What happened.** `practice-verdict.json` (committed `1414979`, before any coder) passed six dealt pages as works:
those where only ratings, condition, length, traffic or a crossing's name was dealt. W refused four of them (c1o2,
c2o1, c3o2, c4o1), each for a misstatement it could see. The practice refused the ten pages whose map had lost its
place, and W agreed on all ten.

**Whose error.** The practice's. The split of *works* from *true* (F-294, F-301) held again: the practice refuses a
page whose form fails and passes one whose form holds while it lies. It is entered a third time because Session
148 is to rule on that split. Tonight's evidence is that the family's judge has no such split.

## F-304 — the key was on disk, unopened, when the practice made its blind calls

**What happened.** `make_packets.py` writes `coder/key.json` when it builds the packets. The practice made its
blind calls (H) after that, and committed them (`588612d`) in the same commit as the key. It did not open the key
before the calls were written. Nothing in the record can prove this. The order of commits shows only that the calls
were not changed after the key was read.

**Whose error.** The practice's, in procedure. The fix for the next blind call by the practice is for the key to be
written to a place outside the repository, and for it to be moved in after the calls are committed.

## F-305 — the practice predicted that single-column lies would pass the guesser, while making the same calls itself

**What happened.** P3 predicted that G would call at most half of the changed one-column copies *dealt*. G called
10 of 12. The practice, guessing blind on the same pages, called 10 of 12 as well, most often by setting a page beside
its siblings. Its prediction counted the page alone. Its own perceiving did not.

**Whose error.** The practice's. It predicted from the page as one work is shown to one viewer. In the event it
perceived as its arrangement let it: twenty pages at once.
