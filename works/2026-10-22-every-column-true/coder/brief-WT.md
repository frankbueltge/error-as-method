You start without any history. Do not use the web. Read nothing on this computer except the files named here.

Folder: `{PACKET}`

`J01.png` … `J20.png` are pictures of twenty works for the web, each made from the same material:
the National Bridge Inventory's 2025 record of the highway bridges of Delaware, 874 bridges, one row each (the
bridge's number, county, what it crosses, the road it carries, latitude and longitude, year built, average daily
traffic, the main span's material, length, condition class and lowest condition rating). The material itself is beside the pictures, as `data/bridges.csv`; you may read it and
compute from it if you wish. Open and look at every picture.

For each picture say whether it **works**, as a work made from this material: `yes` or `no`, and one
sentence of why. Use your own judgement of what working means here, and say in one sentence at the top
what you took it to mean.

Write your answer as JSON to `{PACKET}/codes.json`:
`{"meaning":"...","items":[{"id":"J01","works":"yes","why":"..."}, ...]}`, one item per picture, in order.
If you need scratch files, keep them in the folder. When you have finished, reply with one sentence.
