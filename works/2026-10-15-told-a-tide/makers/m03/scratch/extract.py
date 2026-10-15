from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m03/work/record.jpg').convert('L')
W,H=im.size; print(W,H)
im.resize((W*4,H*4),Image.NEAREST).save('big.png')
px=im.load()
import json
cols=[]
for x in range(W):
    c=[(y,255-px[x,y]) for y in range(H) if px[x,y]<140]
    cols.append(c)
json.dump({'W':W,'H':H,'cols':cols},open('cols.json','w'))
hist=[0]*256
for x in range(W):
  for y in range(H): hist[px[x,y]]+=1
print([sum(hist[i:i+32]) for i in range(0,256,32)])
print('dark per col', [len(c) for c in cols][:60])
# row occupancy
rows=[sum(1 for x in range(W) if px[x,y]<140) for y in range(H)]
print('rows',rows)
