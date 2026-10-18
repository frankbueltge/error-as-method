import sys
d=open('rec.raw','rb').read(); W,H=300,90
px=lambda x,y:255-d[y*W+x]
rows=[sum(px(x,y) for x in range(W)) for y in range(H)]
for y in range(H): print(y,rows[y])
cols=[sum(px(x,y) for y in range(H)) for x in range(W)]
print('cols', cols)
