from PIL import Image
g=Image.open('/tmp/claude-0/s122/mk/m07/work/record.jpg').convert('L')
W,H=g.size
P=[[max(0,255-g.getpixel((x,y))-30) for x in range(W)] for y in range(H)]
def ac(dx,xa=3,xb=210):
  s=0;n=0
  for y in range(40,85):
    for x in range(xa,xb):
      if x+dx<W: s+=P[y][x]*P[y][x+dx]+0.5*(P[y][x]*P[y-1][x+dx]+P[y][x]*P[y+1][x+dx]); n+=1
  return s/n
a=[ac(d) for d in range(0,90)]
b=a[0]
for d in range(1,90): print(d, round(100*a[d]/b), '#'*int(100*a[d]/b-20))
