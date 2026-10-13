from PIL import Image
import json
im=Image.open('/tmp/claude-0/s123/mk/m12/work/record.jpg').convert('L')
W,H=im.size
ink=[[max(0,235-im.getpixel((x,y))) for x in range(W)] for y in range(H)]
pts=[]
for y in range(1,H-1):
    for x in range(1,W-1):
        v=ink[y][x]
        if v<60: continue
        nb=[ink[y+j][x+i] for j in (-1,0,1) for i in (-1,0,1) if i or j]
        if all(v>=n for n in nb):
            # tie-break: skip if equal neighbor earlier in raster order
            if any(ink[y+j][x+i]==v and (j<0 or (j==0 and i<0)) for j in (-1,0,1) for i in (-1,0,1) if i or j): continue
            s=sx=sy=0
            for j in (-1,0,1):
                for i in (-1,0,1):
                    w=ink[y+j][x+i]; s+=w; sx+=w*(x+i+.5); sy+=w*(y+j+.5)
            pts.append((round(sx/s,2),round(sy/s,2),round(s)))
print(len(pts), sum(p[2] for p in pts)/len(pts))
xs=[p[0] for p in pts]; print(min(xs),max(xs))
json.dump(pts,open('pts.json','w'))
