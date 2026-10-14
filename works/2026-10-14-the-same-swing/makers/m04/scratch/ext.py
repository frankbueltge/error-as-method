from PIL import Image
import json,sys
im=Image.open(sys.argv[1]).convert('L');W,H=im.size
cols=[]
for x in range(W):
    d=[max(0,(225-im.getpixel((x,y))))/225 for y in range(H)]
    cols.append(d)
# beads: inverse CDF, value = 1 - y/H (top high)
beads=[];env=[]
for x,d in enumerate(cols):
    n=int((x+1)*36.6)-int(x*36.6)
    tot=sum(d);cum=[0]
    for v in d: cum.append(cum[-1]+v)
    ys=[]
    for k in range(n):
        t=(k+0.5)/n*tot
        for y in range(H):
            if cum[y+1]>=t:
                f=(t-cum[y])/d[y] if d[y] else 0.5
                ys.append(round(1-(y+f)/H,4));break
    beads.append(ys)
    env.append((max(ys),min(ys),sum(ys)/n))
for i,e in enumerate(env): print(i,'%.2f %.2f %.2f range %.2f'%(e[0],e[1],e[2],e[0]-e[1]))
print(sum(len(b) for b in beads))
json.dump({'g':[[im.getpixel((x,y)) for x in range(W)] for y in range(H)],'b':beads},open(sys.argv[2],'w'),separators=(',',':'))
