from PIL import Image
import json,sys
im=Image.open('/tmp/claude-0/s130/mk/m01/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
D=[[255-px[x,y] for y in range(H)] for x in range(W)]
thr=int(sys.argv[1]) if len(sys.argv)>1 else 90
# 2D local maxima
pts=[]
for x in range(W):
  for y in range(H):
    v=D[x][y]
    if v<thr: continue
    ok=True
    for dx in (-1,0,1):
      for dy in (-1,0,1):
        if dx==0 and dy==0: continue
        X,Y=x+dx,y+dy
        if 0<=X<W and 0<=Y<H:
          w=D[X][Y]
          if w>v or (w==v and (dx,dy)<(0,0)): ok=False
    if ok: pts.append((x,y,v))
print(thr,len(pts))
json.dump(pts,open('pts.json','w'))
