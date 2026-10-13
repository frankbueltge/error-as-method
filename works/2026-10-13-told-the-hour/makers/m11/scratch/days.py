from PIL import Image
im=Image.open('/tmp/claude-0/s123/mk/m11/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
sc=295/1463
for d in range(61):
    x0=2+24*d*sc; x1=2+24*(d+1)*sc
    ys=[y for x in range(int(round(x0)),int(round(x1))) for y in range(H) if px[x,y]<130]
    if not ys: print(d,'-'); continue
    ys.sort()
    hi=ys[max(0,len(ys)//20)]; lo=ys[min(len(ys)-1,len(ys)*19//20)]
    print(f"{d:2d} wk{d%7} hi{hi:3d} lo{lo:3d} amp{lo-hi:3d} " + '#'*((80-hi)//2))
