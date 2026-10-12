from PIL import Image, ImageFilter
import json, math, collections
im=Image.open('/tmp/claude-0/s122/mk/m09/work/record.jpg').convert('L')
W,H=im.size; raw=im.load()
d=[[255-raw[x,y] for y in range(H)] for x in range(W)]
# local maxima on raw darkness in 3x3, darkness>60
pk=[]
for x in range(1,W-1):
  for y in range(1,H-1):
    v=d[x][y]
    if v<70: continue
    ok=True
    for dx in(-1,0,1):
      for dy in(-1,0,1):
        if (dx or dy):
          u=d[x+dx][y+dy]
          if u>v or (u==v and (dx,dy)<(0,0)): ok=False
    if ok:
      ws=0;sx=0;sy=0
      for dx in(-1,0,1):
        for dy in(-1,0,1):
          u=d[x+dx][y+dy]; ws+=u; sx+=u*(x+dx); sy+=u*(y+dy)
      pk.append((sx/ws,sy/ws,v,ws))
print(len(pk))
print(collections.Counter(int(p[2]//20)*20 for p in pk))
pk.sort()
print(pk[:8]); print(pk[-8:])
json.dump(pk,open('/tmp/claude-0/s122/mk/m09/scratch/peaks.json','w'))
