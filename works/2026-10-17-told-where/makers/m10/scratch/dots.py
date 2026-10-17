from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m10/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
d=[[255-p[x,y] for x in range(W)] for y in range(H)]
dots=[]
for y in range(1,H-1):
  for x in range(W):
    v=d[y][x]
    if v<70: continue
    ok=True
    for dy in (-1,0,1):
      for dx in (-1,0,1):
        if dx==dy==0: continue
        xx,yy=x+dx,y+dy
        if 0<=xx<W and d[yy][xx]>v: ok=False
        if 0<=xx<W and d[yy][xx]==v and (dy<0 or (dy==0 and dx<0)): ok=False
    if ok:
      # subpixel centroid in 3x3
      s=sx=sy=0
      for dy in (-1,0,1):
        for dx in (-1,0,1):
          xx=x+dx
          if 0<=xx<W:
            w=d[y+dy][xx]; s+=w; sx+=w*xx; sy+=w*(y+dy)
      dots.append((sx/s,sy/s,v))
print(len(dots))
up=[t for t in dots if t[1]<81.5]
print('above baseline',len(up))
json.dump(dots,open('dots.json','w'))
P=4.8207; a=2.45
pxh=P/24
days={}
for x,y,v in up:
  t=(x-a)/pxh
  k=int((t+5)//24)  # day by UTC-5ish? use local: local = t-7
  tl=t-7
  k=int(tl//24)
  days.setdefault(k,[]).append((tl-24*k,y))
for k in sorted(days):
  ys=[y for _,y in days[k]]
  print(k,len(ys),round(min(ys),1), round(sum(83.5-y for y in ys)))
