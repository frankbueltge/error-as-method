from PIL import Image
g=Image.open('../work/record.jpg').convert('L'); W,H=g.size; p=g.load()
D=[[max(0,(235-p[x,y]))/235.0 for x in range(W)] for y in range(H)]
seen=set(); comps=[]
for y in range(H):
  for x in range(W):
    if D[y][x]>0.35 and (x,y) not in seen:
      st=[(x,y)]; seen.add((x,y)); px=[]
      while st:
        a,b=st.pop(); px.append((a,b))
        for da in (-1,0,1):
          for db in (-1,0,1):
            c,e=a+da,b+db
            if 0<=c<W and 0<=e<H and (c,e) not in seen and D[e][c]>0.35:
              seen.add((c,e)); st.append((c,e))
      # mass including halo
      m=0;sx=0;sy=0
      for a,b in px:
        w=D[b][a]; m+=w; sx+=w*a; sy+=w*b
      comps.append((m,sx/m,sy/m,len(px)))
import collections
ms=sorted(c[0] for c in comps)
print(len(comps)); print([round(ms[int(i*len(ms)/20)],2) for i in range(20)])
small=[c for c in comps if c[1]>0]
h=collections.Counter(round(c[0]*2)/2 for c in comps)
print(sorted(h.items())[:30])
print('total mass',sum(ms))
