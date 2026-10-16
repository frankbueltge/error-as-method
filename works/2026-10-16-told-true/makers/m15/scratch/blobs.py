from PIL import Image
import json
im=Image.open('/tmp/claude-0/s130/mk/m15/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
d=[[max(0,255-p[x,y]) for y in range(H)] for x in range(W)]
pts=[]
for x in range(W):
  for y in range(H):
    v=d[x][y]
    if v<70: continue
    nb=[d[x+i][y+j] for i in (-1,0,1) for j in (-1,0,1) if (i or j) and 0<=x+i<W and 0<=y+j<H]
    if all(v>=n for n in nb):
      sw=sx=sy=0
      for i in (-1,0,1):
        for j in (-1,0,1):
          if 0<=x+i<W and 0<=y+j<H:
            w=max(0,d[x+i][y+j]-25);sw+=w;sx+=w*(x+i);sy+=w*(y+j)
      pts.append((round(sx/sw,2),round(sy/sw,2),v))
# dedupe plateaus
out=[]
for q in pts:
  if any(abs(q[0]-o[0])<1 and abs(q[1]-o[1])<1 for o in out): continue
  out.append(q)
print(len(pts),len(out))
total=sum(max(0,v-25) for c in d for v in c);print('total ink',total)
json.dump(out,open('blobs.json','w'))
