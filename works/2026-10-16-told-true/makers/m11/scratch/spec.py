from PIL import Image
import math
im=Image.open('/tmp/claude-0/s130/mk/m11/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
d=[[max(0,255-p[x,y]-15) for y in range(H)] for x in range(W)]
def q(col,f):
    t=sum(col); a=0
    for y in range(H):
        a+=col[y]
        if a>=f*t: return y
d=d[2:298]
cen=[sum(y*c for y,c in enumerate(col))/sum(col) for col in d]
top=[q(c,0.1) for c in d]; bot=[q(c,0.9) for c in d]
ink=[sum(c) for c in d]
rng=[b-t for t,b in zip(top,bot)]
def spec(s,name):
    m=sum(s)/len(s); s=[v-m for v in s]; N=len(s)
    out=[]
    for P10 in range(22,1500,1):
        P=P10/10
        re=sum(v*math.cos(2*math.pi*i/P) for i,v in enumerate(s)); im_=sum(v*math.sin(2*math.pi*i/P) for i,v in enumerate(s))
        out.append((re*re+im_*im_,P))
    out.sort(reverse=True)
    print(name,[(round(P,1),round(pw/1e3)) for pw,P in out[:12]])
for s,n in [(cen,'cen'),(top,'top'),(bot,'bot'),(rng,'rng'),(ink,'ink')]: spec(s,n)
print('hours per px',1464/len(d))
for x in range(len(d)): print(x, round(cen[x],1), top[x], bot[x], ink[x]//100)
