import json
grid=json.load(open('grid.json'))
X0=2.8; XL=296.0; N=1464
pph=(XL-X0)/(N-1)
runs=[]
for L,row in enumerate(grid):
    x=0
    while x<300:
        if row[x]>100:
            a=x
            while x<300 and row[x]>100: x+=1
            b=x-1
            # dot ~2.5px wide: centers lie within [a+0.6, b-0.6]
            ca=a+0.4; cb=b-0.4
            if cb<ca: ca=cb=(a+b)/2
            ta=max(0,(ca-X0)/pph); tb=min(N-1,(cb-X0)/pph)
            runs.append([L,round(ta,1),round(max(tb,ta+1),1)])
        else: x+=1
print(len(runs))
hours=sum(r[2]-r[1] for r in runs); print('covered hours',hours)
# coverage per hour
cov=[0]*N
for L,a,b in runs:
    for h in range(int(a),min(N,int(b)+1)): cov[h]+=1
print('hours uncovered',sum(1 for c in cov if c==0))
# daily mean level & daily min/max
for d in range(0,61,5):
    ls=[L for L,a,b in runs if a<(d+1)*24 and b>d*24]
    print(d,min(ls),max(ls))
json.dump(runs,open('runs.json','w'),separators=(',',':'))
