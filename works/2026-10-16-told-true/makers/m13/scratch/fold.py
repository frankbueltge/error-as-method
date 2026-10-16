from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m13/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
dark=[[max(0,230-px[x,y]) for y in range(H)] for x in range(W)]
cols=[x for x in range(W) if max(dark[x])>80]
print('data x range',cols[0],cols[-1])
top=[]
for x in range(W):
    ys=[y for y in range(H) if dark[x][y]>80]
    top.append(min(ys) if ys else None)
xs=[x for x in range(W) if top[x] is not None]
def d(x):
    win=[top[i] for i in range(max(0,x-10),min(W,x+11)) if top[i] is not None]
    return top[x]-sum(win)/len(win)
best=None
for p1000 in range(4700,5000,5):
    p=p1000/1000
    c=sum(d(x)*math.cos(2*math.pi*x/p) for x in xs); s=sum(d(x)*math.sin(2*math.pi*x/p) for x in xs)
    a=math.hypot(c,s)
    if not best or a>best[0]: best=(a,p,math.atan2(s,c))
print(best)
# first half vs second half stability
for lo,hi in [(0,150),(150,300)]:
    p=best[1]
    xx=[x for x in xs if lo<=x<hi]
    c=sum(d(x)*math.cos(2*math.pi*x/p) for x in xx); s=sum(d(x)*math.sin(2*math.pi*x/p) for x in xx)
    print(lo,hi,round(math.atan2(s,c),2))
# fold: mean detrended top by phase bins
p=best[1]; nb=10; acc=[[] for _ in range(nb)]
for x in xs: acc[int(((x/p)%1)*nb)].append(d(x))
print([round(sum(a)/len(a),1) for a in acc])
