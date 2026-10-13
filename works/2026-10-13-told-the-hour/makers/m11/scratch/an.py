from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s123/mk/m11/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
cols=[]
for x in range(W):
    ys=[(y,255-px[x,y]) for y in range(H) if px[x,y]<170]
    cols.append(ys)
xs=[x for x in range(W) if cols[x]]
print('x extent',xs[0],xs[-1])
allys=[y for c in cols for y,_ in c]; print('y extent',min(allys),max(allys))
top=[min(y for y,_ in c) if c else None for c in cols]
bot=[max(y for y,_ in c) if c else None for c in cols]
mean=[sum(y*w for y,w in c)/sum(w for _,w in c) if c else None for c in cols]
def ac(s,lagmax=40):
    v=[a for a in s if a is not None]; m=sum(v)/len(v)
    out=[]
    for L in range(1,lagmax):
        num=den=0
        for i in range(len(s)-L):
            if s[i] is None or s[i+L] is None: continue
            num+=(s[i]-m)*(s[i+L]-m); 
        den=sum((a-m)**2 for a in v)
        out.append((L,round(num/den,2)))
    return out
for name,s in [('top',top),('bot',bot),('mean',mean)]:
    print(name,ac(s,25))
print('top',top); print('bot',bot)
print([round(m,1) if m else None for m in mean])
