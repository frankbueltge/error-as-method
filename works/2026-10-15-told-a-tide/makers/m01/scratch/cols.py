from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m01/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
import math
out=[]
for x in range(W):
    ws=[(y,max(0,200-p[x,y])) for y in range(H)]
    tot=sum(w for y,w in ws)
    if tot==0: out.append((x,0,0,0,0,0));continue
    m=sum(y*w for y,w in ws)/tot
    sd=math.sqrt(sum(w*(y-m)**2 for y,w in ws)/tot)
    dark=[y for y,w in ws if w>60]
    out.append((x,round(tot),round(m,1),round(sd,1),min(dark) if dark else -1,max(dark) if dark else -1))
for o in out: print(*o)
