import json,math
cols=json.load(open('cols.json'))
hpp=1464/300
xs=[(i*hpp+hpp/2,max(r)) for i,r in enumerate(cols) if r]
m=sum(v for _,v in xs)/len(xs)
res=[]
for k in range(1000,3200):
    P=k/100  # hours
    c=sum((v-m)*math.cos(2*math.pi*t/P) for t,v in xs);s=sum((v-m)*math.sin(2*math.pi*t/P) for t,v in xs)
    res.append((c*c+s*s,P))
for a,P in sorted(res,reverse=True)[:10]: print(P,round(a))
for P in (12.0,12.42,23.93,24.0,24.84,25.82):
    c=sum((v-m)*math.cos(2*math.pi*t/P) for t,v in xs);s=sum((v-m)*math.sin(2*math.pi*t/P) for t,v in xs)
    print('at',P,round(c*c+s*s))
