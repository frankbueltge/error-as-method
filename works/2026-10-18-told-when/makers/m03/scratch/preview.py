import json
from PIL import Image,ImageDraw
D=json.load(open('days.json'))
Z=2;im=Image.new('RGB',(1100*Z,800*Z),(243,239,230));dr=ImageDraw.Draw(im)
L,T,CW,RH,S,DX,DY=74,118,136,70,10,12,3.35
for d in range(61):
    i=d+1;col=i%7;row=i//7;x0=L+col*CW;y0=T+row*RH;cx=x0+14;cy=y0+6
    dr.text((Z*(x0+4),Z*y0),str(d),fill=(138,130,116))
    for l in range(18):
        for k in range(S):
            q=int(D[d][l*S+k]);x=(cx+k*DX)*Z;y=(cy+l*DY)*Z
            if q==0: r=0.55*Z;c=(207,200,184)
            else:
                r=(0.7+q*0.11)*Z;a=0.18+q*0.09;c=tuple(int(243*(1-a)+29*a) for _ in range(3))
            dr.ellipse((x-r,y-r,x+r,y+r),fill=c)
im.save('preview.png')
