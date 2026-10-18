import sys, json
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); px=im.load(); W,H=im.size
d=[[max(0,255-px[x,y]) for y in range(H)] for x in range(W)]
# 2D local maxima of darkness, threshold
pts=[]
for x in range(W):
  for y in range(H):
    v=d[x][y]
    if v<60: continue
    ok=True
    for dx in (-1,0,1):
      for dy in (-1,0,1):
        if dx==dy==0: continue
        xx,yy=x+dx,y+dy
        if 0<=xx<W and 0<=yy<H and d[xx][yy]>v: ok=False
    if ok:
      # subpixel centroid in 3x3
      s=sx=sy=0
      for dx in (-1,0,1):
        for dy in (-1,0,1):
          xx,yy=x+dx,y+dy
          if 0<=xx<W and 0<=yy<H:
            w=d[xx][yy]; s+=w; sx+=w*xx; sy+=w*yy
      pts.append((sx/s,sy/s,v,s))
print(len(pts))
json.dump(pts,open('pts.json','w'))
ys={}
for p in pts: ys[round(p[1])]=ys.get(round(p[1]),0)+1
print(sorted(ys.items()))
