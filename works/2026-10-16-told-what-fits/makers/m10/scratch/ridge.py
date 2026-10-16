from PIL import Image, ImageDraw; import sys
V=[int(v) for v in open('/tmp/claude-0/s131/mk/m10/scratch/data.txt').read().split(',')]
vmin,vmax=min(V),max(V); order=sys.argv[1]
S=2; im=Image.new('RGB',(1100*S,800*S),(243,239,230)); dr=ImageDraw.Draw(im)
x0,x1=70,770; top,bot=150,700; Hs=150; sp=(bot-top)/60
days=range(61) if order=='down' else range(60,-1,-1)
for d in days:
    base=top+d*sp
    pts=[]
    for h in range(25):
        i=min(d*24+h,len(V)-1)
        pts.append(((x0+(x1-x0)*h/24)*S,(base+Hs*0.5-(V[i]-vmin)/(vmax-vmin)*Hs)*S))
    if order=='down': poly=pts+[(x1*S,(base+Hs)*S),(x0*S,(base+Hs)*S)]
    else: poly=pts+[(x1*S,(base-Hs)*S),(x0*S,(base-Hs)*S)]
    dr.polygon(poly,fill=(243,239,230)); dr.line(pts,fill=(36,33,29),width=2)
im.resize((1100,800),Image.LANCZOS).save(f'/tmp/claude-0/s131/mk/m10/scratch/ridge_{order}.png')
