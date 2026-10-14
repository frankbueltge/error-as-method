from PIL import Image
import math
im=Image.open('/tmp/claude-0/s124/mk/m08/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cols=[]
for x in range(W):
  ws=[max(0,255-px[x,y]-25) for y in range(H)]
  s=sum(ws)
  if s==0: cols.append((x,0,None,None,None)); continue
  m=sum(y*w for y,w in enumerate(ws))/s
  ys=[y for y in range(H) if 255-px[x,y]>90]
  cols.append((x,s,m,min(ys) if ys else None,max(ys) if ys else None))
for c in cols: print(*[round(v,1) if isinstance(v,float) else v for v in c])
