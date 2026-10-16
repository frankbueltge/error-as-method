from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m13/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
D=[[max(0,235-px[x,y]) for y in range(H)] for x in range(W)]
out=[]
for x in range(1,W-1):
    for y in range(1,H-1):
        v=D[x][y]
        if v<70: continue
        nb=[D[x+i][y+j] for i in(-1,0,1) for j in(-1,0,1) if (i,j)!=(0,0)]
        if v>=max(nb):
            # strict tie-breaking: skip if an earlier neighbour equals
            if any(D[x+i][y+j]==v for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1)]): continue
            sw=sx=sy=0
            for i in(-1,0,1):
                for j in(-1,0,1):
                    w=D[x+i][y+j]; sw+=w; sx+=w*(x+i); sy+=w*(y+j)
            out.append((round(sx/sw,2),round(sy/sw,2),v))
print(len(out))
import json; json.dump(out,open('blobs.json','w'))
