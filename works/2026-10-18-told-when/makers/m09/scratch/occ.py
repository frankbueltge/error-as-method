import sys, json, math
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); w,h=im.size; p=im.load()
c0, step = 5.5, (83.5-5.5)/17
L=18
occ=[]  # occ[x][k] darkness
for x in range(w):
    row=[]
    for k in range(L):
        c=c0+step*k
        s=0
        for y in range(int(c-1.6), int(c+1.6)+1):
            if 0<=y<h: s+=max(0,255-p[x,y]-20)
        row.append(s)
    occ.append(row)
# weighted mean level per column (level 0 = top = highest)
mean=[]
for x in range(w):
    t=sum(occ[x]); mean.append(sum(k*v for k,v in enumerate(occ[x]))/t if t>200 else None)
json.dump({'occ':occ,'mean':mean},open('occ.json','w'))
# detrended autocorrelation
xs=[x for x in range(w) if mean[x] is not None]
# moving-average detrend window 15
def ma(x,r=12):
    v=[mean[i] for i in range(x-r,x+r+1) if 0<=i<w and mean[i] is not None]; return sum(v)/len(v)
d={x:mean[x]-ma(x) for x in xs}
for lag in range(1,16):
    pr=[(d[x],d[x+lag]) for x in xs if x+lag in d]
    a=sum(u*v for u,v in pr)/len(pr); b=sum(u*u for u,v in pr)/len(pr)
    print(lag, round(a/b,3))
