import sys
W,H=480,220
b=open('births.raw','rb').read()
px=[[b[y*W+x] for x in range(W)] for y in range(H)]
# histogram
h=[0]*256
for r in px:
  for v in r: h[v]+=1
print('hist dark bins', [(i,h[i]) for i in range(0,256,16)], sum(h[:128]), sum(h[:200]))
cols=[sum(1 for y in range(H) if px[y][x]<160) for x in range(W)]
xs=[x for x in range(W) if cols[x]>0]; print('x extent',xs[0],xs[-1])
rows=[sum(1 for x in range(W) if px[y][x]<160) for y in range(H)]
ys=[y for y in range(H) if rows[y]>0]; print('y extent',ys[0],ys[-1])
print('rows', rows)
print('cols', cols)
