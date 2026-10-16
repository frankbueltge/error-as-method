import re
from PIL import Image, ImageDraw, ImageFont
s=open('/tmp/claude-0/s130/mk/m01/work/index.html').read()
S=2
im=Image.new('RGB',(1100*S,800*S),(242,238,229)); d=ImageDraw.Draw(im,'RGBA')
def pathpts(p):
    toks=re.findall(r'[MLCZ]|-?[\d.]+',p); out=[]; i=0; cur=None
    while i<len(toks):
        c=toks[i]; i+=1
        if c in 'ML':
            cur=(float(toks[i]),float(toks[i+1])); i+=2; out.append(cur)
        elif c=='C':
            a=[float(x) for x in toks[i:i+6]]; i+=6
            for k in range(1,9):
                t=k/8; u=1-t
                out.append((u**3*cur[0]+3*u*u*t*a[0]+3*u*t*t*a[2]+t**3*a[4], u**3*cur[1]+3*u*u*t*a[1]+3*u*t*t*a[3]+t**3*a[5]))
            cur=(a[4],a[5])
    return [(x*S,y*S) for x,y in out]
for g in re.findall(r'<g>(.*?)</g>',s):
    d.polygon(pathpts(re.search(r'<path d="([^"]+)" class="f"',g).group(1)),fill=(242,238,229))
    d.line(pathpts(re.search(r'<path d="([^"]+)" class="l"',g).group(1)),fill=(28,27,25,205),width=2)
    for cx,cy,r,c in re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="([\d.]+)" class="(\w)"',g):
        cx,cy,r=float(cx)*S,float(cy)*S,float(r)*S
        d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=(194,65,29) if c=='h' else (28,27,25))
for x,y,cls,txt in re.findall(r'<text x="([\d.]+)" y="([\d.]+)" class="(\w)"[^>]*>([^<]+)<',s):
    d.text((float(x)*S,float(y)*S-{'t':30,'s':13,'m':11}[cls]*S),txt,fill=(28,27,25),font=ImageFont.load_default(size={'t':30,'s':13,'m':11}[cls]*S))
im.resize((1100,800),Image.LANCZOS).save('/tmp/claude-0/s130/mk/m01/scratch/preview.png')
