from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s130/mk/m10/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
D=lambda x,y: max(0,235-p[x,y]) if 0<=x<W and 0<=y<H else 0
pts=[]
for x in range(W):
    for y in range(H):
        d=D(x,y)
        if p[x,y]>165: continue
        if all(d>=D(x+i,y+j) for i in(-1,0,1) for j in(-1,0,1) if (i,j)!=(0,0)):
            s=sx=sy=0
            for i in(-1,0,1):
                for j in(-1,0,1):
                    w=D(x+i,y+j); s+=w; sx+=w*(x+i); sy+=w*(y+j)
            pts.append((sx/s,sy/s,s))
print('n',len(pts),'x range',min(p_[0] for p_ in pts),max(p_[0] for p_ in pts),'y range',min(p_[1] for p_ in pts),max(p_[1] for p_ in pts))
print('total ink / mean blob ink', sum(max(0,235-p[x,y]) for x in range(W) for y in range(H))/ (sum(q[2] for q in pts)/len(pts)) )
json.dump(pts,open('pts.json','w'))
# period fit using blobs: maximize |sum (v-mean) e^{-i 2pi t/P}|
x0=min(q[0] for q in pts); x1=max(q[0] for q in pts)
for span in (x1-x0, 296.0, 294.0):
    hp=1463/span
    T=[(q[0]-x0)*hp for q in pts]; V=[-q[1] for q in pts]; mv=sum(V)/len(V)
    best=max(((abs(sum((v-mv)*complex(math.cos(2*math.pi*t/P),-math.sin(2*math.pi*t/P)) for t,v in zip(T,V))),P) for P in [22+k*0.01 for k in range(400)]))
    semi=max(((abs(sum((v-mv)*complex(math.cos(2*math.pi*t/P),-math.sin(2*math.pi*t/P)) for t,v in zip(T,V))),P) for P in [11.5+k*0.01 for k in range(150)]))
    print('span %.1f px -> best diurnal P %.2f h amp %.0f ; best semidiurnal P %.2f amp %.0f'%(span,best[1],best[0],semi[1],semi[0]))
