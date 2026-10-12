from PIL import Image
g=Image.open('/tmp/claude-0/s122/mk/m07/work/record.jpg').convert('L')
W,H=g.size
P=[[max(0,255-g.getpixel((x,y))-30) for x in range(W)] for y in range(H)]
def ac(dx,dy,xa=5,xb=210):
  s=0;n=0
  for y in range(40,85):
    for x in range(xa,xb):
      if 0<=y+dy<H and 0<=x+dx<W:
        s+=P[y][x]*P[y+dy][x+dx]; n+=1
  return s/n
base=ac(0,0)
print('rows dy -6..6, cols dx 0..30')
for dy in range(-6,7):
  print('%3d '%dy+' '.join('%3d'%int(100*ac(dx,dy)/base) for dx in range(0,31)))
