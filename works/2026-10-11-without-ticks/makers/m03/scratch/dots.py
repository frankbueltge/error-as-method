import pickle, json, random, math
random.seed(7)
W=1100
C,comps=pickle.load(open('cc.pkl','rb'))
areas=[sum(C[j] for j in p) for p in comps]
singles=sorted(a for a,p in zip(areas,comps) if len(p)<=16 and a<7)
print('single-ish areas median',singles[len(singles)//2], 'n',len(singles))
A1=singles[len(singles)//2]
est=[m*(5479/sum(pickle.load(open("mass.pkl","rb")))) for m in pickle.load(open("mass.pkl","rb"))]
base=sum(max(1,round(e)) for e in est)
print('naive count',base)
# scale multi-dot components to reach 5479
multi=sum(e for e in est if round(e)>=2); single=sum(1 for e in est if round(e)<2)
f=(5479-single)/multi; print('scale for multis',f)
ns=[]
for e in est:
    n=max(1,round(e)) if round(e)<2 else e*f
    ns.append(n)
# integerize with largest remainder to exactly 5479
fl=[int(n) for n in ns]; rem=5479-sum(fl)
order=sorted(range(len(ns)),key=lambda i:-(ns[i]-fl[i]))
for i in order[:rem]: fl[i]+=1
print('total',sum(fl))
dots=[]
for p,n in zip(comps,fl):
    pts=[((j%W)+0.5,(j//W)+0.5,C[j]) for j in p]
    if n==1:
        w=sum(c for _,_,c in pts); dots.append((sum(x*c for x,_,c in pts)/w,sum(y*c for _,y,c in pts)/w)); continue
    # k-means++ weighted
    cs=[max(pts,key=lambda t:t[2])[:2]]
    while len(cs)<n:
        dd=[min((x-a)**2+(y-b)**2 for a,b in cs)*c for x,y,c in pts]
        s=sum(dd)
        if s==0: cs.append(pts[random.randrange(len(pts))][:2]); continue
        r=random.random()*s; acc=0
        for (x,y,c),v in zip(pts,dd):
            acc+=v
            if acc>=r: cs.append((x,y)); break
    for it in range(25):
        sx=[0]*n; sy=[0]*n; sw=[0]*n
        for x,y,c in pts:
            k=min(range(n),key=lambda k:(x-cs[k][0])**2+(y-cs[k][1])**2)
            sx[k]+=x*c; sy[k]+=y*c; sw[k]+=c
        cs=[(sx[k]/sw[k],sy[k]/sw[k]) if sw[k]>0 else cs[k] for k in range(n)]
    dots.extend(cs)
json.dump(dots,open('dots_px.json','w'))
print(len(dots))
