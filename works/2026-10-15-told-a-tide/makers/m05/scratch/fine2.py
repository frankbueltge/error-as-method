import json,math
cols=json.load(open('cols.json'))
for x0,x1 in ((2.5,295.5),(3,295),(2,296)):
    hpp=1463/(x1-x0)
    def per(fn,name):
        xs=[((i-x0)*hpp,fn(r)) for i,r in enumerate(cols) if r]
        m=sum(v for _,v in xs)/len(xs)
        best=[]
        for k in range(1000,3200,2):
            P=k/100
            c=sum((v-m)*math.cos(2*math.pi*t/P) for t,v in xs);s=sum((v-m)*math.sin(2*math.pi*t/P) for t,v in xs)
            best.append((c*c+s*s,P))
        best.sort(reverse=True)
        return [b[1] for b in best[:3]]
    print(x0,x1,'bottom',per(max,'b'),'count',per(len,'n'))
