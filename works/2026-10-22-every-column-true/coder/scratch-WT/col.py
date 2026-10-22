import sys,subprocess,collections
src=open('fit.py').read().split('img=sys.argv')[0]
exec(src)
img=sys.argv[1]; ky,x0,y0=map(float,sys.argv[2:5]); kx=ky*0.775; w,h=1100,800
leg={k:tuple(int(c[i:i+2],16) for i in (1,3,5)) for k,c in zip('9876543',sys.argv[5].split(','))}
raw=subprocess.run(['convert',img,'-depth','8','rgb:-'],capture_output=True).stdout
bg=raw[15:18]
P=[]
for x,(la,lo) in zip(r,pts): P.append((x0+(75.5186-lo)*kx,y0+(39.6889-la)*ky,x))
ok=tot=0; conf=collections.Counter()
for X,Y,x in P:
  if min(((X-a)**2+(Y-b)**2)**.5 for a,b,_ in P if (a,b)!=(X,Y))<10: continue
  best=None
  for dx in range(-5,6):
    for dy in range(-6,2):
      i=(int(Y+dy)*w+int(X+dx))*3; p=raw[i:i+3]
      s=sum(abs(p[k]-bg[k]) for k in range(3))
      if best is None or s>best[0]: best=(s,p)
  if best[0]<80: continue
  p=best[1]
  # nearest legend by normalized chroma (scale)
  def dist(c):
    f=sum(p)/max(1,sum(c)); return sum((p[k]-c[k]*f)**2 for k in range(3))
  g=min(leg,key=lambda k:dist(leg[k]))
  tot+=1; ok+= g==x['LOWEST_RATING']; conf[(x['LOWEST_RATING'],g)]+=1
print(img,ok,tot,sorted(conf.items()))
