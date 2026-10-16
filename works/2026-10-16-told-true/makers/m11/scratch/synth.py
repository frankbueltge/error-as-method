import math,random
from PIL import Image, ImageDraw
random.seed(1)
def render(vals):
    im=Image.new('L',(1200,360),255); dr=ImageDraw.Draw(im)
    lo,hi=min(vals),max(vals)
    for i,v in enumerate(vals):
        x=(3+i*293/1463)*4; y=(87-(v-lo)/(hi-lo)*80)*4
        dr.ellipse([x-5,y-5,x+5,y+5],fill=0)
    return im.resize((300,90),Image.LANCZOS)
def spec(im,fs):
    p=im.load(); hpp=1463/293; out=[]
    cen=[]
    for x in range(3,297):
        col=[max(0,255-p[x,y]-15) for y in range(90)]; s=sum(col)
        cen.append((x,sum(y*c for y,c in enumerate(col))/s))
    m=sum(c for _,c in cen)/len(cen)
    for f in fs:
        re=sum((c-m)*math.cos(2*math.pi*f*(x-3)*hpp/24) for x,c in cen); im_=sum((c-m)*math.sin(2*math.pi*f*(x-3)*hpp/24) for x,c in cen)
        out.append(round(math.hypot(re,im_)))
    return out
fs=[0.9295,1.0,1.0027,1.932,2.0]
tide=[math.cos(2*math.pi*1.932*t/24)+0.4*math.cos(2*math.pi*2*t/24)+0.3*math.cos(2*math.pi*1.0027*t/24)+0.25*math.cos(2*math.pi*0.9295*t/24)+random.gauss(0,0.3) for t in range(1464)]
print('synthetic semidiurnal tide', fs, spec(render(tide),fs))
diur=[math.cos(2*math.pi*1.0027*t/24)+0.7*math.cos(2*math.pi*0.9295*t/24)+0.2*math.cos(2*math.pi*1.932*t/24)+random.gauss(0,0.3) for t in range(1464)]
print('synthetic diurnal tide', spec(render(diur),fs))
real=Image.open('/tmp/claude-0/s130/mk/m11/work/record.jpg').convert('L')
print('record', spec(real,fs))
render(tide).save('synth_tide.png')
