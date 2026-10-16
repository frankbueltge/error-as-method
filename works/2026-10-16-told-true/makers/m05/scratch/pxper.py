import math
d=[l.split() for l in open('cols.txt')]
xs=[];ys=[]
for r in d:
    if r[1]!='-': xs.append(int(r[0])+0.5);ys.append(-float(r[5]))
m=sum(ys)/len(ys); y=[v-m for v in ys]
best=[]
for i in range(4500,5300):
    P=i/1000
    w=2*math.pi/P
    c=sum(v*math.cos(w*a) for v,a in zip(y,xs)); s=sum(v*math.sin(w*a) for v,a in zip(y,xs))
    best.append((math.hypot(c,s),P))
best.sort(reverse=True); print(best[:3])
# half-power width
pk=best[0][0]; ws=[P for a,P in best if a>pk*0.707]; print(min(ws),max(ws))
