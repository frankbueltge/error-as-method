import re,sys
from PIL import Image,ImageDraw
S=2
svg=open(sys.argv[1]).read()
base=Image.new('RGBA',(1100*S,800*S),(243,239,230,255))
lay=Image.new('RGBA',base.size,(0,0,0,0))
for cx,cy,rx,ry,a in re.findall(r'<ellipse cx="([\d.]+)" cy="([\d.]+)" rx="([\d.]+)" ry="([\d.]+)" fill-opacity="([\d.]+)"',svg):
    cx,cy,rx,ry,a=map(float,(cx,cy,rx,ry,a))
    e=Image.new('RGBA',base.size,(0,0,0,0))
    o=Image.new('RGBA',(int(2*rx*S)+2,int(2*ry*S)+2),(0,0,0,0))
    ImageDraw.Draw(o).ellipse([0,0,2*rx*S,2*ry*S],fill=(29,27,25,int(a*255)))
    lay.alpha_composite(o,(int((cx-rx)*S),int((cy-ry)*S)))
base.alpha_composite(lay)
d=ImageDraw.Draw(base)
for m in re.findall(r'<path d="([^"]+)" fill="none" stroke="([^"]+)"',svg):
    pts=[(float(a)*S,float(b)*S) for a,b in re.findall(r'[ML]([\d.]+) ([\d.]+)',m[0])]
    d.line(pts,fill=m[1],width=S)
base.convert('RGB').save(sys.argv[2])
