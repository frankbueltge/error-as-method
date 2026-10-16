import numpy as np
from PIL import Image
im=np.asarray(Image.open('/tmp/claude-0/s131/mk/m04/work/record.jpg').convert('L')).astype(float)
d=255-im
cols=np.where((d>80).any(0))[0]; rows=np.where((d>80).any(1))[0]
print('x',cols.min(),cols.max(),'y',rows.min(),rows.max())
for x in range(280,300):
    print(x, list(map(int,np.where(d[:,x]>80)[0])))
