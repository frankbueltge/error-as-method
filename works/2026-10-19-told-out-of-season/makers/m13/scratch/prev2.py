import json,sys
from PIL import Image, ImageDraw
V=json.load(open('/tmp/claude-0/s137/mk/m13/scratch/hourly.json'))
S=2;BG=(19,17,16);im=Image.new('RGB',(1100*S,800*S),BG);d=ImageDraw.Draw(im)
L,R,TOP,PITCH,AMP=150,990,150,68,56
PRE=48  # record starts Wednesday; rows start Monday
def col(v):
    a=(78,88,100);b=(222,204,180);e=(238,122,54)
    if v<.45: t=v/.45;return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))
    t=min(1,(v-.45)/.55);return tuple(int(b[i]+(e[i]-b[i])*t) for i in range(3))
hw=(R-L)/168
for i,v in enumerate(V):
    k=i+PRE;r=k//168;h=k%168
    x=L+(h+.5)*hw;base=TOP+r*PITCH+AMP
    top=base-max(v,0.012)*AMP
    d.rectangle([(x-1.2)*S,top*S,(x+1.2)*S,base*S],fill=col(v))
im.resize((1100,800),Image.LANCZOS).save(sys.argv[1])
