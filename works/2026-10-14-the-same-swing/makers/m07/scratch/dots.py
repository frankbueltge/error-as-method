from PIL import Image
im=Image.open('/tmp/claude-0/s124/mk/m07/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
d=[[255-p[x,y] for x in range(W)] for y in range(H)]
# 2x2 box sum
s=[[sum(d[y+a][x+b] for a in (0,1) for b in (0,1)) for x in range(W-1)] for y in range(H-1)]
pts=[]
for y in range(H-1):
  for x in range(W-1):
    v=s[y][x]
    if v<300: continue
    ok=True
    for a in (-1,0,1):
      for b in (-1,0,1):
        if (a or b) and 0<=y+a<H-1 and 0<=x+b<W-1:
          w=s[y+a][x+b]
          if w>v or (w==v and (a,b)<(0,0)): ok=False
    if ok: pts.append((x+0.5,y+0.5,v))
print(len(pts))
import json; json.dump(pts,open('pts.json','w'))
# per-column counts
from collections import Counter
c=Counter(int(x) for x,y,v in pts)
print([c[i] for i in range(W)])
