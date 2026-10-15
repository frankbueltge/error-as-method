import sys,math
d=open(sys.argv[1],'rb').read()
parts=d.split(b'\n',3); w,h=map(int,parts[1].split()); px=parts[3]
g=lambda x,y: px[y*w+x]
cent=[];med=[]
for x in range(w):
    ink=[max(0,255-g(x,y)-30) for y in range(h)]
    t=sum(ink)
    cent.append(sum(i*y for y,i in enumerate(ink))/t if t else None)
    # weighted median
    c=0;m=None
    for y,i in enumerate(ink):
        c+=i
        if c>=t/2: m=y;break
    med.append(m)
xs=[x for x in range(w) if med[x] is not None]
v=[h-med[x] for x in xs]
mu=sum(v)/len(v); v=[a-mu for a in v]
print("cols",len(xs))
res=[]
for k in range(1,150):
    f=k/ w
    c=sum(a*math.cos(2*math.pi*f*x) for a,x in zip(v,xs)); s=sum(a*math.sin(2*math.pi*f*x) for a,x in zip(v,xs))
    res.append((c*c+s*s,k, w/k, w/k*1464/300/24))
res.sort(reverse=True)
for r in res[:15]: print("pow %.0f k=%d period_px=%.2f days=%.2f"%r)
print(' '.join(str(m) for m in med))
