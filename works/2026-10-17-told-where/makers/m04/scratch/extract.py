from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s133/mk/m04/work/record.jpg').convert('L');px=im.load()
W,H=im.size
D=[[max(0,255-px[x,y]-12)/243.0 for x in range(W)] for y in range(H)]
# kill JPEG ringing below floor
# matching pursuit with 2x2-ish gaussian blob
sig=0.75
def tmpl(cx,cy):
    out=[]
    for y in range(int(cy)-2,int(cy)+4):
        for x in range(int(cx)-2,int(cx)+4):
            if 0<=x<W and 0<=y<H:
                g=math.exp(-((x-cx)**2+(y-cy)**2)/(2*sig*sig))
                out.append((x,y,g))
    return out
# normalising: an ideal dot centred at pixel centre+0.5 => amplitude
dots=[]
R=[row[:] for row in D]
for it in range(4000):
    best=0;bx=by=0
    for y in range(H):
        r=R[y]
        for x in range(W-1):
            v=r[x]+r[x+1]+(R[y+1][x]+R[y+1][x+1] if y+1<H else 0)
            if v>best: best=v;bx=x;by=y
    if best<0.9: break
    # centroid in 3x3 around 2x2
    sw=sx=sy=0
    for y in range(by-1,by+3):
        for x in range(bx-1,bx+3):
            if 0<=x<W and 0<=y<H:
                w=R[y][x]; sw+=w; sx+=w*x; sy+=w*y
    cx=sx/sw; cy=sy/sw
    amp=None
    t=tmpl(cx,cy)
    # subtract one dot of fixed peak 1 (saturating at 0)
    for x,y,g in t:
        R[y][x]=max(0,R[y][x]-g*1.0)
    dots.append((round(cx,2),round(cy,2)))
print(len(dots))
json.dump(dots,open('/tmp/claude-0/s133/mk/m04/scratch/dots.json','w'))
