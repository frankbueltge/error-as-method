from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m17/work/record.jpg').convert('L');W,H=im.size
p=im.load()
D=[[255-p[x,y] for x in range(W)] for y in range(H)]
seen=set();blobs=[]
for y in range(H):
  for x in range(W):
    if D[y][x]>60 and (x,y) not in seen:
      st=[(x,y)];seen.add((x,y));pix=[]
      while st:
        a,b=st.pop();pix.append((a,b))
        for da in(-1,0,1):
          for db in(-1,0,1):
            u,v=a+da,b+db
            if 0<=u<W and 0<=v<H and (u,v) not in seen and D[v][u]>60:
              seen.add((u,v));st.append((u,v))
      m=sum(D[b][a] for a,b in pix)
      cx=sum(a*D[b][a] for a,b in pix)/m; cy=sum(b*D[b][a] for a,b in pix)/m
      blobs.append(dict(x=round(cx,2),y=round(cy,2),mass=m,n=len(pix),ymin=min(b for a,b in pix),ymax=max(b for a,b in pix)))
above=[b for b in blobs if b['ymax']<82]
print(len(blobs),len(above))
import statistics
print('mass median',statistics.median(b['mass'] for b in above))
print(sorted(b['mass'] for b in above)[::10])
print('ymin overall',min(b['y'] for b in above))
json.dump(blobs,open('blobs.json','w'))
