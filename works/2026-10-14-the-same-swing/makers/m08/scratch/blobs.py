from PIL import Image
import json
im=Image.open('/tmp/claude-0/s124/mk/m08/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
dark=[[255-px[x,y] for x in range(W)] for y in range(H)]
tot=sum(sum(r) for r in dark)
mask=[[dark[y][x]>90 for x in range(W)] for y in range(H)]
seen=set(); blobs=[]
for y in range(H):
  for x in range(W):
    if mask[y][x] and (x,y) not in seen:
      st=[(x,y)]; seen.add((x,y)); pts=[]
      while st:
        a,b=st.pop(); pts.append((a,b))
        for da in(-1,0,1):
          for db in(-1,0,1):
            c,d=a+da,b+db
            if 0<=c<W and 0<=d<H and mask[d][c] and (c,d) not in seen:
              seen.add((c,d)); st.append((c,d))
      w=sum(dark[b][a] for a,b in pts)
      blobs.append((sum(a*dark[b][a] for a,b in pts)/w, sum(b*dark[b][a] for a,b in pts)/w, w, len(pts)))
print(len(blobs), 'total ink',tot)
ws=sorted(b[2] for b in blobs); print('median ink',ws[len(ws)//2], 'ink/1464', tot/1464)
xs=[b[0] for b in blobs]; ys=[b[1] for b in blobs]
print(min(xs),max(xs),min(ys),max(ys))
json.dump(blobs,open('blobs.json','w'))
