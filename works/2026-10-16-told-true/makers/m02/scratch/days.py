from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m02/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
x0=2.0; P=(298-2)/61.0
print('P',P)
days=[]
for d in range(61):
    a=x0+d*P; b=a+P
    ys=[];ws=[]
    for x in range(W):
        # fractional overlap of pixel [x,x+1) with [a,b)
        ov=max(0,min(x+1,b)-max(x,a))
        if ov<=0: continue
        for y in range(H):
            w=(255-p[x,y])/255
            if w>0.25: ys.append(y); ws.append(w*ov)
    t=sum(ws); m=sum(y*w for y,w in zip(ys,ws))/t
    s=sorted(zip(ys,ws)); c=0; q10=q90=None
    for y,w in s:
        c+=w
        if q10 is None and c>=0.1*t: q10=y
        if q90 is None and c>=0.9*t: q90=y
    days.append((d,round(m,1),min(ys),max(ys),q10,q90))
for r in days: print(r, ' '*int(90-r[1])+'*')
m=[r[1] for r in days]; mu=sum(m)/61; dd=[v-mu for v in m]
for lag in range(1,15):
    print(lag, round(sum(dd[i]*dd[i+lag] for i in range(61-lag))/sum(v*v for v in dd),2))
