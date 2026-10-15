import sys, json, math
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; px=im.load()
# darkness map
D=[[max(0,255-px[x,y]) for x in range(W)] for y in range(H)]
tot=sum(map(sum,D)); print('total darkness',tot)
# local maxima as dot centers
pts=[]
for y in range(H):
  for x in range(W):
    d=D[y][x]
    if d<60: continue
    ok=True
    for dy in(-1,0,1):
      for dx in(-1,0,1):
        if dx==dy==0: continue
        yy,xx=y+dy,x+dx
        if 0<=yy<H and 0<=xx<W:
          e=D[yy][xx]
          if e>d or (e==d and (dy,dx)<(0,0)): ok=False
    if ok:
      # weighted centroid in 3x3
      sw=sx=sy=0
      for dy in(-1,0,1):
        for dx in(-1,0,1):
          yy,xx=y+dy,x+dx
          if 0<=yy<H and 0<=xx<W:
            w=D[yy][xx]; sw+=w; sx+=w*xx; sy+=w*yy
      pts.append((sx/sw,sy/sw,sw))
print('peaks',len(pts))
import statistics
ws=sorted(p[2] for p in pts); print('mass quantiles',[ws[int(q*(len(ws)-1))] for q in(0,.1,.25,.5,.75,.9,1)])
json.dump(pts,open('peaks.json','w'))
# column profiles: darkness-weighted
cols=[]
for x in range(W):
  col=[D[y][x] for y in range(H)]
  s=sum(col)
  cols.append(col)
json.dump(cols,open('cols.json','w'))
