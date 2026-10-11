import sys
W,H=480,220
d=open('births.raw','rb').read()
px=[[d[y*W+x] for x in range(W)] for y in range(H)]
dark=lambda v:v<170
cols=[sum(dark(px[y][x]) for y in range(H)) for x in range(W)]
rows=[sum(dark(px[y][x]) for x in range(W)) for y in range(H)]
xs=[x for x in range(W) if cols[x]>0]; ys=[y for y in range(H) if rows[y]>0]
print('x',xs[0],xs[-1],'y',ys[0],ys[-1])
print('cols',cols[:12],cols[-12:])
for y in range(H): print(y,rows[y],'#'*(rows[y]//4))
