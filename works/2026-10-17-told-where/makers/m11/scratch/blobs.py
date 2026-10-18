from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m11/work/record.jpg').convert('L');px=im.load()
W,H=im.size
D=[[255-px[x,y] for y in range(H)] for x in range(W)]
# local maxima of darkness in 3x3 neighbourhood, above threshold
bl=[]
for x in range(W):
  for y in range(H):
    v=D[x][y]
    if v<60: continue
    ok=True
    for dx in (-1,0,1):
      for dy in (-1,0,1):
        if dx==0 and dy==0: continue
        xx,yy=x+dx,y+dy
        if 0<=xx<W and 0<=yy<H:
          w=D[xx][yy]
          if w>v or (w==v and (dx,dy)<(0,0)): ok=False
    if ok:
      # subpixel centroid in 3x3
      s=sx=sy=0
      for dx in (-1,0,1):
        for dy in (-1,0,1):
          xx,yy=x+dx,y+dy
          if 0<=xx<W and 0<=yy<H:
            w=max(0,D[xx][yy]-30); s+=w; sx+=w*xx; sy+=w*yy
      bl.append((round(sx/s,2),round(sy/s,2),v))
print(len(bl), sum(1 for b in bl if b[1]<81))
json.dump(bl,open('blobs.json','w'))
