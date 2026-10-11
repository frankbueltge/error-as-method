import json, math
W,H=1100,500
d=bytearray(open('img.raw','rb').read())
X0,X1,Y0,Y1=81,1080,10,449   # plot interior (exclude axis cols 79,80 and axis row 449-450)
# gridline baseline per row: mode of row values in plot
from collections import Counter
base={}
for y in range(Y0,Y1):
    c=Counter(d[y*W+x] for x in range(X0,X1)).most_common(1)[0][0]
    if c<255: base[y]=c
print('gridrows',base)
# gridline centers (darkness-weighted)
def center(rows):
    w=[(255-base[r]) for r in rows]; return sum((r+0.5)*wi for r,wi in zip(rows,w))/sum(w)
rows=sorted(base); groups=[]
for r in rows:
    if groups and r-groups[-1][-1]==1: groups[-1].append(r)
    else: groups.append([r])
gc=[center(g) for g in groups]; print('grid centers',gc)
FULL=221.0
C=[0.0]*(W*H)
for y in range(Y0,Y1):
    b=base.get(y,255)
    for x in range(X0,X1):
        v=min(255,d[y*W+x]*255/b)
        C[y*W+x]=min(1.0,max(0.0,(255-v)/FULL))
tot=sum(C); print('total coverage',tot,'-> dots if no overlap',tot/4.93)
# connected components on C>0.05
seen=bytearray(W*H); comps=[]
for y in range(Y0,Y1):
  for x in range(X0,X1):
    i=y*W+x
    if C[i]>0.05 and not seen[i]:
      st=[i]; seen[i]=1; pix=[]
      while st:
        j=st.pop(); pix.append(j); jx,jy=j%W,j//W
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
          nx,ny=jx+dx,jy+dy
          if X0<=nx<X1 and Y0<=ny<Y1:
            k=ny*W+nx
            if C[k]>0.05 and not seen[k]: seen[k]=1; st.append(k)
      comps.append(pix)
sizes=Counter()
for p in comps:
    a=sum(C[j] for j in p); sizes[round(a/4.93)]+=1
print('components',len(comps),sorted(sizes.items())[:30], max(sizes))
json.dump({'gc':gc},open('calib.json','w'))
import pickle; pickle.dump((C,comps),open('cc.pkl','wb'))
