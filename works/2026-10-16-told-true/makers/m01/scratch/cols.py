from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s130/mk/m01/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cols=[]
for x in range(W):
    ys=[(y,255-px[x,y]) for y in range(H) if px[x,y]<170]
    cols.append(ys)
# per-column: weighted mean, top, bottom
stat=[]
for x,ys in enumerate(cols):
    if not ys: stat.append(None); continue
    w=sum(d for y,d in ys); m=sum(y*d for y,d in ys)/w
    stat.append((min(y for y,_ in ys),max(y for y,_ in ys),m,w))
empty=[x for x,s in enumerate(stat) if s is None]
print('empty cols',empty)
print('ink per col sample',[round(s[3]) if s else 0 for s in stat[:40]])
# mean series
m=[s[2] if s else None for s in stat]
# fill
m=m[2:298]; W=len(m)
mu=sum(m)/W
d=[v-mu for v in m]
def ac(l): return sum(d[i]*d[i+l] for i in range(W-l))/sum(v*v for v in d)
for l in range(1,45): print(l, round(ac(l),3), round(l*1464/296/24,2),'days')
# top-row series
tops=[s[0] if s else None for s in stat]; bots=[s[1] if s else None for s in stat]
print('tops',tops[2:298]); print('bots',bots[2:298])
json.dump({'cols':cols},open('cols.json','w'))
