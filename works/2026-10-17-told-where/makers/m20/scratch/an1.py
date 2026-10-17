from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m20/work/record.jpg').convert('L')
w,h=im.size; px=im.load()
# darkness per column at rows 82-85
for r in (82,83,84,85):
    print(r, [255-px[x,r] for x in range(0,30)])
row=[sum(255-px[x,r] for r in (83,84)) for x in range(w)]
# find runs
runs=[];cur=None
for x in range(w):
    d=row[x]>150
    if d and cur is None: cur=x
    if not d and cur is not None: runs.append((cur,x-1)); cur=None
if cur is not None: runs.append((cur,w-1))
print(len(runs))
cs=[]
for a,b in runs:
    c=sum(x*row[x] for x in range(a,b+1))/sum(row[x] for x in range(a,b+1)); cs.append(c)
print([round(c,2) for c in cs])
import statistics
n=len(cs); xs=list(range(n)); mx=sum(xs)/n; my=sum(cs)/n
sl=sum((i-mx)*(c-my) for i,c in zip(xs,cs))/sum((i-mx)**2 for i in xs)
print('slope',sl,'intercept',my-sl*mx)
print([round(c-(my-sl*mx+sl*i),2) for i,c in enumerate(cs)])
# horizontal extent of any dark pixel
dk=[x for x in range(w) if any(px[x,y]<160 for y in range(h))]
print(dk[0],dk[-1])
dy=[y for y in range(h) if any(px[x,y]<160 for x in range(w))]
print(dy[0],dy[-1])
