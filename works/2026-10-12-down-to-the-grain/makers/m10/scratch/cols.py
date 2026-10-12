import sys, math
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); W,H=im.size; p=im.load()
cols=[]
for x in range(W):
  tw=sum(max(0,255-p[x,y]-20) for y in range(H))
  my=sum(y*max(0,255-p[x,y]-20) for y in range(H))/tw if tw else None
  lo=hi=None
  for y in range(H):
    if 255-p[x,y]>100:
      if lo is None: lo=y
      hi=y
  cols.append((x,tw,my,lo,hi))
for c in cols: print(c[0], c[1], None if c[2] is None else round(c[2],1), c[3], c[4])
