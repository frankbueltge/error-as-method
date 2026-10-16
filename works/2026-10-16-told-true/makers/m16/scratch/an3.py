import json,math
cols=json.load(open('/tmp/claude-0/s130/mk/m16/scratch/cols.json'))
x0=2;N=296;dt=1464/N
ms=[(c[0]-x0,c[2]) for c in cols if c[1]>0.3]
def fit(P,lo,hi):
    pts=[(x,m) for x,m in ms if lo<=x<hi]
    n=len(pts); mu=sum(m for _,m in pts)/n
    w=2*math.pi/P
    # simple LSQ with 3 params via normal eq approx (orthogonality)
    a=sum((m-mu)*math.cos(w*(x+.5)*dt) for x,m in pts)*2/n
    b=sum((m-mu)*math.sin(w*(x+.5)*dt) for x,m in pts)*2/n
    return mu,math.hypot(a,b),math.degrees(math.atan2(b,a))
for s in range(0,N-15,5):
    mu,A,ph=fit(24.0,s,s+15)
    day=s*dt/24
    print('day %5.1f mean %5.1f amp24 %5.2f phase %7.1f'%(day,mu,A,ph))
