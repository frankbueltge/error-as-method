from PIL import Image
import math,json
im=Image.open('/tmp/claude-0/s130/mk/m16/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
NV=1464; X0=2.0; X1=297.0
colof=[int(round(X0+i*(X1-X0)/(NV-1))) for i in range(NV)]
groups={}
for i,c in enumerate(colof): groups.setdefault(c,[]).append(i)
# observed values per column via ink quantiles
obs={}
for c,hs in groups.items():
    pix=[]
    for y in range(H):
        d=max(0,215-px[c,y])/215
        if d>0.12: pix.append((y,d))
    k=len(hs)
    if not pix: obs[c]=[None]*k; continue
    # cluster runs to find dots: split weighted distribution into k quantile slices, take weighted centroid of each
    tot=sum(d for _,d in pix)
    vals=[]
    for j in range(k):
        lo=tot*j/k; hi=tot*(j+1)/k; acc=0; sy=0; sw=0
        for y,d in pix:
            a0=acc; a1=acc+d; acc=a1
            ov=max(0,min(a1,hi)-max(a0,lo))
            sy+=ov*y; sw+=ov
        vals.append(sy/sw)
    obs[c]=vals  # ascending y
# model: smooth mean + 24h harmonic (2 harmonics) with sliding window via columns
def model_params(center_h, halfw=60):
    pts=[]
    for c,hs in groups.items():
        tc=sum(hs)/len(hs)
        if abs(tc-center_h)<=halfw and obs[c][0] is not None:
            for v in obs[c]: pts.append((tc,v))
    return pts
# simple approach: per column mean + sliding fit of daily waveform using column means at their mean time
cm=[(sum(groups[c])/len(groups[c]), sum(obs[c])/len(obs[c])) for c in sorted(groups) if obs[c][0] is not None]
def solve(A,b):
    n=len(A)
    M=[row[:]+[b[i]] for i,row in enumerate(A)]
    for i in range(n):
        p=max(range(i,n),key=lambda r:abs(M[r][i])); M[i],M[p]=M[p],M[i]
        for r in range(n):
            if r!=i:
                f=M[r][i]/M[i][i]
                for k in range(i,n+1): M[r][k]-=f*M[i][k]
    return [M[i][n]/M[i][i] for i in range(n)]
def fitlocal(t0,hw=84):
    rows=[];ys=[]
    for t,v in cm:
        if abs(t-t0)<=hw:
            w=2*math.pi*t/24
            rows.append([1,(t-t0)/24,math.cos(w),math.sin(w),math.cos(2*w),math.sin(2*w)]); ys.append(v)
    n=len(rows[0])
    A=[[sum(r[i]*r[j] for r in rows) for j in range(n)] for i in range(n)]
    b=[sum(r[i]*y for r,y in zip(rows,ys)) for i in range(n)]
    return solve(A,b)
pred=[]
for h in range(NV):
    p=fitlocal(h)
    w=2*math.pi*h/24
    pred.append(p[0]+p[2]*math.cos(w)+p[3]*math.sin(w)+p[4]*math.cos(2*w)+p[5]*math.sin(2*w))
series=[None]*NV
for c,hs in groups.items():
    if obs[c][0] is None: continue
    order=sorted(hs,key=lambda h:pred[h])  # smallest predicted y first
    for h,v in zip(order,obs[c]): series[h]=v
json.dump({'series':series,'pred':pred},open('/tmp/claude-0/s130/mk/m16/scratch/series.json','w'))
print(sum(s is None for s in series))
# phase of daily max (min y) from global fit
p=fitlocal(732,hw=800)
print('global',p)
# fold
fold=[[] for _ in range(24)]
for h,s in enumerate(series):
    if s is not None: fold[h%24].append(s)
for i,f in enumerate(fold):
    f.sort(); print(i, round(f[len(f)//2],1), round(sum(f)/len(f),1))
