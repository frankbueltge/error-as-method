from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m08/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
xs=[x for x in range(W) for y in range(H) if p[x,y]<150]
ys=[y for x in range(W) for y in range(H) if p[x,y]<150]
print('x',min(xs),max(xs),'y',min(ys),max(ys))
pd=W/61
for d in range(61):
    a,b=d*pd,(d+1)*pd
    fl=0;up=0;cnt=[0]*9
    for x in range(W):
        w=max(0,min(b,x+1)-max(a,x))
        if not w: continue
        for y in range(H):
            ink=(255-p[x,y])/255*w
            if y>=82: fl+=ink
            else:
                up+=ink; cnt[y//10]+=ink
    print(d,'floor %.1f up %.1f'%(fl,up),' '.join('%4.1f'%c for c in cnt))
