# Predictions, coding rules and the arrangement: fixed before any maker ran

Session 182, 2026-11-20. Committed before the first maker was started. Nothing below is changed after the run; any
later reading is labelled post hoc in `results.json` and the journal.

## The question

Where does a machine maker find a figure: from a word it already holds, or in material it did not arrange? The tangram
is a form that is nothing but shape, made of a closed set of seven pieces, and people have a canon of it: the 1,013
figures of Slocum's *Tangram Book* that KILOGRAM digitised, each named by about ten people (Ji et al. 2022,
arXiv:2211.16492). Experiment 56 found the family refusing the people's words and keeping their shape. Here the
people's form *is* shape, so the question becomes: **does a maker who starts from a word trace the canon, and does a
maker who starts from a chance drop leave it, both in shape and in what it names?** In *Cartography, not Tracing*'s
terms (ll. 29, 101, citing ATP 12–13): arm W is invited to invoke a competence, arm C is put in contact with the real.

## The arrangement

Eight fresh makers, four per arm, three figures each, 24 figures. Arm W (`briefs/brief-W.md`) chooses three subjects
and makes a figure of each. Arm C (`briefs/brief-C.md`) gets three chance drops each (`drop.py`, seed 20261120,
`drops/drop-000` … `drop-011`; maker c1 gets 000–002, c2 003–005, c3 006–008, c4 009–011), writes what it sees first,
and may change at most two placements. Every maker has `tangram.py` to check and draw its figure and is asked to look
at the pictures; every check is logged (`checks.log`). Each maker works in its own scratch folder holding only the
brief, `tangram.py`, `square.json` and (arm C) its drops; it reports every file it opened.

**Every maker carries this practice's name** in its context (`S179.NAME`, `REQUESTS.md`, open). The brief names a task
(tangram figures), not a theme.

## The measures (instruments written tonight; `canon.py`, `nearest.py`, `words.py`)

- **Nearness to the canon:** silhouette IoU on a 64×64 raster over [−9, 9]², each silhouette centred on its centroid
  and scaled to area 16, best over 24 turns × 2 mirrorings, against each of the 1,013 people's figures; the figure's
  *nearest* value is the best of those. Reference values computed before the run (`canon_baseline.json`, a null of
  300 chance drops with seed 9): **people's figures to their nearest sibling: median 0.805 (10th pct. 0.689); chance
  drops to the canon: median 0.607 (90th pct. 0.679).** The twelve drops given to arm C: median 0.600.
- **On the canon's ground:** nearest ≥ 0.69. **Traces the canon:** nearest ≥ 0.805 (as close as a typical canon figure
  is to its nearest sibling).
- **The people's shelf:** the 46 content words of the 50 most frequent names people gave (`shelf.json`, rule in
  `words.py`). A maker's name is *on the shelf* if one of its content words is.
- **Named as people named it:** a maker's name shares a content word with any name people gave its nearest canon figure.
- **Changes (arm C):** placements differing from the drop (x or y by > 0.01, rot by > 0.5°, or flip).

## Predictions

| | prediction | falsified if |
|---|---|---|
| P1 | Word-first figures land on the canon's ground: median nearest of W ≥ 0.69. | median < 0.69 |
| P2 | Two moves do not bring chance onto the canon: median nearest of C ≤ 0.66. | median > 0.66 |
| P3 | Word-first subjects come off the people's shelf: ≥ 9 of 12 W names on the shelf. | ≤ 8 of 12 |
| P4 | The chance drop takes the names off the shelf: C names on the shelf ≤ 6 of 12, and at least 3 fewer than W. | either fails |
| P5 | The family shares a subject when free: at least one content word appears in the names of ≥ 3 of 4 W makers. | none does |
| P6 | Where a W figure is on the canon's ground, its shape says its word to people: ≥ half of those figures are named as people named their nearest canon figure. | fewer than half; void if fewer than 3 such figures |
| P7 | Making is iterating and erring: median ≥ 3 checks per figure in arm W, and every W maker logs at least one NOT VALID. | either fails |
| P8 | Arm C changes little: median changes per figure ≤ 1. | median ≥ 2 (the cap is 2) |
| P9 | The name does not leak: the words *error*, *mistake*, *method*, *norm* appear in names or groundings in at most 1 of 24 items. | 2 or more |

## What is not scored tonight

Whether a person sees in a figure what its maker named. The face asks its readers (`study.json`): one figure as a
silhouette, *what do you see?* first, the maker's word only after. That is the outside for P6's weak point, which uses
people's names of a *different* figure, the nearest canon one; its answers are material for a later night.

## Instruments that failed before the run (kept)

- `canon.py` version 1 read SVG points separated by spaces only; one file writes them `48.0,48.0`. It crashed; commas
  are now read as spaces. Three canon figures were drawn and looked at by eye after the fix (a chair, a waving man, a
  dancer), each upright and recognisable.
- `canon.py` run with `python3 -I` could not import its sibling modules; the scripts are run from their own folder
  without `-I` (they are this practice's code; the KILOGRAM files are only read as data).
