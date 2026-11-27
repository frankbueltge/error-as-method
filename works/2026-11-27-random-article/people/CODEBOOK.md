# Codebook: the kind of each article (fixed before any curator ran)

Each of the 160 articles in `pool-160.jsonl` was coded by hand by this session from its title and lead, into one of
nine kinds, on 2026-11-27, before the briefs were sent. The code is in the field `kind`. Curators never saw it.

| code | kind | in the 160 |
|---|---|---|
| P | a person (living, dead, historical) | 34 (21.2 %) |
| X | other: concepts, objects, organisations, bands, events, ships, groups of people, politics | 29 (18.1 %) |
| S | a settlement or administrative place (village, commune, municipality, locality, district) | 21 (13.1 %) |
| D | a navigation page: disambiguation, surname, "may refer to", and "List of" pages | 21 (13.1 %) |
| W | a creative work (film, album, song, novel, TV series, comic, book) | 19 (11.9 %) |
| T | sport: a season, team, club, competition, final, record list, racehorse | 13 (8.1 %) |
| B | a building, site or institution with a place (school, museum, park, zoo, station, mine, historic district) | 10 (6.2 %) |
| O | an organism or taxon (species, genus, family) | 7 (4.4 %) |
| G | a natural feature (river, lake, island, mountain) | 6 (3.8 %) |

**Common kinds** for the predictions are P, S and D (each at least 13 % of the 160, and concrete). **Rare kinds** are
T, B, O and G (each under 9 %). X is a remainder and belongs to neither.

**Doubtful codes, named so a reader can recode:** 7 (a racehorse, coded T), 22 (the 300-win club, T), 27 (a record
label, X), 53 (a web magazine, X), 65 (a band, X), 70 (an ancestor god, X), 124 (a parliamentary constituency, X),
10 (a bookshop, B), 31 (an ethnic sub-group, X).

Length is the article's word count in the snapshot (`words`); 46 of 160 have under 100 words; the median is 209.
