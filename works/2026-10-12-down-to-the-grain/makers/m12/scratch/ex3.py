from PIL import Image
import json
im=Image.open('/tmp/claude-0/s122/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
T=205
pk=[]
for x in range(W):
  for y in range(H):
    v=px[x,y]
    if v<T and all(v<=px[x+a,y+b] for a in(-1,0,1) for b in(-1,0,1) if 0<=x+a<W and 0<=y+b<H and (a,b)!=(0,0)):
      s=sx=sy=0
      for a in(-1,0,1):
        for b in(-1,0,1):
          if 0<=x+a<W and 0<=y+b<H:
            w=max(0,235-px[x+a,y+b]); s+=w; sx+=w*(x+a); sy+=w*(y+b)
      pk.append([sx/s,sy/s,v])
# merge close
pk.sort()
out=[]
for p in pk:
  m=None
  for q in out[-6:]:
    if abs(q[0]-p[0])<1.3 and abs(q[1]-p[1])<1.3: m=q
  if m is None: out.append(p)
  elif p[2]<m[2]: m[:]=p
print(len(pk),len(out))
out.sort()
json.dump(out,open('/tmp/claude-0/s122/mk/m12/scratch/peaks.json','w'))
xs=[p[0] for p in out]
import statistics
d=[xs[i+1]-xs[i] for i in range(len(xs)-1)]
print(xs[0],xs[-1],(xs[-1]-xs[0])/1463, max(d))
big=[(round(xs[i]),round(d[i],1)) for i in range(len(d)) if d[i]>3]; print(big)
