from PIL import Image
import json
im=Image.open('/tmp/claude-0/s130/mk/m02/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
out=[]
for x in range(2,298):
    pts=[(y,(255-p[x,y])/255) for y in range(H)]
    pts=[(y,w) for y,w in pts if w>0.3]
    t=sum(w for _,w in pts); c=sum(y*w for y,w in pts)/t
    out.append([round(c,1),min(y for y,_ in pts),max(y for y,_ in pts)])
s=json.dumps(out,separators=(',',':'))
open('cols.js','w').write(s); print(len(out), len(s))
cs=sorted(o[0] for o in out); print('median centroid',cs[len(cs)//2])
