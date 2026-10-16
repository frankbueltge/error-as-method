from PIL import Image
import json
im=Image.open('/tmp/claude-0/s130/mk/m15/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
d=[[max(0,255-p[x,y]-25) for y in range(H)] for x in range(W)]
b=json.load(open('blobs.json'))
out=[]
for x,y,v in b:
  cx,cy=int(round(x)),int(round(y))
  m=sum(d[cx+i][cy+j] for i in (-1,0,1) for j in (-1,0,1) if 0<=cx+i<W and 0<=cy+j<H)
  out.append([x,y,m])
ms=sorted(q[2] for q in out);print(ms[len(ms)//2],ms[0],ms[-1])
# compact string
s=';'.join('%.1f,%.1f,%d'%(x,y,round(m/10)) for x,y,m in out)
open('data.txt','w').write(s);print(len(s))
