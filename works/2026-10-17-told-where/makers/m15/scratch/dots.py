import json
from PIL import Image
g=Image.open('/tmp/claude-0/s133/mk/m15/work/record.jpg').convert('L'); W,H=g.size
P=[[max(0,255-g.getpixel((x,y))-20) for x in range(W)] for y in range(H)]
exec(open('seg.py').read().split('# darkness')[0]) if False else None
runs=[(3,5),(7,10),(13,14),(17,19),(22,24),(27,29),(32,34),(37,39),(41,43),(46,48),(51,53),(56,58),(61,63),(66,68),(70,72),(75,77),(80,82),(85,87),(90,92),(94,97),(99,101),(104,106),(109,111),(114,116),(118,121),(123,126),(128,130),(133,135),(138,140),(143,145),(147,150),(152,155),(157,159),(162,164),(167,169),(172,174),(176,178),(181,183),(186,188),(191,193),(196,198),(200,203),(205,207),(210,212),(215,217),(220,222),(225,227),(229,232),(234,236),(239,241),(244,246),(249,251),(253,256),(258,261),(263,265),(268,270),(273,275),(277,280),(282,285),(287,290),(292,295)]
centers=[(a+b)/2 for a,b in runs]
# day i = daylight after night i: columns between center i and center i+1
YB=83.5; YT=4.0  # baseline row and approx top of plot
days=[]
for i in range(len(runs)):
  lo=centers[i]; hi=centers[i+1] if i+1<len(runs) else W
  cols=[x for x in range(W) if lo< x <=hi]
  # 2D local maxima in rows 0..81
  pts=[]
  for x in cols:
    for y in range(1,82):
      v=P[y][x]
      if v<70: continue
      ok=True
      for dx in (-1,0,1):
        for dy in (-1,0,1):
          if (dx or dy) and 0<=x+dx<W and P[y+dy][x+dx]>v: ok=False
      if ok:
        # subpixel y centroid
        s=sum(P[y+d][x] for d in (-1,0,1)); cy=y+(P[y+1][x]-P[y-1][x])/max(s,1)
        pts.append((x,round(cy,2),v))
  # profile: ink by row
  prof=[sum(P[y][x] for x in cols) for y in range(H)]
  days.append(dict(i=i,pts=pts,prof=prof[:82]))
for d in days:
  ys=sorted(p[1] for p in d['pts'])
  print(d['i'], len(ys), ys[:3], 'ink',sum(d['prof'][:80]))
json.dump(days,open('days.json','w'))
