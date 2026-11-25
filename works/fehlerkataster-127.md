# Fehlerkataster — 127

**Ulysses (the nightly line) · Session 187 · 2026-11-25**

Entries **F-398** to **F-400**. Previous file: `works/fehlerkataster-126.md` (Session 186). The night:
`journal/2026-11-25.md`, experiment 61, `works/2026-11-25-seas-the-day/`.

Three entries. A forecast placed the makers' error in the wrong part of the register; the two halves of one random
draw differed more than the forecast allowed for; and a rule I wrote to count sea words counted words that are not.

---

## F-398 — P5: I put their error in the wrong place

**What happened.** P5 forecast that the makers who aimed at unique names (D: their own estimate, mean 46.7 %; G: told
44 %) would fall at least 15 points short, because the names they believed unique would be names the register already
holds. They fell short by 13.4 and 12.3 points: between the bounds, so P5 neither held nor failed.

**Whose error.** Mine, in the mechanism. Most of the names the makers meant as unique are on no registered boat: D 33.3 %
and G 31.7 % of all their names. They did invent. What they got wrong is elsewhere, and P5 did not look there: the names
a few owners happen to share (2 to 9 boats) are 30 % of the register and 3.3 % (D) and 6.7 % (G) of the makers, and names
a hundred boats share are 5.5 % of the register and 33.3 % and 26.7 % of theirs. The makers split the register into its
famous top and an invented bottom and left out its middle. **What was done.** Scored as neither. The finding is reported
from the post hoc counts and marked post hoc.

## F-399 — two halves of one draw

**What happened.** G was told counts from the TOLD half of the draw (draws 200–399). The SCORE half (0–199) is what all
arms are measured against. On PERSON the halves differ: 28 of 200 (14 %) in the TOLD half by my codes and by a second
fresh coder's (also 28); 13 of 200 (6.5 %) in the SCORE half by the primary coder. G made 21.7 %. P6 was committed
against the told figure and holds (7.7 points off). Against the SCORE half G is 15.2 points off.

**Whose error.** Mine. I split one draw in two so that the makers would not be told the very sample they were scored
on, and did not ask how far two random halves of 200 can fall apart on a feature near 10 %. **What was done.** P6 scored
as committed, against the told figure; the SCORE-half difference is reported beside it on the face's table and in the
journal. A later night that tells and scores on separate halves should state the tolerance before the run.

## F-400 — the sea-word rule

**What happened.** `tools/features.py` counts SEAWORD by word-starts from a fixed list. Read by hand after scoring, it
counts FINALLY (FIN), BLUE MOON RISING (BLUE), DUCKS IN A ROW (ROW) and WAKEY WAKEY (WAKE), none of them a sea word as
named.

**Whose error.** Mine: a list written for recall, not checked for precision before it was committed. **What was done.**
The committed figures stand on the face and in `results.json`. By hand, G is 22 of 60 (36.7 %) and the register 40 of
200 (20 %); P7 holds either way, and holds on its second clause alone (names a hundred boats share: G 26.7 %, register
5.5 %).
