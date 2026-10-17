from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m16/work/record.jpg').convert('L');px=im.load()
W,H=im.size
I=lambda x,y:255-px[x,y] if 0<=x<W and 0<=y<H else 0
# isolated dots: local max with ink>120 and nothing dark (>60) in ring of radius 2..4 
res=[]
for x in range(4,W-4):
  for y in range(4,78):
    v=I(x,y)
    if v<120: continue
    if any(I(x+a,y+b)>v for a in(-1,0,1) for b in(-1,0,1)): continue
    ring=[I(x+a,y+b) for a in range(-4,5) for b in range(-4,5) if max(abs(a),abs(b))>=3]
    if max(ring)>40: continue
    for th in (30,60):
      pass
    tot30=sum(I(x+a,y+b) for a in range(-2,3) for b in range(-2,3) if I(x+a,y+b)>30)
    tot60=sum(I(x+a,y+b) for a in range(-2,3) for b in range(-2,3) if I(x+a,y+b)>60)
    w=[sum(I(x+a,y+b) for b in range(-2,3)) for a in range(-2,3)]
    res.append((tot30,tot60,w))
print(len(res))
t30=sorted(r[0] for r in res);t60=sorted(r[1] for r in res)
print('median30',t30[len(t30)//2],'median60',t60[len(t60)//2])
for r in res[:15]: print(r)
