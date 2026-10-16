from PIL import Image, ImageDraw
import math, json
im=Image.open('/tmp/claude-0/s130/mk/m03/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
X0,X1=3.0,296.3; N=1464
D=[[max(0.0,(225-p[x,y])/225) for y in range(H)] for x in range(W)]
def xi(i): return X0+i*(X1-X0)/(N-1)
# isolated components (spikes / strays)
dark=[[p[x,y]<170 for y in range(H)] for x in range(W)]
seen=set(); comps=[]
for x in range(W):
  for y in range(H):
    if dark[x][y] and (x,y) not in seen:
      st=[(x,y)]; seen.add((x,y)); c=[]
      while st:
        a,b=st.pop(); c.append((a,b))
        for da in (-1,0,1):
          for db in (-1,0,1):
            u,v=a+da,b+db
            if 0<=u<W and 0<=v<H and dark[u][v] and (u,v) not in seen: seen.add((u,v)); st.append((u,v))
      comps.append(c)
# a component is isolated if no other ink (D>0.25) within a ring 3px around it (excluding itself)
iso=[]
for c in comps:
  cs=set(c); xs=[a for a,b in c]; ys=[b for a,b in c]
  near=0
  for a in range(min(xs)-3,max(xs)+4):
    for b in range(min(ys)-4,max(ys)+5):
      if 0<=a<W and 0<=b<H and (a,b) not in cs and D[a][b]>0.3:
        if min(abs(a-u)+abs(b-v) for u,v in c)>1: near+=1
  if near==0 and len(c)<=6:
    w=[D[a][b] for a,b in c]; iso.append((sum(a*q for (a,b),q in zip(c,w))/sum(w), sum(b*q for (a,b),q in zip(c,w))/sum(w)))
print('isolated dots',len(iso))
# per hour: profile at x_i (interpolated), take quantiles among the hours sharing a nearest column
groups={}
for i in range(N):
  groups.setdefault(int(round(xi(i))),[]).append(i)
val=[None]*N
prev=None
for c in sorted(groups):
  hrs=groups[c]; k=len(hrs)
  prof=[D[c][y] for y in range(H)]
  tot=sum(prof)
  if tot<1e-6: prof=[D[c-1][y] for y in range(H)]; tot=sum(prof)
  cum=0; qs=[]; targets=[(j+0.5)/k*tot for j in range(k)]; t=0
  for y in range(H):
    lo=cum; cum+=prof[y]
    while t<k and targets[t]<=cum:
      qs.append(y+ (targets[t]-lo)/max(prof[y],1e-9) -0.5); t+=1
  while len(qs)<k: qs.append(qs[-1])
  # order: monotone, starting nearest prev
  asc=sorted(qs); desc=asc[::-1]
  if prev is not None and abs(desc[0]-prev)<abs(asc[0]-prev): o=desc
  else: o=asc
  # but alternate with a zigzag to avoid artificial sawtooth: interleave around median? keep monotone
  for h,v in zip(hrs,o): val[h]=v
  prev=o[-1]
# inject isolated dots: nearest hour, replace
for x,y in iso:
  i=round((x-X0)*(N-1)/(X1-X0)); i=max(0,min(N-1,i))
  # choose among hours i-2..i+2 the one whose value is farthest in same direction
  cand=range(max(0,i-2),min(N,i+3))
  j=min(cand,key=lambda h: abs(val[h]-y) if False else -abs(val[h]-y)*0+abs(h-i))
  val[j]=y
# convert y to value: v = (Ymax - y) normalized 0..1 by the record's own extremes
ys=val; lo,hi=min(ys),max(ys)
vals=[ (hi-y)/(hi-lo) for y in ys]
json.dump({'y':[round(v,2) for v in ys],'v':[round(v,4) for v in vals],'iso':iso},open('recon.json','w'))
# redraw for comparison
out=Image.new('L',(W,H*2+4),255); d=ImageDraw.Draw(out)
out.paste(im,(0,0))
for i,y in enumerate(ys):
  x=xi(i); d.ellipse([x-0.8,H+4+y-0.8,x+0.8,H+4+y+0.8],fill=40)
out=out.resize((W*4,(H*2+4)*4),Image.NEAREST); out.save('compare.png')
print('range y',lo,hi)
