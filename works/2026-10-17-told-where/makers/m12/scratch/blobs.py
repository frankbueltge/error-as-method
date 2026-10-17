from PIL import Image
import json,sys
im=Image.open('/tmp/claude-0/s133/mk/m12/work/record.jpg').convert('L')
W,H=im.size
px=[[255-im.getpixel((x,y)) for x in range(W)] for y in range(H)]
# floor rows
rowsum=[sum(r) for r in px]
for y in range(78,90): print(y,rowsum[y])
colsum=[sum(px[y][x] for y in range(H)) for x in range(W)]
print('first/last nonzero cols',[x for x in range(W) if colsum[x]>200][:3],[x for x in range(W) if colsum[x]>200][-3:])
