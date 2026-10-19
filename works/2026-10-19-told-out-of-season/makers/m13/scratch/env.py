from PIL import Image
import json
im=Image.open('/tmp/claude-0/s137/mk/m13/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
cols={}
for x in range(W):
    d=[y for y in range(H) if p[x,y]<140]
    if d: cols[x]=(min(d),max(d))
xs=sorted(cols)
prev=None;ent={}
for x in xs:
    a,b=cols[x]
    if prev is None: e,o=a,b
    else:
        e,o=(a,b) if abs(a-prev)<=abs(b-prev) else (b,a)
    ent[x]=(e,o);prev=o
X0,X1=2.0,298.0  # dots occupy columns 2..297
N=1464;k=(X1-X0)/N
vals=[]
for h in range(N):
    u=X0+(h+0.5)*k; c=int(u); f=u-c
    c=min(max(c,xs[0]),xs[-1])
    e,o=ent[c]; y=e+(o-e)*f
    vals.append(y)
v=[90-y for y in vals]; lo,hi=min(v),max(v)
n=[round((a-lo)/(hi-lo),3) for a in v]
json.dump(n,open('hourly.json','w'))
# rise detection: hour of day of largest 5h increase each day
for d in range(61):
    seg=n[d*24:(d+1)*24+6]
    best=max(range(len(seg)-3),key=lambda i:seg[i+3]-seg[i])
    print(d, 'pk %.2f tr %.2f'%(max(n[d*24:(d+1)*24]),min(n[d*24:(d+1)*24])), 'rise@', (best+1)%24, round(seg[best+3]-seg[best],2))
