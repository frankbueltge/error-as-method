import math
d=[l.split() for l in open('cols.txt')]
xs=[];ys=[]
for r in d:
    if r[1]!='-': xs.append(int(r[0]));ys.append(-float(r[5]))
# hours: column x centre -> data from col 2..297 roughly; assume 1464 values spread over cols 2..297
x0,x1=2,297.99
hpp=1464/(x1-x0+0)  # hours per pixel
print('h/px',hpp)
t=[(x-x0+0.5)*hpp for x in xs]
m=sum(ys)/len(ys); y=[v-m for v in ys]
res=[]
for i in range(1,4000):
    P=4+i*0.01  # period hours
    if P>400: break
for P in [x/10 for x in range(97,3000)]:
    w=2*math.pi/P
    c=sum(v*math.cos(w*tt) for v,tt in zip(y,t)); s=sum(v*math.sin(w*tt) for v,tt in zip(y,t))
    res.append((P,(c*c+s*s)/len(y)))
res.sort(key=lambda r:-r[1])
seen=[]
for P,p in res:
    if all(abs(P-q)/q>0.04 for q in seen):
        seen.append(P);print(round(P,1),round(p,1))
    if len(seen)>15:break
