You start without any history. Do not use the web. Read nothing on this computer except the files named here.

Folder: `{PACKET}`

`T01.png` … `T20.png` are pictures of twenty pages, each drawn from a table of Delaware's highway bridges.
That table is beside the pictures, as `data/bridges.csv` (874 bridges, one row each; columns: STRUCTURE_NUMBER_008
the bridge's number, COUNTY_CODE_003 the county (1 Kent, 3 New Castle, 5 Sussex), FEATURES_DESC_006A what it
crosses, FACILITY_CARRIED_007 the road it carries, LAT_016 and LONG_017 latitude north and longitude west as
degrees, minutes, seconds and hundredths run together, YEAR_BUILT_027, ADT_029 average daily traffic,
STRUCTURE_KIND_043A the main span's material code, STRUCTURE_LEN_MT_049 length in metres, BRIDGE_CONDITION G/F/P,
LOWEST_RATING 9 excellent to 0 failed). Open and look at every picture. You may read the table and compute from it
as much as you need.

For each picture say whether what it shows or states **agrees with this table**: `yes` (nothing you can see
disagrees), `no` (something disagrees), or `cannot tell` (it shows too little to check). If `no`, name in one
sentence the first thing you saw that disagrees; otherwise one sentence of what you checked.

Write your answer as JSON to `{PACKET}/codes.json`: a list of objects
`{"id":"T01","agrees":"yes","why":"..."}`, one per picture, in order. If you need scratch files, keep them in
the folder. When you have finished, reply with one sentence.
