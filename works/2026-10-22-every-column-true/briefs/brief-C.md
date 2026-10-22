You are making a work for the web. You start without any history.

Your folder: `{FOLDER}`

It holds two files. `data/bridges.csv` is the National Bridge Inventory's record of the highway bridges of the US
state of Delaware, as the Federal Highway Administration publishes it for 2025, 874 bridges, one row each. Twelve
of its columns are kept, under their published names:
STRUCTURE_NUMBER_008 (the bridge's number), COUNTY_CODE_003 (the county: 1 Kent, 3 New Castle, 5 Sussex),
FEATURES_DESC_006A (what the bridge crosses), FACILITY_CARRIED_007 (the road it carries), LAT_016 and LONG_017
(its latitude north and longitude west, written as degrees, minutes, seconds and hundredths of a second run
together: 39460947 is 39° 46′ 09.47″), YEAR_BUILT_027 (year built), ADT_029 (average daily traffic, vehicles per
day), STRUCTURE_KIND_043A (the main span's material: 1 concrete, 2 concrete continuous, 3 steel, 4 steel
continuous, 5 prestressed concrete, 6 prestressed concrete continuous, 7 wood or timber, 8 masonry, 9 aluminium,
wrought or cast iron, 0 other), STRUCTURE_LEN_MT_049 (the structure's length in metres), BRIDGE_CONDITION (G good,
F fair, P poor), LOWEST_RATING (the lowest of its inspected condition ratings, 9 excellent down to 0 failed).
Words are as published. `data/bridges.js` holds the same table as `const BRIDGES = [...]`, one object per bridge
keyed by those column names, numbers as numbers, because a page opened from a file cannot read a `.csv` beside
it. This table is your material. Do not use the web.

Make one work that gives this material a form. It must be a single still image: no animation, and no
interaction needed to see it. Write it as `index.html` in your folder. Load the material with
`<script src="data/bridges.js"></script>` and read it from `BRIDGES` when the page runs; do not write values from
the table into your page's code. It must load nothing except from your folder (no network when it is
viewed). SVG, canvas, DOM and plain JavaScript are all allowed; no libraries. It will be viewed at
1100 × 800.

Beside your folder is a viewer. Run `node {RENDER} {FOLDER}` and it renders your `index.html` at
1100 × 800 as a picture, `renders/NN.png` in your folder, which you can open and look at. Running the
viewer is allowed, although it lives outside your folder. Use it as often or as little as you like.

Then write `NOTE.md`: the work's title as a heading, then one short paragraph on what the form does.

Do not read or write anything on this computer outside your folder, except running the viewer. If you
need scratch files, keep them in your folder.

When you have finished, reply in a few sentences: what you made.
