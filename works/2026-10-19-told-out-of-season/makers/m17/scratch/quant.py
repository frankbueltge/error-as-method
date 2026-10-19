import json
from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m17/work/record.jpg').convert('L'); W,H=im.size; p=im.load()
N=1464; X0,X1=3.0,297.4
xs=[X0+(X1-X0)*h/(N-1) for h in range(N)]
cols={}
for h,x in enumerate(xs): cols.setdefault(int(round(x)),[]).append(h)
prof={}
for x in cols:
    w=[max(0,(255-p[x,y])-60) for y in range(H)]
    prof[x]=w
Y=[None]*N; last=None
xsorted=sorted(cols)
for i,x in enumerate(xsorted):
    w=prof[x]; tot=sum(w); hs=cols[x]; n=len(hs)
    ys=[y for y in range(H) if w[y]>0]
    lo,hi=min(ys),max(ys)
    if last is None: start_top=True
    else: start_top = abs(last-lo) <= abs(last-hi)   # y small = high value
    order=list(range(H)) if start_top else list(range(H-1,-1,-1))
    # quantiles along traversal
    c=0;qs=[];targets=[(k+0.5)/n*tot for k in range(n)];j=0
    for y in order:
        c2=c+w[y]
        while j<n and targets[j]<=c2:
            f=(targets[j]-c)/w[y] if w[y] else 0.5
            qs.append(y+(f-0.5 if start_top else 0.5-f)); j+=1
        c=c2
    for h,yv in zip(hs,qs): Y[h]=round(yv,2)
    last=Y[hs[-1]]
json.dump(Y,open('q.json','w'))
print(sum(v is None for v in Y))
