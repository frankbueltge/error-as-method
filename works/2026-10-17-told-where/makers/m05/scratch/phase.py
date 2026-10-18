from PIL import Image
import math
im=Image.open('/tmp/claude-0/s133/mk/m05/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
d=[[max(0,(255-p[x,y])/255-0.06) for x in range(W)] for y in range(H)]
col=[sum(d[y][x]*max(0,(83.5-y)/78) for y in range(81)) for x in range(W)]
colf=[d[83][x]+d[84][x] for x in range(W)]
best=[]
for per in [4.78+i*0.005 for i in range(17)]:
    c=sum(col[x]*complex(math.cos(2*math.pi*(x+0.5)/per),math.sin(2*math.pi*(x+0.5)/per)) for x in range(W))
    f=sum(colf[x]*complex(math.cos(2*math.pi*(x+0.5)/per),math.sin(2*math.pi*(x+0.5)/per)) for x in range(W))
    ph=math.atan2(c.imag,c.real)/(2*math.pi)*per%per
    phf=math.atan2(f.imag,f.real)/(2*math.pi)*per%per
    best.append((round(abs(c),1),round(per,3),'noon x',round(ph,2),'floor x',round(phf,2),'diff',round((ph-phf)%per,2)))
for b in sorted(best,reverse=True)[:6]: print(b)
