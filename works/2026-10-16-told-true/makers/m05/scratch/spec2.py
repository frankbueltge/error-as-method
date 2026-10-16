import math
d=[l.split() for l in open('cols.txt')]
xs=[];ys=[]
for r in d:
    if r[1]!='-': xs.append(int(r[0]));ys.append(-float(r[5]))
hpp=1464/296; t=[(x-2+0.5)*hpp for x in xs]
m=sum(ys)/len(ys); y=[v-m for v in ys]
def amp(P,yy=y,tt=t):
    w=2*math.pi/P
    c=sum(v*math.cos(w*a) for v,a in zip(yy,tt)); s=sum(v*math.sin(w*a) for v,a in zip(yy,tt))
    return 2*math.hypot(c,s)/len(yy), math.atan2(s,c)
for P in [12.0,12.42,12.66,11.97,23.0,23.5,23.93,24.0,24.07,24.5,25.0,25.82,26.87,8.0,8.28]:
    print(P,[round(v,2) for v in amp(P)])
# windowed amplitude of 23.93 over 6-day windows
print('windowed')
for s0 in range(0,1464-144,48):
    idx=[i for i,a in enumerate(t) if s0<=a<s0+144]
    yy=[y[i] for i in idx]; mm=sum(yy)/len(yy); yy=[v-mm for v in yy]
    a,ph=amp(24.0,yy,[t[i] for i in idx]); print(s0//24, round(a,2), round(math.degrees(ph)))
