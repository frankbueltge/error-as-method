import json
P=json.load(open('/tmp/claude-0/s133/mk/m13/scratch/px.json'))
f=[(P[83][x]+P[84][x])/2 for x in range(300)]
# light = 255-f ; find local light centroids between dark clusters
L=[max(0,200-v) for v in f]
cents=[];x=0
while x<300:
    if L[x]>0:
        s=x
        while x<300 and L[x]>0: x+=1
        w=sum(L[s:x]); c=sum((i+0.5)*L[i] for i in range(s,x))/w
        cents.append((round(c,2),round(w)))
    else: x+=1
print(len(cents));print(cents)
cs=[c for c,w in cents[1:-1] if w>100]
n=len(cs);ks=list(range(n))
mk=sum(ks)/n;mc=sum(cs)/n
b=sum((k-mk)*(c-mc) for k,c in zip(ks,cs))/sum((k-mk)**2 for k in ks);a=mc-b*mk
print('period',b,'first',a, 'resid',max(abs(c-(a+b*k)) for k,c in zip(ks,cs)))
