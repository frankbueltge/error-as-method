from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m11/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
N=1464; x0=3.0; x1=296.0; s=(x1-x0)/(N-1)
prof=[]; means=[]
for x in range(W):
    ink=[max(0,230-p[x,y]) for y in range(H)]
    t=sum(ink); prof.append(ink)
    means.append(sum(y*i for y,i in enumerate(ink))/t if t else None)
cols={}
for i in range(N):
    cols.setdefault(int(round(x0+i*s)),[]).append(i)
ys=[0.0]*N
for x,idx in cols.items():
    ink=prof[x]; t=sum(ink); n=len(idx)
    cum=0; q=[]; targets=[(k+0.5)/n*t for k in range(n)]; k=0
    for y in range(H):
        prev=cum; cum+=ink[y]
        while k<n and targets[k]<=cum:
            f=(targets[k]-prev)/ink[y] if ink[y] else 0.5
            q.append(y-0.5+f); k+=1
    q=sorted(q)
    a=means[x-1] or means[x]; b=means[x+1] or means[x]
    if b<a: q=q[::-1]   # values rising (y falling)
    for j,i in enumerate(idx): ys[i]=q[j]
print(min(ys),max(ys))
vals=[round(90-y,1) for y in ys]
open('values.txt','w').write('\n'.join(map(str,vals)))
# daily summaries
for d in range(61):
    v=vals[d*24:(d+1)*24]
    print(d+1, min(v), max(v), round(sum(v)/24,1), v.index(max(v)), v.index(min(v)))
