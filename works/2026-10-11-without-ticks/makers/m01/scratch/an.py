d=open('births.raw','rb').read();W,H=480,220
px=lambda x,y:d[y*W+x]
cols=[x for x in range(W) if any(px(x,y)<160 for y in range(H))]
rows=[y for y in range(H) if any(px(x,y)<160 for x in range(W))]
print(cols[0],cols[-1],rows[0],rows[-1])
# row histogram of darkness
for y in range(H):
  s=sum(255-px(x,y) for x in range(W))
  print(y, '#'*(s//400))
