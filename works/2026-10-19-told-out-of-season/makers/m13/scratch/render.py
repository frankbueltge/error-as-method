import json,sys
from PIL import Image, ImageDraw
d=json.load(open('series_y.json'));xs=d['xs'];v=d['vals']
S=4
out=Image.open('/tmp/claude-0/s137/mk/m13/work/record.jpg').convert('RGB').resize((300*S,90*S))
dr=ImageDraw.Draw(out)
for t in range(len(v)-1):
    dr.line([xs[t]*S+S/2,v[t]*S+S/2,xs[t+1]*S+S/2,v[t+1]*S+S/2],fill=(255,0,0),width=1)
out.save('overlay.png')
out.crop((0,0,600,360)).resize((1200,720)).save('overlay_zoom.png')
