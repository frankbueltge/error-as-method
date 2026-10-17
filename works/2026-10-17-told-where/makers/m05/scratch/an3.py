from PIL import Image
import math
im=Image.open('/tmp/claude-0/s133/mk/m05/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
d=[[max(0,255-p[x,y])/255 for x in range(W)] for y in range(H)]
P=4.82; x0=3.9
nb=5
ink=[[0]*nb for _ in range(9)]; cnt=[0]*nb
for x in range(W):
    ph=((x-x0)/P)%1
    b=int(ph*nb)
    cnt[b]+=1
    for y in range(H):
        ink[min(8,y//10)][b]+=d[y][x]
print('phase bins (0=floor centre)',cnt)
for r in range(9):
    print(r*10, ' '.join('%5.1f'%(ink[r][b]/cnt[b]*10) for b in range(nb)))
