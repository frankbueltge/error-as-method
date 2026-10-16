from PIL import Image
import math, cmath
im=Image.open('/tmp/claude-0/s130/mk/m17/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
ink=[[max(0,(235-px[x,y]))/235 for y in range(H)] for x in range(W)]
S=[sum(c) for c in ink]
print('empty cols',[x for x in range(W) if S[x]<0.3])
rows=[sum(ink[x][y] for x in range(W)) for y in range(H)]
print('rows with ink',[y for y in range(H) if rows[y]>0.3][:3],[y for y in range(H) if rows[y]>0.3][-3:])
print(' '.join('%.1f'%s for s in S))
