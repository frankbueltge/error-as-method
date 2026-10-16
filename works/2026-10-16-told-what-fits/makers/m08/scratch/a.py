from PIL import Image; import numpy as np
im=np.array(Image.open('/tmp/claude-0/s131/mk/m08/work/record.jpg').convert('L')).astype(float)
print(im.shape, im.min(), im.max())
d=im<128
for y in range(90): print(''.join('#' if d[y,x] else '.' for x in range(0,150)))
