from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m05/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
d=[[max(0,255-p[x,y])/255 for x in range(W)] for y in range(H)]
cols=[x for x in range(W) if sum(d[y][x] for y in range(H))>0.5]
print('first/last col with ink',cols[0],cols[-1])
rows=[y for y in range(H) if sum(d[y])>0.5]; print('rows',rows[0],rows[-1])
# column ink profile left/right edges
print([round(sum(d[y][x] for y in range(H)),1) for x in range(0,8)])
print([round(sum(d[y][x] for y in range(H)),1) for x in range(292,300)])
# top rows: first ink per column
for y in range(0,8): print(y,[x for x in range(W) if d[y][x]>0.1])
