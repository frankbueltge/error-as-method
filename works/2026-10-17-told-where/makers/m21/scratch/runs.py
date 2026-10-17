from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m21/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
# bottom baseline rows 83-84: darkness per column
d=[ (255-px[x,83])+(255-px[x,84]) for x in range(W)]
runs=[];cur=None
for x in range(W):
    on=d[x]>200
    if on and cur is None: cur=x
    if not on and cur is not None: runs.append((cur,x-1)); cur=None
if cur is not None: runs.append((cur,W-1))
print(len(runs))
for r in runs: print(r, r[1]-r[0]+1, sum(d[r[0]:r[1]+1]))
# top of dots per column (min y with dark < 150 excluding baseline)
top=[]
for x in range(W):
    ys=[y for y in range(0,82) if px[x,y]<150]
    top.append(min(ys) if ys else None)
print(top)
