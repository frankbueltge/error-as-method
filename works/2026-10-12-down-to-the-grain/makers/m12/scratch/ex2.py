from PIL import Image
im=Image.open('/tmp/claude-0/s122/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
for T in (230,215,200,180):
  pk=[]
  for x in range(W):
    for y in range(H):
      v=px[x,y]
      if v<T and all(v<=px[x+a,y+b] for a in(-1,0,1) for b in(-1,0,1) if 0<=x+a<W and 0<=y+b<H and (a,b)!=(0,0)):
        pk.append((x,y,v))
  # dedupe equal plateau
  print(T,len(pk))
