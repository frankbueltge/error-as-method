import sys
from PIL import Image
im=Image.open(sys.argv[1]).convert('L'); px=im.load(); W,H=im.size
ink=lambda x,y: max(0,255-px[x,y])
colfloor=[sum(ink(x,y) for y in (83,84)) for x in range(W)]
colup=[sum(ink(x,y) for y in range(0,81)) for x in range(W)]
colall=[sum(ink(x,y) for y in range(H)) for x in range(W)]
nz=[x for x in range(W) if colall[x]>200]
print('extent',nz[0],nz[-1])
print('floor ink per col:')
print(' '.join('%d'%(c//100) for c in colfloor))
print('up ink per col:')
print(' '.join('%d'%(c//100) for c in colup))
