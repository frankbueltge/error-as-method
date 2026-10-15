import math
rows=[l.split() for l in open('cols.txt')]
d={int(r[0]):r for r in rows}
xs=list(range(3,297))
H=1463/294.0  # hours per px approx
for k,name in [(3,'top'),(4,'bot'),(5,'mean')]:
    s=[float(d[x][k]) for x in xs]; m=sum(s)/len(s); s=[v-m for v in s]; n=len(s)
    out=[]
    for i in range(0,1000):
        per=10+i*0.02
        f=H/per
        c=sum(v*math.cos(2*math.pi*f*j) for j,v in enumerate(s)); q=sum(v*math.sin(2*math.pi*f*j) for j,v in enumerate(s))
        out.append(((c*c+q*q)/n,per))
    print(name,[ '%.2fh:%.0f'%(per,p) for p,per in sorted(out,reverse=True)[:3]])
    for target in (12.0,12.42,12.66,23.93,24.0,24.84,25.82):
        p=min(out,key=lambda o:abs(o[1]-target)); print('   %.2f -> %.0f'%(target,p[0]))
