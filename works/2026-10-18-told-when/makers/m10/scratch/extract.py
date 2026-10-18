from PIL import Image
import json
im=Image.open('/tmp/claude-0/s135/mk/m10/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
D=[[255-p[x,y] for x in range(W)] for y in range(H)]
rows=[sum(D[y]) for y in range(H)]
cols=[sum(D[y][x] for y in range(H)) for x in range(W)]
print('rows',[ (y,r) for y,r in enumerate(rows) if r>300])
dc=[x for x in range(W) if cols[x]>150]
print('xrange',dc[0],dc[-1])
