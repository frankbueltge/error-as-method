from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m09/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cols=[]
for x in range(W):
    w=[max(0,235-px[x,y]) for y in range(H)]
    s=sum(w); m=sum(y*w[y] for y in range(H))/s if s else None
    cols.append((s,m))
ms=[c[1] for c in cols]
print("empty",[i for i,v in enumerate(ms) if v is None])
last=45
for i in range(W):
    if ms[i] is None: ms[i]=last
    last=ms[i]
mu=sum(ms)/len(ms)
d=[m-mu for m in ms]
def ac(l): return sum(d[i]*d[i+l] for i in range(W-l))/sum(v*v for v in d)
for l in range(1,40): print(l, round(ac(l),3), round(l*24*61/300,1),'h')
# fold by daily phase
for nb in [6]:
    b=[[] for _ in range(nb)]
    for x in range(W):
        ph=((x+0.5)*61/300)%1
        b[int(ph*nb)].append(ms[x])
    print([round(sum(v)/len(v),2) for v in b])
# trend: mean y per day-block
print([round(sum(ms[int(i*300/61):int((i+1)*300/61)])/len(ms[int(i*300/61):int((i+1)*300/61)]),1) for i in range(61)])
print('ink',[c[0] for c in cols[:20]])
print('---periodogram (hours)')
res=[]
for i in range(800):
    Ph=8+i*0.05  # hours
    P=Ph*300/1464
    c=sum(d[x]*math.cos(2*math.pi*x/P) for x in range(W)); s=sum(d[x]*math.sin(2*math.pi*x/P) for x in range(W))
    res.append((c*c+s*s,Ph))
res2=sorted(res,reverse=True)
for p,ph in res2[:25]: print(round(ph,2), round(p))
# local maxima
print('peaks')
for i in range(1,len(res)-1):
    if res[i][0]>res[i-1][0] and res[i][0]>res[i+1][0] and res[i][0]>2000: print(round(res[i][1],2), round(res[i][0]))
