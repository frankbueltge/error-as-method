from PIL import Image
g=Image.open('../work/record.jpg').convert('L'); w,h=g.size; p=g.load()
T=170
for x in range(w):
    ys=[y for y in range(h) if p[x,y]<T]
    ink=sum(max(0,255-p[x,y]) for y in range(h))
    if ys:
        m=sum((255-p[x,y])*y for y in range(h))/max(ink,1)
        print(x,len(ys),min(ys),max(ys),round(m,1),round(ink/255,1))
    else: print(x,0)
