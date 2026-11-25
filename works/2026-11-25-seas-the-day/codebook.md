# Codebook — experiment 61, fixed before any maker ran

Every name, the people's and the makers', is coded on seven features. Three are coded by hand, four by
`tools/features.py`. A name can carry several.

## By hand

- **PUN.** The name plays on sound or double meaning. It counts when (a) a word is replaced by a sound-alike
  or respelled into one (REEL for real, KNOT for not, SEA for see, SAIL for sale, BUOYS for boys, MOOR for more,
  NAUTI for naughty, N2 DEEP); (b) a sea, boat or fishing word is fused into another word (SEADATION,
  LEGA-SEA, REELAXIN); or (c) a stock phrase is used whose literal sense is about water, wind, boats or
  fishing while its ordinary sense is something else (ON THE ROCKS, WINDFALL, OUTCAST, FISHER OF MEN).
  A respelling with no second meaning (TRU LUV, SOAKITIN) is not a pun. A joke name with no play on sound or
  sense (THE OFFICE, BANKRUPT) is not a pun.
- **PERSON.** The name contains a person's given name or nickname, a real person's or a fictional
  character's (ISABELLE, MISS MAC, WENDY LU, BLACK BETTY, FIGARO, DOC HOLIDAY). Gods, myths, animals and
  places are not persons (PEGASUS, LORELEI, AEOLUS). A word that is also a name is coded only when nothing
  else reads it (PEARL: no).
- **FOREIGN.** The name is, or contains, a word or phrase in a language other than English, Latin and
  Hawaiian included (SHALOM, CARPE DIEM, KA' MAKANI, JOLI BATEAU). Place names are not foreign words.

When in doubt, the code is no. The doubts are listed in `people/coded-told.json` under `doubt`.

## By `tools/features.py`

- **SINGLE.** One word, after a closing numeral or roman numeral (II, III, 2, TOO) is removed.
- **SEQUEL.** Ends in a numeral, a roman numeral II to X, or TOO.
- **SEAWORD.** Contains, at the start of a word, one of: SEA, SAIL, REEL, FISH, FIN, WATER, WAVE, TIDE, SALT,
  ISLAND, BUOY, KNOT, AQUA, OCEAN, MARIN, NAUT, ANCHOR, BOAT, MOOR, SHELL, BAY, COAST, HARBO, CAPT, SHORE,
  DEEP, BLUE, WIND, HOOK, BAIT, CAST, NET, KEEL, HULL, DOCK, PORT, STARBOARD, LEEWARD, LATITUDE, CREW, MATE,
  SKIPPER, ADMIRAL, MERMAID, PIRATE, DOLPHIN, MARLIN, TUNA, OSPREY, GULL, PELICAN, CORAL, REEF, LAGOON,
  PELAGIC, NAUTICAL, AHOY, OAR, ROW, BREEZE, GALE, SQUALL, SWELL, SURF, SPRAY, BRINE, SALTY, CHANNEL, CAY,
  KEY, BEACH, SAND, DUNE, TROLL, LURE, ANGLE, CATCH, BITE, SNAG, WAKE, BOW, STERN, RUDDER, HELM, ANCHOR,
  MAST, JIB, SHIP.
- **FREQ.** How many valid recreational vessels in the register bear exactly this name, read from the same
  API on the night (`tools/freq.py`). Classes: 1 (this name on one boat only; for a maker's name, on none or
  one), 2–9, 10–99, 100 or more. For a maker's name that no registered boat bears, FREQ is 0 and is reported
  apart from 1.

## Told and untold

Arm G is told the people's shares on four features: PUN, PERSON, SINGLE and FREQ = 1. Arm D is asked to
estimate the same four. FOREIGN, SEQUEL, SEAWORD and FREQ ≥ 100 are told to no maker: they are where a type
that the counted features hold down could move.
