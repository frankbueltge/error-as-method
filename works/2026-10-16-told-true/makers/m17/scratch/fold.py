from PIL import Image
import math, cmath
im=Image.open('/tmp/claude-0/s130/mk/m17/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
ink=[[max(0,(235-px[x,y]))/235 for y in range(H)] for x in range(W)]
x0,x1=2.8,296.6
def hr(x): return (x-x0)/(x1-x0)*1463
cols=[]
for x in range(2,298):
    s=sum(ink[x]); m=sum(y*ink[x][y] for y in range(H))/s
    sd=math.sqrt(sum((y-m)**2*ink[x][y] for y in range(H))/s)
    # median
    c=0
    for y in range(H):
        c+=ink[x][y]
        if c>=s/2: med=y;break
    cols.append((x,s,m,sd,med))
mean=sum(c[2] for c in cols)/len(cols)
for P in [8,12,16,20,22,23,23.5,24,24.5,25,26,28,48,72,168,240]:
    z=sum(cmath.exp(2j*math.pi*hr(x)/P)*(med-mean) for x,s,m,sd,med in cols)/len(cols)
    z2=sum(cmath.exp(2j*math.pi*hr(x)/P)*(s-5.4) for x,s,m,sd,med in cols)/len(cols)
    z3=sum(cmath.exp(2j*math.pi*hr(x)/P)*(sd-4) for x,s,m,sd,med in cols)/len(cols)
    print(P,'med %.2f'%abs(z),'ink %.2f'%abs(z2),'sd %.2f'%abs(z3), 'phase med %.1fh'%((-cmath.phase(z))/(2*math.pi)*P%P),'phase sd %.1fh'%((-cmath.phase(z3))/(2*math.pi)*P%P))
B=12
bins=[[] for _ in range(B)]
for x,s,m,sd,med in cols:
    bins[int((hr(x)%24)/24*B)].append((med,sd,s))
for i,b in enumerate(bins):
    n=len(b); print('%4.1fh'%(i*24/B),n,'med %.2f sd %.2f ink %.2f'%(sum(v[0] for v in b)/n,sum(v[1] for v in b)/n,sum(v[2] for v in b)/n))
# trend: 61 daily medians
for d in range(61):
    ys=[med for x,s,m,sd,med in cols if d*24<=hr(x)<(d+1)*24]
    print(d,ys)
