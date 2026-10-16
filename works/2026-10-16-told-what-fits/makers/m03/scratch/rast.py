import re
from PIL import Image, ImageDraw, ImageFont
S=2
s=open('prev.svg').read()
img=Image.new('RGBA',(1100*S,800*S),(243,238,228,255))
def rgb(c):
    if c.startswith('#'):
        c=c[1:]; return tuple(int(c[i:i+2],16) for i in (0,2,4))
    return tuple(int(x) for x in re.findall(r'\d+',c))
for m in re.finditer(r'<(path|circle|line|text) ([^>]*)>([^<]*)',s):
    t,at,tx=m.groups(); a=dict(re.findall(r'(\S+?)="([^"]*)"',at))
    lay=Image.new('RGBA',img.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    if t=='path':
        nums=[float(v) for v in re.findall(r'-?[\d.]+',a['d'])]
        pts=[(nums[0]*S,nums[1]*S)]
        if 'C' in a['d']:
            q=nums[2:]
            for j in range(0,len(q),6):
                x0,y0=pts[-1][0]/S,pts[-1][1]/S; x1,y1,x2,y2,x3,y3=q[j:j+6]
                for k in range(1,9):
                    t=k/8; u=1-t
                    pts.append(((u**3*x0+3*u*u*t*x1+3*u*t*t*x2+t**3*x3)*S,(u**3*y0+3*u*u*t*y1+3*u*t*t*y2+t**3*y3)*S))
        else:
            pts=[(nums[i]*S,nums[i+1]*S) for i in range(0,len(nums),2)]
        op=float(a.get('stroke-opacity',1)); d.line(pts,fill=rgb(a['stroke'])+(int(255*op),),width=max(1,int(float(a['stroke-width'])*S)),joint='curve')
    elif t=='circle':
        x,y,r=float(a['cx'])*S,float(a['cy'])*S,float(a['r'])*S
        op=float(a.get('fill-opacity',1))
        if a.get('fill','none')!='none': d.ellipse([x-r,y-r,x+r,y+r],fill=rgb(a['fill'])+(int(255*op),))
        else: d.ellipse([x-r,y-r,x+r,y+r],outline=rgb(a['stroke'])+(255,),width=1)
    elif t=='line':
        d.line([float(a['x1'])*S,float(a['y1'])*S,float(a['x2'])*S,float(a['y2'])*S],fill=(58,42,28,140),width=1)
    elif t=='text':
        f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(float(a['font-size'])*S))
        d.text((float(a['x'])*S,float(a['y'])*S-float(a['font-size'])*S*0.8),tx.replace('&amp;','&'),font=f,fill=(58,42,28,255))
    img=Image.alpha_composite(img,lay)
img.resize((1100,800),Image.LANCZOS).convert('RGB').save('prev.png')
