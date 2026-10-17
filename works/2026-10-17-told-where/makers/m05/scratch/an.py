from PIL import Image
im=Image.open('/tmp/claude-0/s133/mk/m05/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
d=[[max(0,255-p[x,y])/255 for x in range(W)] for y in range(H)]
# bottom rows profile
for y in range(78,90):
    print(y, round(sum(d[y]),1))
# column darkness in floor band 84-85
band=[d[84][x]+d[85][x] for x in range(W)]
print(''.join(str(min(9,int(b*5))) for b in band))
# autocorr of band
import math
m=sum(band)/W
for lag in range(3,8):
    pass
best=[]
for per10 in range(470,520):
    per=per10/100
    # phase coherence
    c=sum(band[x]*complex(math.cos(2*math.pi*x/per),math.sin(2*math.pi*x/per)) for x in range(W))
    best.append((abs(c),per,math.degrees(math.atan2(c.imag,c.real))))
best.sort(reverse=True);print(best[:5])
