from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m05/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
d=[[max(0,255-p[x,y])/255 for x in range(W)] for y in range(H)]
# isolated dots: local max in rows 3..70, with nothing else inked in 7x7 ring
res=[]
for y in range(3,70):
  for x in range(3,W-3):
    v=d[y][x]
    if v<0.3: continue
    if any(d[y+j][x+i]>v for i in (-1,0,1) for j in (-1,0,1)): continue
    inner=sum(d[y+j][x+i] for i in range(-1,2) for j in range(-1,2))
    big=sum(d[y+j][x+i] for i in range(-3,4) for j in range(-3,4))
    if big-inner<0.9: res.append((round(inner,2),round(big,2),x,y))
res.sort()
print(len(res)); print(res[:10]); print(res[-10:])
import statistics
print('median inner',statistics.median(r[0] for r in res),'median big',statistics.median(r[1] for r in res))
# show a few
for _,_,x,y in res[len(res)//2:len(res)//2+3]:
  for j in range(-2,3): print(' '.join('%3d'%(255-int(d[y+j][x+i]*255)) for i in range(-2,3)))
  print()
