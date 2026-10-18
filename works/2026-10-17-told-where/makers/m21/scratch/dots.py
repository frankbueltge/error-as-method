from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m21/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
# local minima detection above baseline
dots=[]
for y in range(0,90):
  for x in range(W):
    v=px[x,y]
    if v>200: continue
    nb=[px[i,j] for i in range(max(0,x-1),min(W,x+2)) for j in range(max(0,y-1),min(H,y+2)) if (i,j)!=(x,y)]
    if v<=min(nb):
      dots.append((x,y,v))
print(len(dots))
import collections
c=collections.Counter(y for x,y,v in dots)
print(sorted(c.items()))
json.dump(dots,open('dots.json','w'))
