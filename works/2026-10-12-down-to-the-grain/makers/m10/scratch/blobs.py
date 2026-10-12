import sys, json
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; p=im.load()
d=[[max(0,255-p[x,y]) for x in range(W)] for y in range(H)]
# local maxima of 3x3-summed darkness
S=[[0]*W for _ in range(H)]
for y in range(H):
  for x in range(W):
    s=0
    for dy in (0,1):
      for dx in (0,1):
        yy,xx=y+dy,x+dx
        if yy<H and xx<W: s+=d[yy][xx]
    S[y][x]=s
pts=[]
for y in range(H):
  for x in range(W):
    v=S[y][x]
    if v<250: continue
    ok=True
    for dy in (-1,0,1):
      for dx in (-1,0,1):
        if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W:
          w=S[y+dy][x+dx]
          if w>v or (w==v and (dy,dx)<(0,0)): ok=False
    if ok:
      # centroid in 2x2
      tw=0;cx=0;cy=0
      for dy in (0,1):
        for dx in (0,1):
          yy,xx=y+dy,x+dx
          if yy<H and xx<W: w=d[yy][xx]; tw+=w; cx+=w*xx; cy+=w*yy
      pts.append((cx/tw,cy/tw,v))
print(len(pts), file=sys.stderr)
xs=[q[0] for q in pts]; print(min(xs),max(xs), file=sys.stderr)
json.dump(pts,open('pts.json','w'))
# darkness total
tot=sum(map(sum,d)); print('total dark',tot, file=sys.stderr)
