from PIL import Image
im=Image.open('/tmp/claude-0/s124/mk/m10/work/record.jpg').convert('L'); px=im.load(); W,H=im.size
D=[[255-px[x,y] for y in range(H)] for x in range(W)]
out=[]
for x in range(1,W-1):
  for y in range(1,H-1):
    v=D[x][y]
    if v<70: continue
    nb=[D[x+i][y+j] for i in (-1,0,1) for j in (-1,0,1)]
    if v<max(nb): continue
    # tie-break: skip if an earlier neighbor equal
    if any(D[x+i][y+j]==v and (i,j)<(0,0) for i in (-1,0,1) for j in (-1,0,1)): continue
    s=sum(nb); cx=sum(D[x+i][y+j]*i for i in (-1,0,1) for j in (-1,0,1))/s; cy=sum(D[x+i][y+j]*j for i in (-1,0,1) for j in (-1,0,1))/s
    out.append((x+cx, (H-1)-(y+cy), v))
print(len(out))
import collections
print(collections.Counter(round((o[0]%1),1) for o in out))
open('blobs.txt','w').write(','.join(f'{x:.2f},{y:.2f},{v//16}' for x,y,v in out))
