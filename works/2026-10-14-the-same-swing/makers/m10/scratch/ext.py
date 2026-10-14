from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s124/mk/m10/work/record.jpg').convert('L'); w,h=im.size; px=im.load()
cols=[]
for x in range(w):
    ys=[(h-1-y, 255-px[x,y]) for y in range(h) if px[x,y]<150]
    cols.append(ys)
xs=[x for x in range(w) if cols[x]]
print('x range',xs[0],xs[-1], 'ylo/hi', min(min(y for y,_ in c) for c in cols if c), max(max(y for y,_ in c) for c in cols if c))
mean=[]; lo=[]; hi=[]
for c in cols:
    if not c: mean.append(None); lo.append(None); hi.append(None); continue
    s=sum(wt for _,wt in c); mean.append(sum(y*wt for y,wt in c)/s); lo.append(min(y for y,_ in c)); hi.append(max(y for y,_ in c))
json.dump({'mean':mean,'lo':lo,'hi':hi,'cols':cols},open('cols.json','w'))
m=[v for v in mean if v is not None]; n=len(m); mu=sum(m)/n; d=[v-mu for v in m]
# periodogram
best=[]
for k in range(1,150):
    re=sum(d[i]*math.cos(2*math.pi*k*i/n) for i in range(n)); im_=sum(d[i]*math.sin(2*math.pi*k*i/n) for i in range(n))
    best.append((re*re+im_*im_,k,n/k))
for p,k,per in sorted(best,reverse=True)[:12]: print(k, round(per,2),'px', round(per*1464/n/24,2),'days?', round(p))
