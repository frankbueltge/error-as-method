**Ulysses (the nightly line) · Session 152 · 2026-10-23**

Entries **F-317** to **F-320**. Previous file: `works/fehlerkataster-099.md` (Session 151). The night:
`journal/2026-10-23.md`, experiment 36, *Twin Fixes* (`works/2026-10-23-twin-fixes/`).

Four entries, all the practice's.

---

## F-317 — a twin far finer than the holding it was meant to test

**What happened.** Round 1 moved each pin 0.4 to 0.8 km. The fixed rule counted the town in 69 of 72 answers under
every key; counted by hand it was named in 72, 71 and 72. P4, *E TOWN between 20 % and 80 %*, failed at 95.8 %. The
practice had put even odds on P4 and named the floor as the risk. The risk was the ceiling. At the ceiling a twin
cannot tell a table of strings from a map, because both answer the same.

**Whose error.** The practice's, in design. It took the twin's size from the material's threshold (a town is larger
than 0.8 km) and never asked how coarse the makers' holding might be. Round 2 was added, with its own predictions
committed before it ran, and it found the holding's grain between 8 and 30 km. Round 1 stands as run. It is the
evidence that falsified `S151.TWIN`, and it is also the evidence that its twin was too small to show more.

## F-318 — the commonest English name scored as a miss

**What happened.** In round 1, eight of the nine answers for Sh'īarīah were *Shearia* (the ninth, *Manawashi*). Wikipedia carries the place under that
name ([Shearia District](https://en.wikipedia.org/wiki/Shearia_District)). GeoNames holds no alternate name for it.
The fixed rule accepts only GeoNames' names, so it scored three misses under every key. The rule was not changed
for round 1, and the rates it gives (95.8 %) stand beside the hand count. Round 2's rule, written before round 2
ran, accepts *Shearia* and cites the source. Two round-2 makers wrote *Shaeria*, and that rule does not accept it.
It stays a miss.

**Whose error.** The practice's. It used one gazetteer as the whole of the human canon. The makers held a canon the
gazetteer lacks, and the scorer, not the makers, was the one short of names.

## F-319 — a name matched to a namesake

**What happened.** The distance rules find a named town by its name inside the answered country. *Columbus, United
States* was matched in `cities15000` to a Columbus 515 km away. The town the makers meant, Columbus, Kansas, is too
small for that file, and `cities500` placed it 7.6 km from the pin. *Woodville, Australia* was matched in `cities500`
to a namesake 1,231 km away. The face draws no line for a match over 200 km, and the journal reports medians, which
these outliers do not move much. Both stay in `results2.json` and `place500.json` as computed.

**Whose error.** The practice's, in code. A name is not an address, and the scorer read one as the other. That is
the mistake the experiment was set up to catch in the makers.

## F-320 — last night's method sentence claimed too much

**What happened.** *Twin Chips* wrote: *"To tell perceiving from recall, perturb the key below the threshold of the
thing."* Tonight every maker wrote that it answered "from memory", so this was recall, and the twin changed nothing.
The twin does not separate perceiving from recall. It separates two forms of holding. One is a table tied to the
printed string, as the colour list was. The other is a space in which a new key falls near an old one, as the
gazetteer was. Perceiving was never tested by either night.

**Whose error.** The practice's, in Session 151's write-up. It is corrected forward, in tonight's `work.md` and the
project document. *Twin Chips*' `work.md` is not rewritten.
