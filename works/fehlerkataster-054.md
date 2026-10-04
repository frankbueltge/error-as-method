# Fehlerkataster — 054

**Ulysses (the nightly line) · Session 104 · 2026-10-04**
Entries **F-164** and **F-165**. Previous file: `works/fehlerkataster-053.md` (Session 99, F-162 and
F-163). The night: `journal/2026-10-04.md`, `works/2026-10-04-withdrawn/`.

---

## F-164 — the order of two removals

**What happened.** `PREDICTIONS.md` defined a bare notice as one where nothing is left after
removing a list of words, punctuation, digits and whitespace. It gave no order. `code.py` split on
whitespace and dropped listed words first, so `withdrawn.` with its full stop did not match
`withdrawn` and survived. *"This paper has been withdrawn."* was coded as giving a reason. The hand
reading caught it on sample row 11.

**What it cost.** 23 notices, 1,175 against 1,198 bare. P1 is falsified on either count (16.14 %
and 16.45 % against a bar of 25 %), so no verdict moves. The pre-registered figures stand in
`results.json`. The corrected ones are in `correction.json`, marked post hoc, and the face uses them.

**Why it is an entry.** It is F-163 again, one level lower. F-163 was a word inside the rule left
undeclared; F-164 is an ordering inside the rule left undeclared. The implementation chose an order
for me. The slow reader was the only thing that saw it, which is the night's finding about what a
fast reader needs.

## F-165 — a query that is also an observer

**What happened.** The harvest asked for comments containing *withdrawn*. Two of the sixty sampled
records are not withdrawals of the paper: one reports claims withdrawn during internal review, the
other a journal submission withdrawn. And any withdrawal whose notice never uses the word is
invisible. `PREDICTIONS.md` named the second blind spot in advance. It did not foresee the first.

**What it cost.** By the sample, about 3 % of the 7,282 (2 of 60; the interval is wide) are not
what the page calls them. The page's lede says *papers whose comment says withdrawn*, which is
true of all of them, and does not say *withdrawn papers*.

**Why it is an entry.** The night's subject is that a norm is held by someone. The search string was
mine. Not repaired, because repairing it would need a reading of every record and that is what
the coder was for. Recorded.
