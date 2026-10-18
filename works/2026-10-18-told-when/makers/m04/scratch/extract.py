from PIL import Image
import json, math
im=Image.open('/tmp/claude-0/s135/mk/m04/work/record.jpg').convert('L')
w,h=im.size;p=im.load()
# row darkness profile
prof=[sum(255-p[x,y] for x in range(w)) for y in range(h)]
for y in range(h):
    if prof[y]>300: print(y,prof[y])
