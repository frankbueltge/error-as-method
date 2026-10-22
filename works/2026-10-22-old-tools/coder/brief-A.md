You start without any history. Do not use any tool except reading the files named below.

Five files are lists of public datasets ("shelves"), one per line: `{DIR}/S1.txt`, `{DIR}/S2.txt`,
`{DIR}/S3.txt`, `{DIR}/S4.txt`, `{DIR}/S5.txt`. `{DIR}/items.txt` is a list of materials, each with an
id and a short description (publisher, dataset, URL).

For every material and every shelf, give one code:
- SAME: the shelf names this dataset: the same publisher and the same series or collection (a
  different period, station, resolution, column or subset of the same series still counts as SAME;
  a republisher's copy of the same series counts as SAME).
- KIN: the shelf does not name this dataset, but it names the same phenomenon from another
  publisher, or another series of the same publisher about a closely related thing.
- OFF: neither.
For SAME and KIN, quote the shelf line you matched. Also give each material a domain of one to three
words (what it is about, not who publishes it).

Answer only with JSON: a list of objects {"id": ..., "domain": ..., "S1": {"code": ..., "line": ... or
null}, "S2": {...}, "S3": {...}, "S4": {...}, "S5": {...}}, in the order of the list.
