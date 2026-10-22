You start without any history. Do not use the web. Read nothing on this computer except the files named here.

Folder: `{PACKET}`

`G01.png` … `G20.png` are pictures of twenty pages for the web, each drawn from a table:
the National Bridge Inventory's 2025 record of the highway bridges of Delaware, 874 bridges, one row each (the
bridge's number, county, what it crosses, the road it carries, latitude and longitude, year built, average daily
traffic, the main span's material, length, condition class and lowest condition rating). Some of the pages were drawn from the true table. The others were drawn from a copy in which one or more
columns were **shuffled**: every value in a shuffled column is a real value from that column, and appears as often
as before, but the values were dealt out to the wrong bridges. You do not have the table. Open and look at every
picture.

For each picture say `real` or `shuffled`, how sure you are (`low`, `medium`, `high`), and one sentence of
what in the picture decided it.

Write your answer as JSON to `{PACKET}/codes.json`: a list of objects
`{"id":"G01","call":"real","sure":"low","why":"..."}`, one per picture, in order.
When you have finished, reply with one sentence.
