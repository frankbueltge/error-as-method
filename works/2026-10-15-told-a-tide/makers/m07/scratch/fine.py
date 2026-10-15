import math
d=[l.split() for l in open('colstats.txt')]
xs=[int(a) for a,b,c in d if b!='None']; m=[float(b) for a,b,c in d if b!='None']; s=[float(c) for a,b,c in d if c!='None']
hpc=1464/(297-2+1)
print('h per col',hpc)
def pg(ys,lo,hi,step):
    mu=sum(ys)/len(ys); out=[]
    P=lo
    while P<hi:
        c=sum((y-mu)*math.cos(2*math.pi*x/P) for x,y in zip(xs,ys)); sn=sum((y-mu)*math.sin(2*math.pi*x/P) for x,y in zip(xs,ys))
        out.append((round(P*hpc,2), round(2*math.hypot(c,sn)/len(ys),2))); P+=step
    return out
for P,a in pg(m,4.3,5.6,0.03): print(P,a,'#'*int(a*4))
print('semi')
for P,a in pg(m,2.2,2.9,0.02): print(P,a,'#'*int(a*4))
print('long')
for P,a in pg(m,20,200,6): print(P/24,a,'#'*int(a*2))
