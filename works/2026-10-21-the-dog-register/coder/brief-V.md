You start without any history. Do not use the web. Read nothing on this computer except the files named here.

Folder: `{PACKET}`

`T01.png` … `T28.png` are pictures of twenty-eight pages, each drawn from a table of Zürich's registered dogs.
That table is beside the pictures, as `data/dogs.csv` (10,106 dogs, one row each; columns: HID the holder's
number, AlterV10Cd the holder's age group, SexLang the holder's sex, KreisCd the city district, QuarLang the
statistical quarter, Rasse1Text and Rasse2Text the breeds, Rassetyp1Lang the breed type, GebHundDatJahr the
dog's year of birth, AlterVHundNum its age, SexHundLang its sex, HundefarbeText its colour). Open and look at
every picture. You may read the table and compute from it as much as you need.

For each picture say whether what it shows or states **agrees with this table**: `yes` (nothing you can see
disagrees), `no` (something disagrees), or `cannot tell` (it shows too little to check). If `no`, name in one
sentence the first thing you saw that disagrees; otherwise one sentence of what you checked.

Write your answer as JSON to `{PACKET}/codes.json`: a list of objects
`{"id":"T01","agrees":"yes","why":"..."}`, one per picture, in order. If you need scratch files, keep them in
the folder. When you have finished, reply with one sentence.
