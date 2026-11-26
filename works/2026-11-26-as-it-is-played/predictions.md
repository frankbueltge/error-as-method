# Predictions — experiment 62, Session 188, 2026-11-26

Written and committed before any selector ran.

**The material.** The Lichess open database, standard rated games, October 2026 (CC0,
`https://database.lichess.org/standard/lichess_db_standard_rated_2026-10.pgn.zst`). This session read the first
40 MiB of the compressed file: 128,323 complete games played 2026-10-01 00:00:25 to 01:46:39 UTC
(`tools/frame.py`, `people/frame-summary.json`). 400 drawn by seed 188 (`people/drawn-400.json`); draws 0–59 are
the POOL the selectors see (`tools/pool.py`, `people/pool/`), with player names, URLs and clocks removed. Every
feature below is computed from the record (moves replayed with python-chess); nothing is hand-coded, so there is no
coder this time.

**The pool of sixty** (this session has read it and is not blind to it):

| feature | of 60 |
|---|---|
| ended by resignation | 23 |
| ended on time | 18 |
| ended by checkmate | 16 (26.7 %) |
| draw | 3 |
| blitz / bullet / rapid / ultrabullet | 28 / 22 / 9 / 1 |
| SHORT: over before move 15 (untold) | 8 (13.3 %) |
| LONG: more than 50 moves (untold) | 4 |
| HIGH: mean rating of the two players 2000 or more (untold) | 10 |
| median length | 30.5 moves |
| mean of the two ratings, averaged | 1662 |

The 400 drawn: resignation 163, time 132, checkmate 90, draw 15; median 31 moves; mean rating 1665.

**Design.** Eighteen fresh selectors of one family, folders outside the repository (absolute paths), carrying this
practice's name (`S179.NAME`). Each reads the same sixty and chooses eight for a page where only the eight are shown,
replayed on small boards. Every version kept.
- **A** (six), `briefs/brief-A.md`: eight that show how people play chess online today, *as it is*.
- **C** (six), `briefs/brief-C.md`: the eight *most worth showing*. The specimen asked for outright, to see whether
  "as it is" moves the selection at all.
- **B** (six), `briefs/brief-B.md`: A's brief, plus the pool's counts of endings and speeds and the instruction to
  keep those proportions. Experiment 61's G arm, moved from making to choosing.
After "done", each answers `briefs/question.md` (a fair picture? and two estimates, without counting again).

**The question.** Experiments 57 and 61 found that the maker's type gave way only to material it did not arrange, or
to numbers, and only where the numbers counted. The obvious method a researcher reaches for next is not to make at
all: to let the machine collaborator choose from the people's own material (found footage, the archive, the
ready-made). Does the type return through selection? And told the proportions, does it go where they do not count, as
it did in making?

**The null.** A random eight from the sixty. Its expected shares are the pool's; its spread is simulated
(`tools/score.py`, 100,000 draws). Shares are over each arm's 48 final picks, repeats counted.

## Predictions

- **P1 (the specimen through "as it is": checkmate).** A's 48 picks are at least **41.7 %** checkmates (pool 26.7 %).
  *Falsifier:* 31.7 % or less.
- **P2 (time).** A's picks end on time on at most **20 %** (pool 30 %). *Falsifier:* 27 % or more.
- **P3 (the unfinished).** A's picks are SHORT on at most **3 of 48** (6.3 %; pool 13.3 %). *Falsifier:* 5 or more.
- **P4 ("as it is" does not undo the specimen).** A's checkmate share is at most 15 points below C's. *Falsifier:*
  25 points or more below.
- **P5 (numbers held).** At least **5 of 6** B selectors keep the endings within a total absolute deviation of 2.0
  games from eight times the pool's shares (resignation 3.07, time 2.4, checkmate 2.13, draw 0.4). *Falsifier:* 3 or
  fewer.
- **P6 (the type goes where the numbers are silent).** B's picks are SHORT on at most **3 of 48**. *Falsifier:* 5 or
  more.
- **P7 (one observer).** The median overlap between two A selectors' eights is at least **2 games** (a random pair:
  about 1.07). *Falsifier:* 1 or fewer.
- **P8 (knowing beside choosing).** The eighteen selectors' median estimate of SHORT games in the sixty lies between
  **4 and 12** (true: 8). *Falsifier:* below 2 or above 15.

Recorded, not predicted: mean rating and HIGH share per arm; LONG; speed shares in A and C; first version against
final (iterating); the answers to "a fair picture?" beside each selector's measured distance from the pool; which
games are chosen most often.

Neither held nor failed means the result lies between a prediction and its falsifier.
