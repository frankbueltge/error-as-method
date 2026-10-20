You start without any history. You are a coder. Use no tool except reading the files named here.

Read `{DIR}/shelf.txt`. It is a numbered list of "wrong readings": ways of reading a dataset that are
known to be wrong, which someone might use on purpose to make a work of art. Lines are labelled
S1-01 … S4-25.

Read `{DIR}/items.txt`. It holds six items, I1 … I6. Each is a wrong reading that someone chose on
purpose for one data file: the 2024 record of an ocean buoy (wind, waves, pressure, temperatures, in
rows every ten minutes). In that file, missing values are marked by runs of nines (99.00, 999, 999.0,
9999.0), as the publisher's documentation says. About two thirds of the wave-height values in the file
are such markers, and several columns are markers in every row.

Read `{DIR}/notes.txt`. It holds twelve short notes, N01 … N12, each written by the maker of one work
made from that same file.

Write `{DIR}/codes.json` with exactly this shape, and nothing else:

{"items": {"I1": {"code": "SAME|KIN|OFF", "shelf": ["S#-##", ...], "own": "YES|NO", "why": "one sentence"}, ...},
 "notes": {"N01": {"named": "YES|NO", "quote": "the words that decide it, or empty"}, ...},
 "shelf_missing": ["S#-##", ...]}

For each item:
- code SAME if one or more shelf lines name the same wrong reading (the same operation done to the data);
  KIN if a shelf line names a close relative (the same kind of operation, but a different one); OFF if
  no shelf line comes close. List the shelf lines you matched (none for OFF).
- own YES if the wrong reading consists in treating the file's missing-value markers as real values, or
  in reading the gaps they mark as the material; NO otherwise.

For each note: named YES if the note says that the file marks missing values (the nines, markers,
sentinels, fill values) or that values are missing from the record; NO otherwise. Quote the deciding words.

shelf_missing: every shelf line whose wrong reading consists in treating missing values, missing-value
markers, gaps or absences as data. Empty list if none.

When done, reply with the word "done".
