from PIL import Image
import json
im=Image.open('/tmp/claude-0/s135/mk/m03/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
centers=[5.5,10,14.5,19,23.5,28.5,33,37.5,42.5,46.5,51.5,56,60.5,65.5,69.5,74.5,79,83.5]
# darkness per column per level: min over rows within +-2
G=[]
for x in range(W):
    col=[]
    for c in centers:
        rows=[r for r in range(int(c-2),int(c+2)+1) if 0<=r<H]
        col.append(255-min(p[x,r] for r in rows))
    G.append(col)
json.dump({'centers':centers,'G':G},open('grid.json','w'))
# per column min/max occupied level (dark>110)
for x in range(W):
    occ=[i for i,v in enumerate(G[x]) if v>110]
    print(x, occ)
