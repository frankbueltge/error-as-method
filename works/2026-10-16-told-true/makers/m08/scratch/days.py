from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s130/mk/m08/work/record.jpg').convert('L'); p=im.load()
W,H=im.size
wt=[[max(0,(225-p[x,y]))/225 for y in range(H)] for x in range(W)]
N=61; days=[]
for d in range(N):
    a=d*W/N; b=(d+1)*W/N
    h=[0.0]*H
    x=int(a)
    while x<b:
        f=min(b,x+1)-max(a,x)
        for y in range(H): h[y]+=f*wt[x][y]
        x+=1
    s=sum(h); h=[v*24/s for v in h]   # ink -> hours
    days.append(h)
# vertical extent
lo=min(y for y in range(H) if any(dd[y]>0.02 for dd in days)); hi=max(y for y in range(H) if any(dd[y]>0.02 for dd in days))
print(lo,hi)
for d in range(0,N,6):
    h=days[d]; c=0; med=None
    for y in range(H):
        c+=h[y]
        if c>=12 and med is None: med=y
    print(d, med, round(sum(h[:45]),2))
json.dump({'r0':lo,'r1':hi,'days':[[round(v,3) for v in h[lo:hi+1]] for h in days]},open('/tmp/claude-0/s130/mk/m08/scratch/days.json','w'),separators=(',',':'))
