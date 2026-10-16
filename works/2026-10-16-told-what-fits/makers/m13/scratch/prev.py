import re
from PIL import Image,ImageDraw
s=open('work.svg').read();S=2
img=Image.new('RGBA',(1100*S,800*S),(243,239,230,255))
def pts(d):
    toks=re.findall(r'[MCLZ]|-?\d+\.?\d*',d);out=[];i=0;cur=None
    while i<len(toks):
        t=toks[i]
        if t in 'ML': cur=(float(toks[i+1]),float(toks[i+2]));out.append(cur);i+=3
        elif t=='C':
            c=[float(x) for x in toks[i+1:i+7]];p0=cur
            for k in range(1,9):
                u=k/8;a=(1-u)**3;b=3*u*(1-u)**2;cc=3*u*u*(1-u);e=u**3
                out.append((a*p0[0]+b*c[0]+cc*c[2]+e*c[4],a*p0[1]+b*c[1]+cc*c[3]+e*c[5]))
            cur=(c[4],c[5]);i+=7
        else:i+=1
    return [(x*S,y*S) for x,y in out]
def col(h,a=1.0): return (int(h[1:3],16),int(h[3:5],16),int(h[5:7],16),int(255*a))
for m in re.finditer(r'<path d="([^"]*)"([^>]*)/>',s):
    d,at=m.groups();P=pts(d)
    lay=Image.new('RGBA',img.size,(0,0,0,0));dr=ImageDraw.Draw(lay)
    fo=re.search(r'fill-opacity="([\d.]+)"',at); fill=re.search(r'fill="(#\w+)"',at); st=re.search(r'stroke="(#\w+)"',at); sw=re.search(r'stroke-width="([\d.]+)"',at); so=re.search(r'stroke-opacity="([\d.]+)"',at)
    if fill: dr.polygon(P,fill=col(fill.group(1),float(fo.group(1)) if fo else 1))
    if st: dr.line(P,fill=col(st.group(1),float(so.group(1)) if so else 1),width=max(1,round(float(sw.group(1))*S)))
    img=Image.alpha_composite(img,lay)
img.convert('RGB').resize((1100,800),Image.LANCZOS).save('preview.png')
