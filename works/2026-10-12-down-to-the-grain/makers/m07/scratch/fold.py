from PIL import Image
import math,json
g=Image.open('/tmp/claude-0/s122/mk/m07/work/record.jpg').convert('L')
W,H=g.size
P=[[max(0,255-g.getpixel((x,y))-25) for x in range(W)] for y in range(H)]
pts=[]
for y in range(1,H-1):
  for x in range(1,W-1):
    v=P[y][x]
    if v<70: continue
    if all(v>P[y+dy][x+dx] or (v==P[y+dy][x+dx] and (dy,dx)>(0,0)) for dy in (-1,0,1) for dx in (-1,0,1) if (dx,dy)!=(0,0)):
      sw=sx=sy=0
      for dy in (-1,0,1):
        for dx in (-1,0,1):
          w=P[y+dy][x+dx]; sw+=w; sx+=w*(x+dx); sy+=w*(y+dy)
      pts.append((sx/sw,sy/sw,v))
print(len(pts))
X0,X1=2.0,296.5
hp=1463/(X1-X0)
json.dump({'pts':pts,'X0':X0,'X1':X1},open('pts2.json','w'))
import sys
for per in (12.42,12.0,24.84,24.0):
  grid=[[0]*48 for _ in range(30)]
  for x,y,v in pts:
    t=(x-X0)*hp
    if t>24*40: continue
    ph=(t%per)/per
    r=int((y-40)/1.5)
    if 0<=r<30: grid[r][int(ph*48)]+=1
  print('period',per)
  for r in grid: print(''.join(' .:-=+*#%@'[min(9,c)] for c in r))
