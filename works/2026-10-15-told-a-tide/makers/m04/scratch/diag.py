import json,sys
S=json.load(open('samples.json'))
X0,X1=2.6,296.4; HP=1463/(X1-X0)
t=lambda x:(x-X0)/(X1-X0)*1463
P=float(sys.argv[1]); mode=sys.argv[2]
n=int(1464//P)+1
# hourly grid: weighted mean y and min y via box of +-HP/2
grid=[[0,0] for _ in range(1464)]
mn=[99]*1464
for x,y,d in S:
  c=t(x)
  for h in range(int(c-HP/2)+1,int(c+HP/2)+1):
    if 0<=h<1464:
      grid[h][0]+=d*y; grid[h][1]+=d
      if d>0.3: mn[h]=min(mn[h],y)
mean=[a/b if b else None for a,b in grid]
val = mn if mode=='top' else [max(y for x,y,d in [(0,0,0)]) for _ in range(0)]
if mode=='mean': val=mean
chars=' .:-=+*#%@'
for r in range(n):
  line=''
  for k in range(48):
    h=int(r*P+k*P/48)
    if h>=1464: line+=' '; continue
    v=val[h]
    line+=chars[max(0,min(9,int((v-15)/5)))] if v is not None else '?'
  print('%2d %s'%(r,line))
