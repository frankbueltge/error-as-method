from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s130/mk/m03/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
cols=[]
for x in range(W):
    ws=[(y,max(0,230-p[x,y])/230) for y in range(H)]
    m=sum(w for y,w in ws); c=sum(y*w for y,w in ws)/m if m else None
    cols.append((m,c))
# mean centroid per column
cs=[c for m,c in cols]

print('empty',[i for i,c in enumerate(cs) if c is None])
for i in range(W):
    if cs[i] is None:
        j=i
        while j<W and cs[j] is None: j+=1
        a=cs[i-1] if i>0 else cs[j]; b=cs[j] if j<W else a
        cs[i]=(a+b)/2
mu=sum(cs)/len(cs)
d=[c-mu for c in cs]
def ac(l): return sum(d[i]*d[i+l] for i in range(W-l))/sum(v*v for v in d)
print('autocorr',[ (l,round(ac(l),2)) for l in range(1,30)])
# periodogram over period in px
best=[]
for P10 in range(20,400):
    P=P10/10; s=sum(d[i]*math.cos(2*math.pi*i/P) for i in range(W)); c=sum(d[i]*math.sin(2*math.pi*i/P) for i in range(W))
    best.append((s*s+c*c,P))
best.sort(reverse=True); print(best[:12])
# phase fold with period 300/61
P=300/61; bins=[[] for _ in range(8)]
for x in range(W):
    ph=((x+0.5)/P)%1; bins[int(ph*8)].append(d[x])
print([round(sum(b)/len(b),2) for b in bins])
# daily mean centroid
for k in range(61):
    xs=[x for x in range(W) if int((x+0.5)/P)==k]
    print(k, round(sum(cs[x] for x in xs)/len(xs),1), round(min(cs[x] for x in xs),1), round(max(cs[x] for x in xs),1))
