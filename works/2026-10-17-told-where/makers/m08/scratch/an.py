from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m08/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
# floor darkness
fl=[min(p[x,83],p[x,84]) for x in range(W)]
print(' '.join('%3d'%v for v in fl[:60]))
# top envelope per column
top=[]
for x in range(W):
    t=None
    for y in range(H):
        if p[x,y]<170: t=y;break
    top.append(t)
pd=W/61
for d in range(61):
    xs=range(int(d*pd),int((d+1)*pd))
    ts=[top[x] for x in xs if top[x] is not None]
    gaps=[x for x in xs if fl[x]>150]
    print(d, min(ts) if ts else None, 'gapcols',gaps)
