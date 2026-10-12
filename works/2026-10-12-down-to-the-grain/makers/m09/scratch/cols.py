from PIL import Image
im=Image.open('/tmp/claude-0/s122/mk/m09/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
thr=200
runs=[]
for x in range(W):
  r=[];y=0
  while y<H:
    if px[x,y]<thr:
      y0=y; w=0; s=0
      while y<H and px[x,y]<thr:
        d=255-px[x,y]; w+=d; s+=d*y; y+=1
      r.append((round(s/w,1),w))
    else: y+=1
  runs.append(r)
import collections
print(collections.Counter(len(r) for r in runs))
for x in range(400,440): print(x,runs[x])
import json; json.dump(runs,open('/tmp/claude-0/s122/mk/m09/scratch/runs.json','w'))
