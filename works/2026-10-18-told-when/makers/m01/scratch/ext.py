from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s135/mk/m01/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
dark=[[max(0,255-p[x,y])/255 for y in range(H)] for x in range(W)]
# row profile
prof=[sum(dark[x][y] for x in range(W)) for y in range(H)]
for y in range(H): print(y, round(prof[y],1))
