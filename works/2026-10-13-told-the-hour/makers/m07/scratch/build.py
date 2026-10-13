from PIL import Image
import json
im=Image.open('work/record.jpg').convert('L'); W,H=im.size; N=1464
cols=[]
for x in range(W):
    d=[max(0,(255-im.getpixel((x,y)))-30) for y in range(H)]
    tot=sum(d); n=(x+1)*N//W - x*N//W
    pos=[]
    for k in range(n):
        q=(k+0.5)/n*tot; acc=0
        for y in range(H):
            if acc+d[y]>=q and d[y]>0:
                pos.append(round(y+(q-acc)/d[y],3)); break
            acc+=d[y]
    cols.append(pos)
json.dump({'cols':cols,'px':[[im.getpixel((x,y)) for x in range(W)] for y in range(H)]},open('scratch/data.json','w'))
print([len(c) for c in cols], sum(len(c) for c in cols))
print([ (c[0],c[-1]) for c in cols][:5])
