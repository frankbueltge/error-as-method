from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m14/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
print(W,H, im.mode)
hist=[0]*256
for x in range(W):
  for y in range(H): hist[px[x,y]]+=1
print([sum(hist[i*16:(i+1)*16]) for i in range(16)])
for y in range(H):
  print('%2d '%y+''.join('#' if px[x,y]<100 else ('+' if px[x,y]<180 else ' ') for x in range(W)))
