from PIL import Image, ImageDraw
import math,json
v=json.load(open('hourly_fit.json'))
S=2
im=Image.new('RGB',(1100*S,800*S),(18,20,23)); d=ImageDraw.Draw(im)
stops=[(0,(18,26,56)),(.2,(30,68,112)),(.4,(52,122,136)),(.56,(130,160,118)),(.72,(206,160,76)),(.86,(240,138,62)),(1,(255,228,176))]
def col(t):
    for i in range(1,len(stops)):
        if t<=stops[i][0]:
            t0,a=stops[i-1];t1,b=stops[i];f=(t-t0)/(t1-t0)
            return tuple(round(a[j]+(b[j]-a[j])*f) for j in range(3))
pal=[col(i/17) for i in range(18)]
cx,cy,r0,pitch=400,400,46,4.95
N=len(v)
R=lambda t:r0+pitch*t/24
A=lambda t:-math.pi/2+2*math.pi*t/24
for h in range(24):
    a=A(h); d.line([((cx+(r0-14)*math.cos(a))*S,(cy+(r0-14)*math.sin(a))*S),((cx+(R(N)+10)*math.cos(a))*S,(cy+(R(N)+10)*math.sin(a))*S)],fill=(42,44,48),width=S)
for i in range(N):
    pts=[]
    for k in range(9):
        t=max(0,i-0.5+k/8); r=R(t); a=A(t); pts.append(((cx+r*math.cos(a))*S,(cy+r*math.sin(a))*S))
    d.line(pts,fill=pal[v[i]],width=round(pitch*0.82*S))
# swatches
for i,c in enumerate(pal): d.rectangle([ (820+i*240/18)*S,580*S,(820+(i+1)*240/18)*S,594*S],fill=c)
im.resize((1100,800),Image.LANCZOS).save('preview.png')
