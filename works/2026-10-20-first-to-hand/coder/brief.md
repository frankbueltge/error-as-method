You start without any history. Do not use any tool except reading the two files named below.

`{SHELF}` is a list of public datasets (the "shelf"), one per line, alphabetised.
`{ITEMS}` is a list of materials, each with an id and a short description (publisher, dataset, URL).

For every material, give one code:
- SAME: the shelf names this dataset: the same publisher and the same series or collection (a
  different period, station, resolution or subset of the same series still counts as SAME).
- KIN: the shelf does not name this dataset, but it names the same phenomenon from another
  publisher, or another series of the same publisher about a closely related thing.
- OFF: neither.
For SAME and KIN, quote the shelf line you matched. Also give each material a domain of one to three
words (what it is about, not who publishes it).

Answer only with JSON: a list of objects {"id": ..., "code": ..., "shelf_line": ... or null,
"domain": ...}, in the order of the list.
