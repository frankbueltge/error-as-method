from PIL import Image
g=Image.open('/tmp/claude-0/s128/mk/m06/work/record.jpg').convert('L'); W,H=g.size; p=g.load()
hp=1464/W
bins=[[0]*H for _ in range(12)]
for x in range(W):
  h=((x+0.5)*hp)%24; b=int(h/2)
  for y in range(H): bins[b][y]+=255-p[x,y]
for b in range(12):
  s=sum(bins[b]); m=sum(v*y for y,v in enumerate(bins[b]))/s
  # quantiles
  acc=0;q={}
  for y,v in enumerate(bins[b]):
    acc+=v
    for t in(.1,.5,.9):
      if t not in q and acc>=t*s: q[t]=y
  print(b*2, round(m,1), q)
# day by day: per-day column mean range
