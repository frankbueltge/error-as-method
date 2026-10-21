You are making a work for the web. You start without any history.

Your folder: `{FOLDER}`

It holds two files. `data/elements.csv` is the periodic table as PubChem publishes it for download
(https://pubchem.ncbi.nlm.nih.gov/periodic-table/), 118 elements, one row each, seventeen columns:
AtomicNumber, Symbol, Name, AtomicMass, CPKHexColor, ElectronConfiguration, Electronegativity,
AtomicRadius, IonizationEnergy, ElectronAffinity, OxidationStates, StandardState, MeltingPoint,
BoilingPoint, Density, GroupBlock, YearDiscovered. `data/elements.js` holds the same table as
`const ELEMENTS = [...]`, one object per element keyed by those column names, numbers as numbers and
empty cells as null, because a page opened from a file cannot read a `.csv` beside it. This table is
your material. Do not use the web.

Make one work that gives this material a form. It must be a single still image: no animation, and no
interaction needed to see it. Write it as `index.html` in your folder. Load the material with
`<script src="data/elements.js"></script>` and read it from `ELEMENTS` when the page runs; do not write
values from the table into your page's code. It must load nothing except from your folder (no network
when it is viewed). SVG, canvas, DOM and plain JavaScript are all allowed; no libraries. It will be viewed
at 1100 × 800.

Beside your folder is a viewer. Run `node {RENDER} {FOLDER}` and it renders your `index.html` at
1100 × 800 as a picture, `renders/NN.png` in your folder, which you can open and look at. Running the
viewer is allowed, although it lives outside your folder. Use it as often or as little as you like.

Then write `NOTE.md`: the work's title as a heading, then one short paragraph on what the form does.

Do not read or write anything on this computer outside your folder, except running the viewer. If you
need scratch files, keep them in your folder.

When you have finished, reply in a few sentences: what you made.
