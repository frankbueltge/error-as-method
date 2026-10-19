from PIL import Image
import json
im=Image.open('/tmp/claude-0/s137/mk/m05/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
# horizontal extent of ink
cols=[x for x in range(W) if any(p[x,y]<150 for y in range(H))]
x0,x1=cols[0],cols[-1]
N=1464
def centers(x):
    if x<0 or x>=W: return []
    c=[]
    for y in range(H):
        v=p[x,y]
        if v<170 and (y==0 or v<=p[x,y-1]) and (y==H-1 or v<p[x,y+1]):
            c.append(y)
    return c
# hours per column
byc={}
for i in range(N):
    x=x0+(i+0.5)*(x1+1-x0)/N
    byc.setdefault(int(x),[]).append(i)
vals=[None]*N
prev=None
for x in sorted(byc):
    hrs=byc[x]; c=sorted(centers(x))
    if not c: c=[prev] if prev is not None else [50]
    n=len(hrs)
    # resample to n by quantiles
    if len(c)!=n:
        c=[c[min(len(c)-1,int(round(k*(len(c)-1)/max(1,n-1))))] for k in range(n)] if len(c)>1 else c*n
    c=sorted(c)
    # ordering: continue decline (larger y) from prev, then jump up and decline
    if prev is not None:
        cont=[y for y in c if y>=prev-3]
        rest=[y for y in c if y<prev-3]
        if cont and rest:
            c=sorted(cont)+sorted(rest)
    for h,y in zip(hrs,c): vals[h]=y
    prev=c[-1]
v=[round((H-y)/H*100,1) for y in vals]
json.dump({'x0':x0,'x1':x1,'v':v},open('series.json','w'))
print(x0,x1,len(v),min(v),max(v))
# re-render check
out=Image.new('L',(W,H),255); q=out.load()
for i,y in enumerate(vals):
    q[int(x0+(i+0.5)*(x1+1-x0)/N),y]=0
out.save('rerender.png')
