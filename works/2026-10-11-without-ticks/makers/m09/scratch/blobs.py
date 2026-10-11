import json
d=json.load(open('gray.json'));g=d['g']
X0,X1,Y0,Y1=81,1079,21,448
dark=lambda x,y: g[y][x]<200
seen=set();blobs=[]
for y in range(Y0,Y1):
  for x in range(X0,X1):
    if dark(x,y) and (x,y) not in seen:
      st=[(x,y)];seen.add((x,y));px=[]
      while st:
        a,b=st.pop();px.append((a,b,g[b][a]))
        for da in(-1,0,1):
          for db in(-1,0,1):
            n=(a+da,b+db)
            if X0<=n[0]<X1 and Y0<=n[1]<Y1 and n not in seen and dark(*n):
              seen.add(n);st.append(n)
      blobs.append(px)
json.dump(blobs,open('blobs.json','w'))
from collections import Counter
print(len(blobs)); print(sorted(Counter(len(b) for b in blobs).items())[:30])
# show an isolated small blob
for b in blobs:
  if len(b) in (4,5,6,7,8,9):
    xs=[p[0] for p in b];ys=[p[1] for p in b]
    print(min(xs),min(ys)); 
    for y in range(min(ys)-1,max(ys)+2): print(' '.join('%3d'%g[y][x] for x in range(min(xs)-1,max(xs)+2)))
    break
