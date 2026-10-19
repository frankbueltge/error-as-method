import math
rows=[l.split() for l in open('cols.txt')]
m=[float(r[4]) for r in rows[3:205]]
# fold periodogram
best=[]
for P10 in range(400,560):
    P=P10/100
    re=sum(v*math.cos(2*math.pi*i/P) for i,v in enumerate(m)); im=sum(v*math.sin(2*math.pi*i/P) for i,v in enumerate(m))
    best.append((math.hypot(re,im),P))
best.sort(reverse=True); print(best[:5])
