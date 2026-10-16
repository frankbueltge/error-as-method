import json, math
from PIL import Image, ImageDraw, ImageFont
v=json.load(open('series2.json'))
W,H,S=1100,800,3
L,R,T,B=86,86,70,150; cw=(W-L-R)/61
vmin,vmax=min(v),max(v)
Y=lambda q:T+(vmax-q)/(vmax-vmin)*(H-T-B)
night,day=(26,32,66),(216,142,44)
sun=lambda h:(1-math.cos(2*math.pi*h/24))/2
col=lambda h,a:tuple(round(night[i]+(day[i]-night[i])*sun(h)) for i in range(3))+(int(a*255),)
im=Image.new('RGB',(W*S,H*S),(243,239,230)); dr=ImageDraw.Draw(im,'RGBA')
for d in range(61):
    hs=v[d*24:d*24+24]; x0=L+d*cw; xc=x0+cw/2
    dr.rectangle([(xc-.5)*S,Y(max(hs))*S,(xc+.5)*S,Y(min(hs))*S],fill=(90,80,70,70))
    for h in sorted(range(24),key=lambda h:-sun(h)):
        y=Y(hs[h]); dr.rectangle([(x0+2.4)*S,(y-1.1)*S,(x0+cw-2.4)*S,(y+1.1)*S],fill=col(h,.82))
ky=H-78
fi=ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf',25*S)
fr=ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',int(12.5*S))
fs=ImageFont.truetype('/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf',11*S)
dr.text((L*S,(ky-12)*S),'Sixty-one Breaths',font=fi,fill=(28,34,64),anchor='ls')
for i,s in enumerate(['Carbon dioxide in the air at one station, hourly for sixty-one days.','Each column is a day, each stroke an hour; higher means more.','The source gave no scale, place or date, so none is given here.']):
    dr.text((L*S,(ky+14+18*i)*S),s,font=fr,fill=(109,106,98),anchor='ls')
kw=7;kx2=W-R-24*kw
for h in range(24): dr.rectangle([(kx2+h*kw+1)*S,(ky-2)*S,(kx2+h*kw+kw-1)*S,(ky+.2)*S],fill=col(h,.9))
for h in (0,6,12,18): dr.text(((kx2+h*kw+kw/2)*S,(ky+14)*S),str(h),font=fs,fill=(109,106,98),anchor='ms')
dr.text(((W-R)*S,(ky+32)*S),'hour of the day, counted from the first value',font=fs,fill=(109,106,98),anchor='rs')
im.resize((W,H),Image.LANCZOS).save('final.png')
