from PIL import Image; import numpy as np
im=np.array(Image.open('/tmp/claude-0/s131/mk/m13/work/record.jpg').convert('L')).astype(int)
print(im.shape, im.min(), im.max())
for y in range(90):
    print('%2d '%y+''.join('#' if v<100 else ('+' if v<180 else ' ') for v in im[y]))
