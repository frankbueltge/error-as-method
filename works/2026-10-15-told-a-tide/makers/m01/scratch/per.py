import math
rows=[l.split() for l in open('cols.txt')]
xs=[];sd=[];mn=[]
for r in rows:
    x=int(r[0])
    if 3<=x<=295: xs.append(x); sd.append(float(r[3])); mn.append(float(r[2]))
def pg(v,label):
    m=sum(v)/len(v); v=[a-m for a in v]
    res=[]
    for i in range(300,1600):
        P=i/100  # period in px
        c=sum(a*math.cos(2*math.pi*x/P) for a,x in zip(v,xs)); s=sum(a*math.sin(2*math.pi*x/P) for a,x in zip(v,xs))
        res.append((c*c+s*s,P))
    res.sort(reverse=True)
    print(label,[(round(p,2),round(P*1464/295/1,2)) for p,P in [(r[1],r[1]) for r in res[:12]]])
    print(' power top', [round(r[0]) for r in res[:5]])
pg(sd,'sd'); pg(mn,'mean')
