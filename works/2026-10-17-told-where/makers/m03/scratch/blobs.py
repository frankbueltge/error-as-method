from PIL import Image
import json, sys
g=Image.open(sys.argv[1]).convert('L'); W,H=g.size; p=g.load()
D=[[ max(0,(240-p[x,y]))/240.0 for x in range(W)] for y in range(H)]
def at(x,y): return D[y][x] if 0<=x<W and 0<=y<H else 0
bl=[]
for y in range(H):
  if y in (83,84): continue
  for x in range(W):
    d=D[y][x]
    if d<0.12: continue
    if all(d>=at(x+i,y+j) for i in (-1,0,1) for j in (-1,0,1) if (i,j)!=(0,0) and (j==0 or y+j not in (83,84))):
      s=sx=sy=0
      for i in (-1,0,1):
        for j in (-1,0,1):
          if y+j in (83,84): continue
          v=at(x+i,y+j); s+=v; sx+=v*(x+i); sy+=v*(y+j)
      bl.append((round(sx/s+0.5,2), round(sy/s+0.5,2), round(s,2), round(d,2)))
band=[round(min(1,(D[83][x]+D[84][x])/1.6),2) for x in range(W)]
print(len(bl), 'blobs; above zero', sum(1 for b in bl if b[1]<83), 'below', sum(1 for b in bl if b[1]>85))
import collections
print('weight quantiles', sorted(b[2] for b in bl)[::len(bl)//10])
json.dump({'blobs':bl,'band':band},open('data.json','w'))
