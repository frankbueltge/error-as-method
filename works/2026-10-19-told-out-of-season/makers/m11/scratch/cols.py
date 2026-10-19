from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m11/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
out=[]
for x in range(W):
    ink=[max(0,235-p[x,y]) for y in range(H)]
    tot=sum(ink)
    ys=[y for y in range(H) if p[x,y]<140]
    if tot==0: out.append((x,0,None,None,None));continue
    mean=sum(y*i for y,i in enumerate(ink))/tot
    out.append((x,tot,min(ys) if ys else None,max(ys) if ys else None,round(mean,1)))
for o in out: print(*o)
