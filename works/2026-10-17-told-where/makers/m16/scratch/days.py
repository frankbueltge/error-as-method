from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m16/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
ink=lambda x,y:255-px[x,y]
x0,x1=3,296  # approx data extent
pd=(x1-x0)/61
for d in range(61):
    a=x0+d*pd; b=a+pd
    cols=[x for x in range(W) if a<=x+0.5<b]
    best=None
    for x in cols:
        for y in range(0,81):
            if ink(x,y)>110:
                if best is None or y<best[1]: best=(x,y)
                break
    lit=sum(1 for x in cols if ink(x,83)+ink(x,84)<150)
    print(d, cols, 'max h=%s'%(83.5-best[1] if best else None), 'at x', best[0]-a if best else None, 'gapcols',lit)
