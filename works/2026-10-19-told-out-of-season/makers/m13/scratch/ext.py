from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m13/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
print(W,H)
cols=[]
for x in range(W):
    ys=[y for y in range(H) if p[x,y]<128]
    cols.append(ys)
# print ascii
for y in range(H):
    print(''.join('#' if p[x,y]<100 else ('+' if p[x,y]<170 else ' ') for x in range(W)))
import json
json.dump(cols,open('cols.json','w'))
