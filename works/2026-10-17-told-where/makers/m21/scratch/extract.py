from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m21/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
D=lambda x,y: max(0,255-px[x,y]) if 0<=x<W and 0<=y<H else 0
out=[]
for y in range(H):
  for x in range(W):
    v=px[x,y]
    if v>205: continue
    nb=[px[i,j] for i in range(max(0,x-1),min(W,x+2)) for j in range(max(0,y-1),min(H,y+2)) if (i,j)!=(x,y)]
    if v>min(nb) : continue
    s=sx=sy=0
    for i in range(x-1,x+2):
      for j in range(y-1,y+2):
        d=D(i,j); s+=d; sx+=d*i; sy+=d*j
    out.append([round(sx/s+0.5,2), round(sy/s+0.5,2), round((255-v)/255,2)])
print(len(out))
# baseline level
bl=[o for o in out if o[1]>82.5 and o[1]<85.5]
print('baseline n',len(bl), sum(o[1] for o in bl)/len(bl))
print('min y', min(o[1] for o in out if o[2]>0.5))
print('below', [o for o in out if o[1]>85.5])
json.dump(out,open('dots2.json','w'),separators=(',',':'))
