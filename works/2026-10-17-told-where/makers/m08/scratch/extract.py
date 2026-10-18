import json
from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m08/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
pd=W/61; FL=82; ph=1.57
def win(a,b):
    row=[0.0]*FL; fl=0; t=FL; cov=0
    for x in range(W):
        w=max(0,min(b,x+1)-max(a,x))
        if not w: continue
        cov+=w
        for y in range(H):
            ink=max(0,(235-p[x,y]))/235*w
            if y>=FL: fl+=ink
            else:
                row[y]+=ink
                if p[x,y]<150 and y<t: t=y
    return row,fl,t,cov
prof=[];top=[];cov=[];nights=[]
for d in range(61):
    c=ph+d*pd
    r,fl,t,cv=win(c-pd/2,c+pd/2)
    prof.append([round(v*20) for v in r]); top.append(t); cov.append(round(cv/pd,2))
for n in range(60):
    c=ph+(n+0.5)*pd
    r,fl,t,cv=win(c-pd/2,c+pd/2)
    nights.append(round(fl,2))
json.dump({'prof':prof,'top':top,'cov':cov,'night':nights},open('data.json','w'),separators=(',',':'))
print(top);print(cov);print(nights)
