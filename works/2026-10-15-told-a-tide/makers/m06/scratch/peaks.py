from PIL import Image
import json, math
g=Image.open('/tmp/claude-0/s128/mk/m06/work/record.jpg').convert('L'); W,H=g.size; p=g.load()
D=[[255-p[x,y] for x in range(W)] for y in range(H)]
tot=sum(map(sum,D)); print('total darkness',tot)
# local maxima
pk=[]
for y in range(H):
  for x in range(W):
    v=D[y][x]
    if v<60: continue
    ok=True
    for dy in(-1,0,1):
      for dx in(-1,0,1):
        if dx==dy==0: continue
        yy,xx=y+dy,x+dx
        if 0<=yy<H and 0<=xx<W:
          w=D[yy][xx]
          if w>v or (w==v and (dy,dx)<(0,0)): ok=False
    if ok: pk.append((x,y,v))
print('peaks',len(pk))
# per-column stats
cm=[]
for x in range(W):
  s=sum(D[y][x] for y in range(H)); m=sum(D[y][x]*y for y in range(H))/s
  cm.append(m)
json.dump({'peaks':pk,'colmean':cm},open('peaks.json','w'))
# darkness sum of a single isolated dot estimate
import statistics
print(statistics.median(v for _,_,v in pk))
