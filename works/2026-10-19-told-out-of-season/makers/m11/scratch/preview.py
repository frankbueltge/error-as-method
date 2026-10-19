import math
from PIL import Image, ImageDraw
D=[float(l) for l in open('values.txt')]; N=len(D)
S=2; W,H=1100,800
im=Image.new('RGB',(W*S,H*S),(232,226,214)); g=ImageDraw.Draw(im)
cx,cy=550,400; DISC,R0,R1=384,368,100
g.ellipse([(cx-DISC)*S,(cy-DISC)*S,(cx+DISC)*S,(cy+DISC)*S],fill=(20,19,17))
def val(t):
    i=math.floor(t); f=t-i
    p=lambda k:D[max(0,min(N-1,k))]
    a,b,c,d=p(i-1),p(i),p(i+1),p(i+2)
    return b+0.5*f*(c-a+f*(2*a-5*b+4*c-d+f*(3*(b-c)+d-a)))
def width(v):
    u=max(0,min(1,(v-4)/80)); return 0.3+5.4*u**2.0
for d in range(61):
    t0=d*24; t1=min(N-1,(d+1)*24+0.25); o=[];inn=[]; t=t0
    while t<=t1+1e-9:
        tt=min(t,N-1); ang=-math.pi/2+tt/24*2*math.pi; r=R0-(R0-R1)*tt/(N-1); w=width(val(tt))
        o.append(((cx+math.cos(ang)*(r+w/2))*S,(cy+math.sin(ang)*(r+w/2))*S))
        inn.append(((cx+math.cos(ang)*(r-w/2))*S,(cy+math.sin(ang)*(r-w/2))*S)); t+=1/8
    for k in range(len(o)-1):
        tt=min(t0+(k+0.5)/8,N-1); u=max(0,min(1,(val(tt)-4)/80))
        L=0.2+0.8*u**1.5
        col=(int(40+L*206),int(36+L*200),int(32+L*180))
        g.polygon([o[k],o[k+1],inn[k+1],inn[k]],fill=col)
g.ellipse([(cx-74)*S,(cy-74)*S,(cx+74)*S,(cy+74)*S],fill=(232,226,214))
im.resize((W,H),Image.LANCZOS).save('preview.png')
im.crop((550*S,40*S,940*S,400*S)).save('crop.png')
