from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s130/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
x0,x1=2,297; ppd=(x1+1-x0)/61
S=[(x,y,255-px[x,y]) for x in range(W) for y in range(H) if 255-px[x,y]>60]
print('samples',len(S),'ppd',ppd)
# column upper envelope (value) & lower
col={}
for x,y,d in S: col.setdefault(x,[]).append((89-y,d))
up=[];lo=[]
for x in range(x0,x1+1):
    vs=sorted(v for v,d in col.get(x,[]) if d>100)
    up.append(vs[-1] if vs else None); lo.append(vs[0] if vs else None)
# detrend upper-minus-lower spread and fold by phase
spread=[(u-l) if u is not None else 0 for u,l in zip(up,lo)]
for name,arr in (('top',up),('bottom',lo),('spread',spread)):
    a=[v if v is not None else 0 for v in arr]
    # remove running mean
    n=len(a); r=[a[i]-sum(a[max(0,i-5):i+6])/len(a[max(0,i-5):i+6]) for i in range(n)]
    best=[]
    for P10 in range(40,60):
        P=P10/10; c=sum(r[i]*math.cos(2*math.pi*i/P) for i in range(n)); s=sum(r[i]*math.sin(2*math.pi*i/P) for i in range(n))
        best.append((round(math.hypot(c,s)),P,round(math.atan2(s,c)/(2*math.pi)*P,2)))
    best.sort(reverse=True); print(name,best[:4])
