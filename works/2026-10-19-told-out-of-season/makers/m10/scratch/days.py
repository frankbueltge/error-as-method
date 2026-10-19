import json
from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m10/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
TH=170
# clusters per column: runs of dark pixels, darkness-weighted centre
pts=[]
for x in range(W):
    run=[]
    for y in range(H+1):
        v=px[x,y] if y<H else 255
        if v<TH: run.append((y,255-v))
        elif run:
            # split long runs into ~2px dots
            n=max(1,round(len(run)/2.2))
            k=len(run)/n
            for i in range(n):
                seg=run[int(i*k):int((i+1)*k)] or run[-1:]
                w=sum(d for _,d in seg); c=sum(yy*d for yy,d in seg)/w
                pts.append((x,c))
            run=[]
xs=[p[0] for p in pts]; x0,x1=min(xs),max(xs)
print('x range',x0,x1,'npts',len(pts))
span=(x1-x0+1)/61
import sys
phase=float(sys.argv[1]) if len(sys.argv)>1 else 0
days=[]
for d in range(61):
    a=x0+phase+d*span; b=a+span
    ys=[y for x,y in pts if a<=x+0.5<b] if d<60 else [y for x,y in pts if a<=x+0.5]
    if d==0: ys=[y for x,y in pts if x+0.5<b]
    days.append((min(ys),max(ys),len(ys)))
for i,(lo,hi,n) in enumerate(days): print(i,round(lo,1),round(hi,1),n)
json.dump({'pts':[(x,round(y,1)) for x,y in pts],'days':days,'x0':x0,'x1':x1},open('/tmp/claude-0/s137/mk/m10/scratch/data.json','w'))
