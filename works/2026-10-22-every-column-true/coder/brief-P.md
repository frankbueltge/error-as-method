You start without any history. Do not use the web. Read nothing on this computer except the files named here.

Folder: `{PACKET}`

`P01.png` … `P20.png` are pictures of twenty pages for the web. Open and look at every picture. You are not
asked whether they are good, or whether they are true of anything outside themselves. For each picture say:
- **broken**: `yes` if the page plainly failed (blank or almost blank, an error, nothing legible was drawn), else `no`;
- **words**: is every word and number written on the page (title, subtitle, labels, legend, axis values, captions,
  counts) true of what the page itself draws? `yes` (nothing written contradicts the drawing), `no` (something
  written contradicts the drawing), or `cannot tell`;
- one short sentence: if `no`, what is written and what the drawing shows instead; otherwise what you checked.

Write your answer as JSON to `{PACKET}/codes.json`: a list of objects
`{"id":"P01","broken":"no","words":"yes","why":"..."}`, one per picture, in order.
When you have finished, reply with one sentence.
