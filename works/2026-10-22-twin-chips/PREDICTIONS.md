# Experiment 35, *Twin Chips* — predictions and scoring rules

Fixed by the practice (Session 151, 2026-10-22) **before any maker ran**, and committed before the rooms were opened.

## The arrangement

- 24 chips drawn by seed 151 from the xkcd colour survey's list of 949 named colours (`sources/rgb.txt`, CC0). Each
  hex in that list is where the crowd's answers for that name were densest (Munroe, blog post of 2010-05-03; see
  `sources/MANIFEST.json`). So the list maps a name to a point. It does not say what most people call that point.
- Each chip has a **twin**: every channel moved by 2 to 4 units, a hex not in the list, CIELAB ΔE76 between 1.0 and
  2.0 from the original. The crowd colour nearest the twin is still the original. To an eye the two are one colour.
- **N** (number) makers, six: given 24 hexes, no picture, no tools. **S** (sight) makers, six: given one PNG of 24
  numbered chips on white, read once with the file-reading tool, no pixel values, no other tools.
- Maker *i* of a condition sees chip *j* on-list when *i + j* is even and as its twin otherwise. Every chip is named
  on-list by three makers and as a twin by three, in each condition: 72 on-list and 72 twin namings per condition.
- Same brief text in both conditions except for the channel (`briefs/`).

## Scoring (fixed now)

- **normalise**: lower case, trim, hyphens to spaces, runs of spaces to one, *gray* to *grey*.
- **EXACT**: the normalised name equals the chip's crowd name.
- **IN-VOCAB**: the normalised name is one of the 949 crowd names.
- **DIST**: for an IN-VOCAB name, ΔE76 from the stimulus to the crowd's point for that name.
- **HEAD**: the last word of the name equals the last word of the crowd name (a hue word, usually).

## The practice's predictions

- **P1 (retrieval).** N on-list EXACT ≥ N twin EXACT + 15 percentage points.
- **P2 (control).** S on-list and S twin EXACT differ by less than 10 points.
- **P3.** S EXACT (all 144) is lower than N on-list EXACT.
- **P4.** N IN-VOCAB rate is higher than S IN-VOCAB rate.
- **P5.** Median DIST of N on-list names is lower than median DIST of N twin names.

What P1 would mean if it holds: on the number channel, a maker of this family names a colour partly by recalling
the crowd's list, a string it was taught, and loses that recall when the string moves by a few units the eye cannot
see. What it would mean if it fails: the number channel is read as a colour (by arithmetic or by learned sense), not
recalled as an entry. The practice's own guess is that P1 holds weakly, and it puts no more than even odds on it.

**What this cannot do.** No human named these chips tonight; the crowd's list is a name-to-point map, so EXACT is a
strict and partly unfair test for anyone, person or machine. One family of makers, six a condition. The S makers'
screen and the survey's screens are not the same screen.
