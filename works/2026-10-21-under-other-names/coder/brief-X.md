You start without any history. Do not use the web. Read nothing on this computer except the files named here.

Folder: `{PACKET}`

`family/F1.png` … `family/F4.png` are pictures of four works, each made by a different maker from the same
table. `variants/V01.png` … `variants/V24.png` are pictures of twenty-four other pages. Open and look at
every picture.

For each variant V01 … V24, say:
- **broken**: yes if the page plainly failed (blank or almost blank, an error, nothing legible was drawn), else no;
- **nearest**: which of F1–F4 it is nearest to, or `none`;
- **distance** from that nearest family work, on this scale (give it even when broken is yes, if you can):
  0 the same work, or a slight change of it; 1 the same form changed in details; 2 a related form, changed
  in structure; 3 a different work that shares no visible form with the family;
- one short sentence of what you see.

Write your answer as JSON to `{PACKET}/codes.json`: a list of objects
`{"id":"V01","broken":"no","nearest":"F2","distance":1,"seen":"..."}`, one per variant, in order.
When you have finished, reply with one sentence.
