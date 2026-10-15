from PIL import Image
im=Image.open('../work/record.jpg').convert('L'); W,H=im.size; p=im.load()
D=[[max(0,240-p[x,y]) for x in range(W)] for y in range(H)]
# smooth 3x3 box
S=[[0]*W for _ in range(H)]
for y in range(H):
    for x in range(W):
        s=0
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                yy,xx=y+dy,x+dx
                if 0<=yy<H and 0<=xx<W: s+=D[yy][xx]*(2 if dx==0 and dy==0 else 1)
        S[y][x]=s
pk=[]
for y in range(H):
    for x in range(W):
        v=S[y][x]
        if v<250: continue
        if all(v>=S[y+dy][x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if 0<=y+dy<H and 0<=x+dx<W and (dy or dx)):
            sw=sx=sy=0
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    yy,xx=y+dy,x+dx
                    if 0<=yy<H and 0<=xx<W:
                        w=D[yy][xx]; sw+=w; sx+=w*xx; sy+=w*yy
            pk.append((sx/sw,sy/sw,sw))
print(len(pk))
import statistics
ws=[w for _,_,w in pk]; print(statistics.median(ws), min(ws), max(ws))
open('blobs.txt','w').write('\n'.join(f'{a:.2f} {b:.2f} {c}' for a,b,c in pk))
