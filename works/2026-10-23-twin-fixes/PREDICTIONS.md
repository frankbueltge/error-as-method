# Experiment 36, *Twin Fixes* — predictions and scoring rules

Fixed by the practice (Session 152, 2026-10-23) **before any maker ran**, and committed before the rooms were opened.

## The arrangement

- 24 places drawn by seed 152 from GeoNames `cities15000` (`sources/cities15000-columns.tsv`, CC BY 4.0): four per
  continent (AF, AS, EU, NA, SA, OC by GeoNames' `countryInfo.txt`), population 20,000 to 200,000, both coordinates
  printed by GeoNames to five decimals, and **no other place of the file within 15 km**, so that a pin near the town
  can only mean that town.
- Each place has three keys (`prepare.py`):
  - **E**, the gazetteer's own string, as GeoNames prints it;
  - **D**, the same point rewritten in degrees, minutes and seconds — a new string for the same place, within 3 m;
  - **T**, the **twin**: the point moved 400 to 800 m on a seeded bearing and printed like E. The twin's nearest
    place in the file is still the original (asserted in `prepare.py`). To a map of towns, E and T are one pin.
- Before any maker ran, the gazetteer's points were compared with a second human canon, Wikidata's coordinate (P625)
  for the item carrying the same GeoNames ID (P1566) (`canons.py`, `canons.json`, `sources/wikidata-p625.json`, CC0).
  21 of 24 have one. **The median gap between the two canons is 0.38 km; the median twin step is 0.62 km.** Four
  Wikidata points are identical to GeoNames' to the metre (Oliveira, Amargosa, Mirador, Sragen): one canon copied the
  other. So the twin is not inside the canons' own disagreement. It is of the same order, and well under the size of
  a town of 20,000 people. That last clause is **conjecture**: no town boundary was checked.
- **A known confound, written down now.** For the four places above, GeoNames' decimals are exact conversions of
  whole seconds, so their D key (`20°41'47.0"S`) may be the *older* string, the one the canons were copied from.
- Nine fresh makers, no tools. Maker *i* (1 to 9) sees place *j* under key E, D or T by (*i* + *j*) mod 3, the
  order shuffled per maker by the seed. Every place is pinned three times under each key: **72 pins per key.**
- One brief for all (`brief-template.txt`); only the 24 lines differ.

## Scoring (fixed now)

- **normalise**: Unicode NFKD with combining marks removed, lower case, apostrophes, hyphens and full stops to spaces,
  runs of spaces to one, trimmed.
- An answer is split at its **last comma**: before it the town, after it the country.
- **TOWN**: the normalised town equals the normalised GeoNames `name`, `asciiname`, or any of its `alternatenames`.
- **COUNTRY**: the normalised country equals the normalised GeoNames country name, or one of: *usa, us, united
  states of america, america* (United States); *russian federation* (Russia); *turkiye* (Turkey); *png* (Papua New
  Guinea).
- **DIST** (for a TOWN miss): if a place of `cities15000` in the answered country carries the answered town as its
  name, ascii name or an alternate name, the distance from the drawn place to the nearest such place. Otherwise the
  miss is **unplaced**. A TOWN hit has DIST 0.

## The practice's predictions

- **P1 (the test `S151.TWIN` waits for).** T TOWN rate is **at least two thirds** of E TOWN rate. If P1 holds,
  `S151.TWIN` is falsified on this canon. The practice's guess: it holds, at about 60 %. A gazetteer is not a list of
  strings in the way a colour list is: a town's position is learned from many texts that each round it differently,
  so the family should hold a map here, not a table.
- **P2 (string or value).** E and D TOWN rates differ by **less than 10 points**. If P2 fails with D lower, the
  canon is held as a string; if it fails with D higher, the confound above is doing work. Guess: holds.
- **P3 (the map at a coarser scale).** COUNTRY rates under E, D and T lie within **5 points** of one another.
  Guess: holds, near the ceiling.
- **P4 (a check on the design).** E TOWN rate lies between 20 % and 80 %. Guess: even odds; the floor is the risk.
- **P5 (the silence `S151.TWIN` names).** No maker says, unasked, that a pin did not match anything it knew.
  Guess: holds.

What P1 failing would mean: the family names small towns from coordinates by recalling the gazetteer's printed
string, and a step of half a kilometre, which no map of towns can show, takes the name away. What P1 holding would
mean: the twin rule of Session 151 is not a property of the family's channel to a canon, but of the canon's form. A
list that was copied as strings is recalled as strings; a world learned as a world is read as a map.

**What this cannot do.** No person pinned these points tonight. One family of makers, nine instances, 24 places.
`cities15000` is one gazetteer among several; the makers may hold another canon's string, which would read here as
a twin.
