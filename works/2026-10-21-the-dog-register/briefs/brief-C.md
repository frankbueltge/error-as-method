You are making a work for the web. You start without any history.

Your folder: `{FOLDER}`

It holds two files. `data/dogs.csv` is the dog register of the city of Zürich as the city publishes it for
download (Open Data Zürich, "Aktueller Hundebestand der Stadt Zürich", reference day 30 September 2026),
10,106 dogs, one row each. Twelve of its columns are kept, under their published names:
HID (the holder's number), AlterV10Cd (the holder's age group: 10 means 10–19 years, 20 means 20–29, and so
on; 999 unknown), SexLang (the holder's sex), KreisCd (the city district, 1–12, where the holder lives),
QuarLang (the statistical quarter), Rasse1Text (the dog's breed), Rasse2Text (second breed, for a cross),
Rassetyp1Lang (the breed's type: Kleinwüchsig small, Rassentypenliste I or II the city's lists of larger
breeds), GebHundDatJahr (the dog's year of birth), AlterVHundNum (the dog's age in years), SexHundLang (the
dog's sex), HundefarbeText (the dog's colour). Words are in German as published. `data/dogs.js` holds the
same table as `const DOGS = [...]`, one object per dog keyed by those column names, numbers as numbers and
empty cells as null, because a page opened from a file cannot read a `.csv` beside it. This table is your
material. Do not use the web.

Make one work that gives this material a form. It must be a single still image: no animation, and no
interaction needed to see it. Write it as `index.html` in your folder. Load the material with
`<script src="data/dogs.js"></script>` and read it from `DOGS` when the page runs; do not write values from
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
