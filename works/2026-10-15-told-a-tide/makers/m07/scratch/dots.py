from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m07/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
# local minima detection
for thr in (120,150,180):
    pts=[]
    for x in range(1,W-1):
        for y in range(1,H-1):
            v=px[x,y]
            if v>thr: continue
            nb=[px[x+dx,y+dy] for dx in(-1,0,1) for dy in(-1,0,1) if dx or dy]
            if all(v<=n for n in nb): pts.append((x,y))
    print(thr,len(pts))
# total ink estimate vs single dot ink
tot=sum(max(0,240-px[x,y]) for x in range(W) for y in range(H))
print('total ink',tot, 'per value', tot/1464)
