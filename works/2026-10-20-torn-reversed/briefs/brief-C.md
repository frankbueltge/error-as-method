You are making a work for the web. You start without any history.

Your folder: `{FOLDER}`

It holds two files. `data/selborne.txt` is Gilbert White, *The Natural History of Selborne* (1789), the
whole text as published by Project Gutenberg (eBook #1408, https://www.gutenberg.org/ebooks/1408), with
Project Gutenberg's header and licence footer removed; nothing else was changed. `data/selborne.js`
holds the same text as one JavaScript string, `const SELBORNE = "...";`, because a page opened from a
file cannot read a `.txt` beside it; load it with `<script src="data/selborne.js"></script>`. This text
is your material. Do not use the web.

Make one work that gives this material a form. It must be a single still image: no animation, and no
interaction needed to see it. Write it as `index.html` in your folder. It must load the data only from
your folder (no network when it is viewed). SVG, canvas, DOM and plain JavaScript are all allowed; no
libraries. It will be viewed at 1100 × 800.

Beside your folder is a viewer. Run `node {RENDER} {FOLDER}` and it renders your `index.html` at
1100 × 800 as a picture, `renders/NN.png` in your folder, which you can open and look at. Running the
viewer is allowed, although it lives outside your folder. Use it as often or as little as you like.

Then write `NOTE.md`: the work's title as a heading, then one short paragraph on what the form does.

Do not read or write anything on this computer outside your folder, except running the viewer. If you
need scratch files, keep them in your folder.

When you have finished, reply in a few sentences: what you made.
