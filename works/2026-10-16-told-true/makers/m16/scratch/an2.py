import json,math
cols=json.load(open('/tmp/claude-0/s130/mk/m16/scratch/cols.json'))
ink=[c for c in cols if c[1]>0.3]
x0=ink[0][0]; x1=ink[-1][0]
print('x extent',x0,x1, 'ymin',min(c[4] for c in ink),'ymax',max(c[5] for c in ink))
N=x1-x0+1; dt=1464/N
print('N',N,'dt',dt)
ms=[(c[0]-x0,c[2]) for c in cols if c[1]>0.3]
mu=sum(m for _,m in ms)/len(ms)
res=[]
P=8.0
while P<800:
    f=1/P
    a=sum((m-mu)*math.cos(2*math.pi*f*(x+0.5)*dt) for x,m in ms)
    b=sum((m-mu)*math.sin(2*math.pi*f*(x+0.5)*dt) for x,m in ms)
    res.append((math.hypot(a,b)*2/len(ms),P))
    P*=1.005
loc=[r for i,r in enumerate(res) if 0<i<len(res)-1 and r[0]>res[i-1][0] and r[0]>res[i+1][0]]
for r in sorted(loc,reverse=True)[:15]: print('%.3f px amp at period %.2f h'%r)
