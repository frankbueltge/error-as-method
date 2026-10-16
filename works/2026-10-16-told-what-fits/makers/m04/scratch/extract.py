import numpy as np
from PIL import Image
im=np.asarray(Image.open('/tmp/claude-0/s131/mk/m04/work/record.jpg').convert('L')).astype(float)
print(im.shape, im.min(), im.max())
H,W=im.shape
d=255-im
# per column: list dark runs
for x in range(W):
    col=d[:,x]
    ys=np.where(col>80)[0]
    print(x, list(ys))
