from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s135/mk/m04/work/record.jpg').convert('L')
w,h=im.size;p=im.load()
K=18
c=[5.5+78/17*k for k in range(K)]
D=[]
for x in range(w):
    row=[]
    for k in range(K):
        y0=int(round(c[k]-1.5)); s=0
        for y in range(max(0,y0),min(h,y0+3)): s+=max(0,200-p[x,y])
        row.append(s)
    D.append(row)
# occupancy threshold
occ=[[1 if v>150 else 0 for v in r] for r in D]
first=min(x for x in range(w) if any(occ[x])); last=max(x for x in range(w) if any(occ[x]))
print('x range',first,last)
mean=[]
for x in range(w):
    t=sum(D[x]); mean.append(sum(k*v for k,v in enumerate(D[x]))/t if t>200 else None)
# column count & coverage
print('empty cols',[x for x in range(first,last+1) if not any(occ[x])])
# daily folding
span=(last-first+1)
ppd=span/61
# detrend with 1-day running mean
xs=[x for x in range(first,last+1) if mean[x] is not None]
bins=[[] for _ in range(5)]
for x in xs:
    nb=[mean[j] for j in range(x-3,x+4) if 0<=j<w and mean[j] is not None]
    r=mean[x]-sum(nb)/len(nb)
    ph=((x-first+0.5)/ppd)%1
    bins[int(ph*5)].append(r)
for i,b in enumerate(bins): print('phase %d-%dh'%(i*24/5,(i+1)*24/5), round(sum(b)/len(b),3), len(b))
json.dump({'occ':occ,'D':D,'first':first,'last':last},open('occ.json','w'))
for x in range(first,last+1,5): print(x, ''.join('#' if occ[x][k] else '.' for k in range(K)), round(mean[x],2) if mean[x] else None)
