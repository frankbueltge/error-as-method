from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m21/work/record.jpg').convert('L');px=im.load()
W,H=im.size
def D(x,y): return 255-px[x,y]
# isolated strong dots: darkness>180 and neighborhood within radius 3 otherwise light
ws=[];hs=[]
for y in range(4,78):
  for x in range(4,W-4):
    if D(x,y)<170: continue
    if D(x,y)<max(D(i,j) for i in range(x-1,x+2) for j in range(y-1,y+2)): continue
    ring=[D(i,j) for i in range(x-3,x+4) for j in range(y-3,y+4) if max(abs(i-x),abs(j-y))>=2]
    if max(ring)>60: continue
    row=[D(i,y) for i in range(x-3,x+4)]; col=[D(x,j) for j in range(y-3,y+4)]
    ws.append(sum(row)/D(x,y)); hs.append(sum(col)/D(x,y))
print(len(ws), sum(ws)/len(ws), sum(hs)/len(hs))
# floor profile width at half max
f=[max(D(x,83),D(x,84)) for x in range(W)]
print(f[:60])
