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

---

# Round 2 — added after round 1 was scored, before any round-2 maker ran

**Why a second round.** Round 1 came back at its ceiling: TOWN 69 of 72 under E, D and T alike (`results.json`).
The three misses per key are the same answer, *Shearia*, the English spelling under which Wikipedia carries the
place ([Shearia District](https://en.wikipedia.org/wiki/Shearia_District)); GeoNames holds no alternate name for
Sh'īarīah, so the fixed rule scores it a miss. A twin of 0.6 km cannot tell a table from a map when the makers'
holding is much coarser than 0.6 km. So round 2 asks where the holding stops: **how far can a pin move before the
makers stop naming the town?** Nine new fresh makers, the same brief, the same 24 places.

- Keys (`round2.py`, seed 1522): each place moved **2, 8 or 30 km** on a seeded bearing, printed like E. Maker *i*
  sees place *j* at step (*i* + *j*) mod 3: 72 pins per step. No round-2 maker has seen round 1.
- At 30 km, seven places fall **captured**: another `cities15000` place lies within 10 km of the moved pin
  (Cláudio 1.3 km from Oliveira's pin, Onitsha 1.0 from Ogwashi-Uku's, San Diego 5.1 from Turrialba's, Ubaíra 6.0
  from Amargosa's, Teotihuacán de Arista 6.7 from Calpulalpan's, Maitland 9.4 from Cessnock's, Lautoka 9.95 from
  Nadi's): 21 pins. At those pins the original town is the wrong answer.

**Scoring, fixed now.** As round 1, and also:
- **ORIG**: the answer is the original town (TOWN as above; for round 2 *Shearia* also counts for Sh'īarīah, on the
  source just cited).
- **NEAR**: the answer is the `cities15000` place nearest the moved pin, when that is not the original.
- **ERR**: if the answered town is a `cities15000` place in the answered country, the distance from the pin to it.

**Predictions.**
- **Q1.** S2 ORIG ≥ 90 %.
- **Q2.** S8 ORIG ≥ 75 %.
- **Q3 (is the neighbour on the map?).** On the 21 captured pins, NEAR ≥ 50 % and ORIG ≤ 20 %. If ORIG is high, the
  holding is a set of anchors with wide basins — a tracing with a tolerance, not a map.
- **Q4.** Median ERR at S30 ≤ 15 km.
- **Q5 (silence).** Fewer than 5 of the 72 S30 answers say, unasked, that the pin lies outside any town.

The practice's guess: Q1, Q2 hold; Q3 holds for Onitsha and fails for the small captures; Q4 holds; Q5 holds.
