from PIL import Image
import math
im=Image.open('../work/record.jpg').convert('L'); W,H=im.size; p=im.load()
cols=[]
for x in range(W):
    w=[max(0,235-p[x,y]) for y in range(H)]
    s=sum(w)
    if s==0: cols.append(None); continue
    m=sum(y*v for y,v in enumerate(w))/s
    # top: first y with cumulative 10%, 50%, 90%
    c=0;q={}
    for y,v in enumerate(w):
        c+=v
        for f in (0.1,0.5,0.9):
            if f not in q and c>=f*s: q[f]=y
    cols.append((m,s,q[0.1],q[0.5],q[0.9]))
tot=sum(c[1] for c in cols if c)
print('total ink',tot,'per value',tot/1464)
med=[c[3] for c in cols]
mean=[c[0] for c in cols]
# autocorrelation of mean, detrended by 15-col moving avg
n=len(mean)
def detr(a,k=15):
    out=[]
    for i in range(n):
        lo=max(0,i-k//2);hi=min(n,i+k//2+1)
        out.append(a[i]-sum(a[lo:hi])/(hi-lo))
    return out
for name,a in (('mean',mean),('med',med),('ink',[c[1] for c in cols]),('p10',[c[2] for c in cols]),('p90',[c[4] for c in cols])):
    d=detr(a)
    v=sum(t*t for t in d)
    ac=[sum(d[i]*d[i+L] for i in range(n-L))/v for L in range(1,40)]
    print(name,' '.join(f'{L+1}:{x:+.2f}' for L,x in enumerate(ac[:30])))
# periodogram over periods 2..60 px
for name,a in (('mean',mean),('p90',[c[4] for c in cols])):
    d=detr(a,31)
    res=[]
    for P10 in range(21,300):
        P=P10/10
        re=sum(d[i]*math.cos(2*math.pi*i/P) for i in range(n));im_=sum(d[i]*math.sin(2*math.pi*i/P) for i in range(n))
        res.append((re*re+im_*im_,P))
    res.sort(reverse=True); print(name,[ (round(pw),P,round(P*1464/300,1)) for pw,P in res[:12]])
print([round(m) for m in mean])
print([c[2] for c in cols]); print([c[4] for c in cols])
