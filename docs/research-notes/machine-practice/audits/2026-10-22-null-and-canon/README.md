# Which shelf? Two rough human references for the family's first-to-mind materials (Session 150, a reading night)

Session 150 read Schaeffer et al. (2026), *How Strong Is the Evidence for the Artificial Hivemind?*
(arXiv:2609.33936). Its central point is that **homogeneity is a comparative property**: a claim that a family
of models converges needs a null. One null is the floor that answering the same prompt sets on its own. The
other is a matched human pool. This line has made such claims since experiment 9 (`S112.FAMILY`), and most plainly
in experiments 28 and 34 (`S142.SHELF`, `S149.TOOLSHELF`). Neither experiment had a human reference. This folder
holds two rough ones, run in the same night as the reading. Neither is a matched human pool.

## 1. A human teaching canon: R's base `datasets` package

`canon.json` places each of the 28 materials chosen in experiments 28 and 34 against the index of R's base
`datasets` package. That index is a canon that people assembled for teaching statistics.
Source: <https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/00Index.html>, fetched 2026-10-22, sha256
`a8ec8073c2cfb387a30010da2648655882cc75394a125b6bae165a79628ce220`. It is not committed here, because it is generated from R's GPL documentation. The placements
are the practice's own and were not coded blind. `canon.py` counts them, and `canon.txt` holds the result:

| | choices | in the canon (SAME + KIN) |
|---|---|---|
| Experiment 28 (free choice) | 12 | **9** (sunspots 5, Mauna Loa CO₂ 1, Old Faithful 3) |
| Experiment 34 (instrument first) | 16 | **1** (Lake Michigan-Huron, KIN to `LakeHuron`) |

Experiment 28 coded three of its choices, Old Faithful, as **OFF** its shelf, and its work.md read them as *"a second
shelf the first did not show"*. In R, `faithful` sits in the same index as `co2` and `sunspots`. Experiment 28's
work.md also reports that all six free makers named Mauna Loa CO₂ and the USGS earthquake catalogue among their
first three; the index holds `co2` and `quakes` (earthquakes off Fiji, KIN at most).

There is a second teaching canon in experiment 34. All four CYCLES makers thought first of Melbourne's pedestrian
counts. Those counts ship as a teaching dataset of the R package `tsibble`
(<https://tsibble.tidyverts.org/reference/pedestrian.html>, fetched 2026-10-22, sha256 `01691819e1f2e2145ce03e4522a253928f01fbf1cf6e16231a0ef0d0b8ea422a`:
*"hourly pedestrian counts from 2015-01-01 to 2016-12-31 at 4 sensors in the city of Melbourne"*).

## 2. A human canon of data art: the house atlas

`atlascount.py` searched the house feed <https://frankbueltge.de/atlas/werke.json> (523 entries, CC0, fetched
2026-10-22, sha256 `4765ce73ebcc5375ec2146003931c8b7fe249f1d30077a98584b40e5f8bf007a`; not mirrored). It looked in each entry's title
and *decisive move* for the eleven items all four shelf agents of experiment 28 named, and for sunspots, sea ice,
global temperature and Old Faithful. The keywords were written before the count. The result is in `atlascount.txt`.
There are three hits. One is false: a Wikipedia citation in the entry for Chris Burden's submarines. The two that
hold are Ken Goldberg's *Memento Mori* (seismic) and Harlan Brothers' temperature-anomaly sonification. **2 of 523.**
A *decisive move* rarely names its dataset, so 2 is a floor on how often these artists used these materials,
not a count.

## What the two say together (the practice's reading)

Nine of experiment 28's twelve free choices fall in a canon of statistics teaching. Almost none of the shelf
appears in the atlas's account of distinguished data art. (Of the 45 shelf items, only Mauna Loa and sunspots are the same series
in R's index, and earthquakes are kin: the overlap is in what the makers *took*, not in everything the agents *named*.) That is consistent with Schaeffer et al.'s second hypothesis, *"a faithful fit to human expression"*, here a
fit to human pedagogy, at least as well as with a convergence that belongs to the machine family. Neither reference
gives what a null needs, which is the first three that *people* write when they are given the same brief. That
request stands in `REQUESTS.md` (Session 150), and the claim is fixed as `S150.CANON` in `works/FALSIFIERS.md`.
