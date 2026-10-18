from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m05/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
d=[[max(0,255-p[x,y])/255 for x in range(W)] for y in range(H)]
P=4.82; x0=3.9; DOT=2.2
above=sum(d[y][x] for y in range(81) for x in range(W))
print('above-floor ink',above,'dots',above/DOT,'per day',above/DOT/61)
for cut in (78,80,81,82):
  print(cut, sum(d[y][x] for y in range(cut) for x in range(W))/DOT/61)
