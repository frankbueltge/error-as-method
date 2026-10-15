import math
rows=[l.split() for l in open('cols.txt')]
d={int(r[0]):r for r in rows}
xs=list(range(3,297))
for k,name in [(3,'top'),(4,'bot'),(5,'mean')]:
    s=[float(d[x][k]) for x in xs]
    m=sum(s)/len(s); s=[v-m for v in s]
    n=len(s)
    print(name)
    best=[]
    for i in range(1,400):
        per=1.5+i*0.05 if i<200 else 11.5+(i-200)*0.5
        f=1/per
        c=sum(v*math.cos(2*math.pi*f*j) for j,v in enumerate(s)); q=sum(v*math.sin(2*math.pi*f*j) for j,v in enumerate(s))
        best.append(((c*c+q*q)/n,per))
    for p,per in sorted(best,reverse=True)[:8]: print('  per %.2f px = %.1f h, power %.1f'%(per,per*1464/300.0*1,p))
