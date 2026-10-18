from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m16/work/record.jpg').convert('L');px=im.load()
W,H=im.size
ink=[[max(0,245-px[x,y]) for y in range(H)] for x in range(W)]
seen=set();comps=[]
for x in range(W):
  for y in range(H):
    if ink[x][y]>60 and (x,y) not in seen:
      st=[(x,y)];seen.add((x,y));pts=[]
      while st:
        a,b=st.pop();pts.append((a,b))
        for da in(-1,0,1):
          for db in(-1,0,1):
            c,d=a+da,b+db
            if 0<=c<W and 0<=d<H and (c,d) not in seen and ink[c][d]>60:
              seen.add((c,d));st.append((c,d))
      comps.append(pts)
# ink of comps including halo
def tot(pts):
  s=set()
  for a,b in pts:
    for da in(-1,0,1):
      for db in(-1,0,1):
        s.add((a+da,b+db))
  return sum(ink[a][b] for a,b in s if 0<=a<W and 0<=b<H)
import collections
up=[c for c in comps if max(b for a,b in c)<80]
sizes=collections.Counter(len(c) for c in up)
print(sorted(sizes.items()))
small=[tot(c) for c in up if len(c)<=2]
small.sort();print(len(small),small[len(small)//2])
allup=sum(ink[x][y] for x in range(W) for y in range(0,82))
print('ink above 82',allup, 'est dots', allup/small[len(small)//2])
bot=sum(ink[x][y] for x in range(W) for y in range(82,90))
print('ink bottom',bot,'est', bot/small[len(small)//2])
