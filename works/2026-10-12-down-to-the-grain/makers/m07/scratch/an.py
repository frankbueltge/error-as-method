from PIL import Image
import json,sys,math
g=Image.open('/tmp/claude-0/s122/mk/m07/work/record.jpg').convert('L')
W,H=g.size
P=[[255-g.getpixel((x,y)) for x in range(W)] for y in range(H)]  # darkness
# local maxima of darkness
pts=[]
for y in range(H):
  for x in range(W):
    v=P[y][x]
    if v<90: continue
    ok=True
    for dy in (-1,0,1):
      for dx in (-1,0,1):
        if dx==0 and dy==0: continue
        yy,xx=y+dy,x+dx
        if 0<=yy<H and 0<=xx<W and (P[yy][xx]>v or (P[yy][xx]==v and (dy,dx)<(0,0))): ok=False
    if ok: pts.append((x,y,v))
print('peaks',len(pts))
# per column envelope via dark pixels
env=[]
for x in range(W):
  ys=[y for y in range(H) if P[y][x]>100]
  env.append((min(ys),max(ys),sum(ys)/len(ys)) if ys else None)
for x in range(0,W,5):
  print(x,env[x])
json.dump({'pts':pts,'env':env},open('pts.json','w'))
