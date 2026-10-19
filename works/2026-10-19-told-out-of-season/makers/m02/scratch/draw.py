import json,re
from PIL import Image,ImageDraw
S=2
els=json.load(open('els.json'))
im=Image.new('RGB',(1100*S,800*S),'#f3f0e8'); d=ImageDraw.Draw(im)
def walk(es):
    for e in es:
        a=e['attrs']; n=e['n']
        if n=='circle':
            x,y,r=float(a['cx'])*S,float(a['cy'])*S,float(a['r'])*S
            d.ellipse([x-r,y-r,x+r,y+r],fill=a['fill'])
        elif n=='line':
            d.line([float(a['x1'])*S,float(a['y1'])*S,float(a['x2'])*S,float(a['y2'])*S],fill=a['stroke'],width=1)
        elif n=='path':
            pts=[tuple(float(v)*S for v in p.split(',')) for p in re.split('[ML]',a['d']) if p]
            d.line(pts,fill='#1f3442',width=2)
        elif n=='text':
            d.text((float(a['x'])*S,float(a['y'])*S-12),e['textContent'],fill='#555')
        walk(e['children'])
walk(els)
im.resize((1100,800),Image.LANCZOS).save('out.png')
