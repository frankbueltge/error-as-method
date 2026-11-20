# Brief, arm W (from a word)

You are a maker working alone in the folder `{DIR}`. Work only there. Open no file outside it.

**The material is the tangram:** seven flat pieces cut from a square: two large triangles (L1, L2), one medium
triangle (M), two small triangles (S1, S2), a square (Q) and a parallelogram (P). A figure uses all seven pieces,
every piece touching the figure, none overlapping. People have made figures from these pieces for two hundred years.

**What to make:** three figures, each of a different subject of your own choosing. A viewer will see each figure only
as a dark silhouette, with no title, and should be able to see what it is.

**How the pieces are written.** A figure is a JSON list of seven placements:
`{"piece": "L1", "x": 2.0, "y": 0.667, "rot": 0, "flip": false}`. `x, y` is where the piece's centre goes, `rot` turns
it counter-clockwise in degrees about its centre, `flip` mirrors it first (only matters for P). `square.json` in your
folder is the seven pieces put together as the 4×4 square they are cut from; read it to see the pieces' shapes and
sizes.

**How to look.** `python3 tangram.py check fig1.json fig1.png` tells you whether the figure is valid (and what is
wrong if not) and draws two pictures: `fig1.png` with the pieces labelled, and `fig1-silhouette.png`, which is what a
viewer will see. Open the pictures with your file-reading tool and look at them. Check and look as often as you like;
every check is logged in `checks.log`, which is part of the record (please do not edit or delete it).

**Hand back.** Save the three figures as `fig1.json`, `fig2.json`, `fig3.json`, each valid. Then write `makings.json`:

```json
{"figures": [
  {"file": "fig1.json", "name": "what it is, in a few words", "how": "at most two sentences: how you found this form",
   "seen_before": "yes / no / unsure, and if yes, where or what"},
  ...],
 "files_opened": ["every file you opened or read, including pictures"]}
```

Then reply with one line: done.
