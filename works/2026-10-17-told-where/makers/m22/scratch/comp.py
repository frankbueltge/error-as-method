from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m22/work/record.jpg').convert('L')
W,H=im.size;px=im.load()
D=[[max(0,255-px[x,y]) for x in range(W)] for y in range(H)]
T=30
seen=set();comps=[]
for y in range(H):
  for x in range(W):
    if D[y][x]>T and (x,y) not in seen:
      st=[(x,y)];seen.add((x,y));pts=[]
      while st:
        a,b=st.pop();pts.append((a,b))
        for da in(-1,0,1):
          for db in(-1,0,1):
            c,e=a+da,b+db
            if 0<=c<W and 0<=e<H and (c,e) not in seen and D[e][c]>T:
              seen.add((c,e));st.append((c,e))
      S=sum(D[b][a] for a,b in pts)
      cx=sum(a*D[b][a] for a,b in pts)/S; cy=sum(b*D[b][a] for a,b in pts)/S
      comps.append(dict(S=S,x=cx,y=cy,n=len(pts),x0=min(a for a,b in pts),x1=max(a for a,b in pts),y0=min(b for a,b in pts),y1=max(b for a,b in pts)))
import collections
print(len(comps))
Ss=sorted(c['S'] for c in comps if c['y1']<80)
print(Ss[::10])
big=[c for c in comps if c['y0']>=79]
print('baseline comps',len(big), sorted(round(c['S']) for c in big)[:10], sorted(round(c['S']) for c in big)[-5:])
json.dump(comps,open('comps.json','w'))
