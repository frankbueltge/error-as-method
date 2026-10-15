import sys,math
d=open('/tmp/claude-0/s128/mk/m09/scratch/gray.pgm','rb').read()
parts=d.split(b'\n',3); w,h=map(int,parts[1].split()); px=parts[3]
x0,x1=float(sys.argv[1]),float(sys.argv[2])
pts=[]
for x in range(w):
    for y in range(h):
        i=255-px[y*w+x]-40
        if i>0: pts.append(((x+0.5-x0)/(x1-x0)*1463, h-y, i))
W=sum(p[2] for p in pts); mu=sum(p[1]*p[2] for p in pts)/W
def power(P):
    c=sum((p[1]-mu)*p[2]*math.cos(2*math.pi*p[0]/P) for p in pts); s=sum((p[1]-mu)*p[2]*math.sin(2*math.pi*p[0]/P) for p in pts)
    return (c*c+s*s)/W/W
best=max(((power(P/1000),P/1000) for P in range(23000,25000,10)))
print("best",best)
P=float(sys.argv[3]) if len(sys.argv)>3 else best[1]
nb=24
bins=[[0,0] for _ in range(nb)]
hist=[[0]*h for _ in range(nb)]
for t,v,i in pts:
    b=int((t%P)/P*nb)%nb; bins[b][0]+=v*i; bins[b][1]+=i; hist[b][h-v]+=i
for b in range(nb):
    col=hist[b]; tot=sum(col)
    print("%2d mean=%.1f "%(b,bins[b][0]/bins[b][1]) + ''.join(" .:-=+*#%@"[min(9,int(c/tot*60))] for c in col))
