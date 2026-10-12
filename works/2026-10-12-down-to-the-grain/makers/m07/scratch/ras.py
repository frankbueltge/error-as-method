import xml.etree.ElementTree as ET,re,base64,io
from PIL import Image,ImageDraw,ImageFont
S=2
root=ET.parse('out.svg').getroot()
im=Image.new('RGBA',(1100*S,800*S),(243,239,230,255))
def col(c,op=1.0):
  if c.startswith('#'):
    c=c[1:]; r,g,b=int(c[0:2],16),int(c[2:4],16),int(c[4:6],16); a=int(c[6:8],16)/255 if len(c)==8 else 1
  else:
    r,g,b=map(int,re.findall(r'\d+',c)); a=1
  return (r,g,b,int(255*a*op))
try: font=lambda s:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',int(s*S))
except: font=None
def walk(e,inh):
  global im
  tag=e.tag.split('}')[1]
  inh=dict(inh); inh.update(e.attrib)
  ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
  f=lambda k,dv=0:float(inh.get(k,dv))
  if tag=='rect' and 'clip' not in inh.get('_p',''):
    x,y,w,h=f('x'),f('y'),f('width'),f('height'); r=f('rx')
    d.rounded_rectangle([x*S,y*S,(x+w)*S,(y+h)*S],radius=r*S,fill=col(inh.get('fill','#000'),f('fill-opacity',1)))
  elif tag=='line':
    d.line([f('x1')*S,f('y1')*S,f('x2')*S,f('y2')*S],fill=col(inh.get('stroke','#000'),f('stroke-opacity',1)),width=max(1,int(f('stroke-width',1)*S)))
  elif tag=='text':
    fs=f('font-size',12); fn=font(fs)
    txt=e.text or ''
    x,y=f('x'),f('y'); anc=inh.get('text-anchor','start')
    c=col('#1d2433',f('fill-opacity',1))
    if txt:
      w=d.textlength(txt,font=fn)/S
      xx=x-(w if anc=='end' else w/2 if anc=='middle' else 0)
      d.text((xx*S,(y-fs*0.8)*S),txt,font=fn,fill=c)
    yy=y
    for ts in e:
      yy+=float(ts.get('dy',0)); d.text((float(ts.get('x'))*S,(yy-fs*0.8)*S),ts.text,font=fn,fill=c)
    im=Image.alpha_composite(im,ov); return
  elif tag=='image':
    href=[v for k,v in e.attrib.items() if k.endswith('href')][0]
    src=Image.open(io.BytesIO(base64.b64decode(href.split(',')[1]))).convert('RGBA').resize((int(f('width')*S),int(f('height')*S)))
    im.alpha_composite(src,(int(f('x')*S),int(f('y')*S)))
  im=Image.alpha_composite(im,ov)
  if tag in('clipPath',): return
  for c in e:
    if tag=='g' or tag=='svg': walk(c,inh)
walk(root,{})
im.convert('RGB').resize((1100,800),Image.LANCZOS).save('out.png')
