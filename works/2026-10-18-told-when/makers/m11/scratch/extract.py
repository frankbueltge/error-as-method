import json
d=open('rec.raw','rb').read();W,H=300,90
C=[5.5,10.1,14.5,19.3,23.8,28.4,33,37.5,42.4,46.8,51.5,56,60.6,65.4,69.7,74.5,78.9,83.5]
def dark(x,L):
    c=C[L];ys=[y for y in range(int(c-1.5),int(c+2.5)) if 0<=y<H]
    return max(255-d[y*W+x] for y in ys)
M=[[dark(x,L) for L in range(18)] for x in range(W)]
N=1464
vals=[];prev=None
for i in range(N):
    xf=(i+0.5)*W/N; x=min(W-1,int(xf))
    # combine neighbouring columns weighted
    sc=[M[x][L] for L in range(18)]
    cand=[L for L in range(18) if sc[L]>90]
    if not cand:
        cand=[max(range(18),key=lambda L:sc[L])]
    if prev is None: v=min(cand,key=lambda L:-sc[L])
    else: v=min(cand,key=lambda L:(abs(L-prev),-sc[L]))
    vals.append(v);prev=v
lv=[17-v for v in vals]  # 0=lowest,17=highest
json.dump(lv,open('series.json','w'))
print(''.join('%x'%min(15,a) if a<16 else 'G' if a==16 else 'H' for a in lv))
# daily cycle
days=[lv[k*24:(k+1)*24] for k in range(61)]
import statistics as s
prof=[0]*24
for dd in days:
    m=s.mean(dd)
    for h in range(24): prof[h]+=dd[h]-m
print([round(p/61,2) for p in prof])
print([round(s.mean(dd),1) for dd in days])
print([max(dd)-min(dd) for dd in days])
