import json
from PIL import Image, ImageDraw
s=json.load(open('/tmp/claude-0/s122/mk/m08/scratch/series.json'))
for key in ('rec','model'):
    im=Image.new('L',(300,90),255); d=ImageDraw.Draw(im)
    N=1464
    for t,v in enumerate(s[key]):
        x=2.9+t*(296.4-2.9)/(N-1); d.rectangle([round(x),round(v-1),round(x)+1,round(v)],fill=40)
    im.resize((1200,360),Image.NEAREST).save(f'/tmp/claude-0/s122/mk/m08/scratch/re_{key}.png')
